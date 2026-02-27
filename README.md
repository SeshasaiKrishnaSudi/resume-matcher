# 📄 AI Resume Matcher

An AI-powered web app that compares your resume against a job description and gives you instant feedback — match score, missing skills, and tips to improve.

Built with **Streamlit** + **Google Gemini AI**.

---

## 🚀 Live Demo
> Add your Streamlit Cloud link here after deploying!

---

## ✨ Features
- 📎 Upload your Resume as a PDF
- 💼 Paste any Job Description
- 🎯 Get a Match Score (0–100)
- ✅ See matching skills found in your resume
- ❌ See missing keywords you should add
- 💡 Get 3 actionable improvement tips
- 📝 Overall AI summary of your application

---

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/) — Web UI
- [Google Gemini AI](https://makersuite.google.com/) — LLM Analysis
- [PyPDF2](https://pypdf2.readthedocs.io/) — PDF Text Extraction
- Python 3.10+

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/resume-matcher-ai.git
cd resume-matcher-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```
Get your free API key at: https://makersuite.google.com/app/apikey

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
resume-matcher-ai/
├── app.py              # Main Streamlit app
├── utils.py            # PDF reader + Gemini AI logic
├── requirements.txt    # Dependencies
├── .env.example        # API key template
├── .gitignore
└── README.md
```

---

## 🌐 Deploy on Streamlit Cloud (Free)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `GOOGLE_API_KEY` in the Secrets settings
5. Deploy! 🎉

---

## 📜 License
MIT License — free to use and modify.
