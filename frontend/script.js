document.addEventListener('DOMContentLoaded', () => {
    const contextInput = document.getElementById('context');
    const questionInput = document.getElementById('question');
    const askBtn = document.getElementById('ask-btn');
    const resultContainer = document.getElementById('result-container');
    const answerText = document.getElementById('answer-text');
    const confidenceBadge = document.getElementById('confidence');
    const btnText = askBtn.querySelector('span');
    const loader = askBtn.querySelector('.loader');

    const BACKEND_URL = 'http://127.0.0.1:8000/ask';

    const getAnswer = async () => {
        const context = contextInput.value.trim();
        const question = questionInput.value.trim();

        if (!context) {
            alert('Please provide some context/reference text.');
            contextInput.focus();
            return;
        }

        if (!question) {
            alert('Please ask a question.');
            questionInput.focus();
            return;
        }

        // Setup loading state
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        askBtn.disabled = true;
        
        // Hide previous result if any
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ context, question })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch answer from backend');
            }

            const data = await response.json();

            // Display result
            answerText.textContent = data.answer;
            const confidencePercent = Math.round(data.score * 100);
            
            confidenceBadge.style.display = 'inline-block';
            confidenceBadge.textContent = `${confidencePercent}% Match`;
            
            // Adjust confidence color based on score (TF-IDF usually produces 0 to 1)
            if (data.score > 0.4) {
                confidenceBadge.style.color = '#2ea043'; // Success green
                confidenceBadge.style.background = 'rgba(46, 160, 67, 0.15)';
                confidenceBadge.style.borderColor = 'rgba(46, 160, 67, 0.3)';
            } else if (data.score > 0.15) {
                confidenceBadge.style.color = '#d29922'; // Warning yellow
                confidenceBadge.style.background = 'rgba(210, 153, 34, 0.15)';
                confidenceBadge.style.borderColor = 'rgba(210, 153, 34, 0.3)';
            } else {
                confidenceBadge.style.color = '#f85149'; // Error red
                confidenceBadge.style.background = 'rgba(248, 81, 73, 0.15)';
                confidenceBadge.style.borderColor = 'rgba(248, 81, 73, 0.3)';
            }
            
            // Animate in the result box
            setTimeout(() => {
                resultContainer.classList.remove('hidden');
            }, 100);

        } catch (error) {
            console.error('Error fetching answer:', error);
            
            // Show error in the UI
            answerText.textContent = `Error: ${error.message}`;
            confidenceBadge.style.display = 'none';
            
            resultContainer.style.borderColor = 'rgba(248, 81, 73, 0.5)';
            resultContainer.classList.remove('hidden');
            
            // Revert border color after 5 seconds
            setTimeout(() => {
                resultContainer.style.borderColor = 'rgba(88, 166, 255, 0.3)';
            }, 5000);
            
        } finally {
            // Restore button state
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            askBtn.disabled = false;
        }
    };

    askBtn.addEventListener('click', getAnswer);

    // Allow pressing Enter in the question box to submit
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            getAnswer();
        }
    });
});
