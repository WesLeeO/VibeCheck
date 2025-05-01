# 💫 VibeCheck

**VibeCheck** is a web application that analyzes the overall sentiment and emotional tone of a Twitter user's recent tweets.  
It leverages **FastAPI** for the backend and state-of-the-art NLP models for real-time analysis.

🔗 **Live demo:** [wesleeo.github.io/VibeCheck](https://wesleeo.github.io/VibeCheck/)

---

## ✨ Features

- 🔎 Fetches recent tweets from any public Twitter account using **TwitterAPI.io**
- 🤖 Performs sentiment analysis (positive / neutral / negative) with pre-trained transformer models
- 😎 Detects emotions such as **joy**, **anger**, **sadness**, and more
- 🧠 Combines tweet analysis with profile metadata for deeper insights
- 🌐 Backend powered by **FastAPI**, with **CORS** enabled for frontend integration
- 🚀 Fully deployed on **Modal** — a serverless GPU-enabled platform

---

## 🧰 Tech Stack

- **FastAPI** — High-performance Python framework for serving the backend API
- **Modal** — Serverless cloud platform (GPU-enabled) used to host and scale the backend
- **Hugging Face Transformers** — Pre-trained NLP models for sentiment and emotion classification
- **PyTorch** — Deep learning engine used for model inference
- **TwitterAPI.io** — External API for fetching tweets and user profile data
- **Python 3.10+** — Core programming language for backend development

---

## 📂 Repository Structure

📂 VibeCheck/
.
├── backend
│   ├── api.py # Main API endpoints (if separate from modal)
│   ├── profile_fetcher.py # Fetches Twitter profile data
│   ├── requirements.txt  # Python dependencies
│   ├── sentiment.py  # NLP sentiment analysis
│   ├── tweet_analyzer.py # Processes tweet data
│   ├── tweet_fetcher.py # Handles Twitter API calls
│   └── vibecheck_modal.py # Modal backend
├── frontend
│   ├── dist
│   │   ├── assets
│   │   ├── index.html
│   │   └── vite.svg
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── assets
│   │   ├── App.css
│   │   ├── App.jsx # Main page
│   │   ├── index.css
│   │   └── main.jsx
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── README.md

## 🛠️ Deployment Notes

The backend is deployed using **Modal**, which provides serverless infrastructure with optional GPU acceleration.  
This allows the app to run powerful NLP pipelines on demand — without managing servers or containers.

---

Feel free to fork, contribute, or reach out with ideas! 🙌