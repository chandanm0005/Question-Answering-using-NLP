from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure NLTK sentence tokenizers are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

app = FastAPI(title="Basic NLP QA API")

# Setup CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QAQuery(BaseModel):
    context: str
    question: str

class QAResponse(BaseModel):
    answer: str
    score: float

@app.post("/ask", response_model=QAResponse)
def ask_question(query: QAQuery):
    if not query.context.strip() or not query.question.strip():
        raise HTTPException(status_code=400, detail="Context and question cannot be empty")
        
    try:
        # 1. Split the text into sentences
        sentences = nltk.sent_tokenize(query.context)
        if not sentences:
            raise ValueError("Context contains no valid sentences")

        # 2. Create an NLP Vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # 3. Fit and transform all text (sentences + question)
        all_text = sentences + [query.question]
        try:
            tfidf_matrix = vectorizer.fit_transform(all_text)
        except ValueError:
            # Handles edge case where there's no english vocabulary found
            raise HTTPException(status_code=400, detail="Could not extract meaningful english words from the context")
        
        # 4. Calculate cosine similarity between the question and all context sentences
        question_vector = tfidf_matrix[-1]
        sentence_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(question_vector, sentence_vectors).flatten()
        
        # 5. Extract the sentence with the highest correlation to the question
        best_idx = similarities.argmax()
        raw_score = float(similarities[best_idx])
        best_sentence = sentences[best_idx].strip()
        
        # Boost confidence score mathematically for better UX (TF-IDF is naturally low)
        boosted_score = min(0.99, (raw_score ** 0.5) * 1.8)
        
        # "Generate" a conversational answer format
        if raw_score < 0.05:
            final_answer = "Sorry, I couldn't find a highly relevant answer to that question in the provided context."
            boosted_score = 0.0
        else:
            final_answer = f"According to the context, {best_sentence[:1].lower() + best_sentence[1:]}"
            
        return QAResponse(
            answer=final_answer,
            score=boosted_score
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
