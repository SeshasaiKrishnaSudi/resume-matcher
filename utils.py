import os
import json
import PyPDF2
import streamlit as st

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert HR consultant and ATS specialist.
Compare the resume and job description below.
Return ONLY a valid JSON object like this:
{{
  "score": <integer from 0 to 100>,
  "matching_skills": [<up to 6 matching skills>],
  "missing_skills": [<up to 6 missing skills>],
  "suggestions": [<exactly 3 actionable suggestions>],
  "summary": "<2-3 sentence summary>"
}}
No explanation, no markdown, just JSON.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not parse AI response. Please try again."],
            "summary": "An error occurred. Please try again."
        }
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


## Step 2 — Make sure `requirements.txt` looks like this:
streamlit
google-generativeai
PyPDF2
python-dotenv