# VibeCheck

**VibeCheck** is a web app that analyzes the overall sentiment and emotional tone of a Twitter user's recent tweets.  
It uses **FastAPI** for the backend and machine learning models for NLP analysis.

---

## Features
- 🔎 Fetches recent tweets from a given username
- 🤖 Analyzes sentiment (positive/neutral/negative) using a pre-trained model
- 😎 Detects emotions like joy, anger, sadness, etc.
- 🧠 Combines profile information and tweet analysis
- 🚀 FastAPI backend with CORS enabled for frontend integration

---

## Tech Stack
- **FastAPI** (Backend API)
- **Hugging Face Transformers** (for Sentiment + Emotion models)
- **TwitterAPI.io** (for fetching tweets)
- **Python 3.10+**

---

## How to Run Locally

1. Clone the repo:
    ```bash
    git clone https://github.com/WesLeeO/VibeCheck.git
    cd VibeCheck
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

4. Access the API at:
    ```
    http://127.0.0.1:8000/analyze/{username}
    ```

---

## Example API Usage

**Endpoint:**
