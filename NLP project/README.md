# Fast NLP Question Answering App

A simple, lightweight, and blazing-fast Natural Language Processing application that extracts answers to questions based on a provided text context.

**[Live Application Link](YOUR_DEPLOYED_LINK_HERE)**

## 🚀 Overview
Unlike heavy modern Machine Learning applications that require downloading massive multi-gigabyte models (like PyTorch, LLMs, or Transformers), this application relies on a bulletproof classic NLP algorithm called **TF-IDF (Term Frequency-Inverse Document Frequency) Cosine Similarity**. 

Because of this specific design choice, it is incredibly fast, extremely reliable, and runs instantly on almost any machine without any hardware acceleration!

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn, Scikit-learn, NLTK
- **Frontend:** Vanilla HTML, CSS, JavaScript (Premium Glassmorphism Design)

## 📁 Project Structure
- `/backend`
  - `main.py` - The FastAPI server containing the mathematical NLP logic.
  - `requirements.txt` - Python backend dependencies list.
- `/frontend`
  - `index.html` - The beautiful user web interface.
  - `style.css` - Visual styling, dynamic animations, and dark mode aesthetics.
  - `script.js` - Connects the UI to the backend API via async fetch.

## ⚙️ How to Run Locally
1. **Start the Backend server:**
   Navigate into the `/backend` folder using your terminal and run:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
2. **Open the Frontend:**
   You do not need an additional web server! Simply navigate to the frontend folder and double-click `index.html` to open it in your browser.

## 💡 How it Works
1. You paste a paragraph of information into the "Context" box.
2. You ask a natural language question.
3. The local NLP backend automatically strips out stop-words, calculates the term relevance weightings vector, computes the cosine similarity against your question, and extracts the best matching sentence for you!
