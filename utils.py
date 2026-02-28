import os
import json
import PyPDF2
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(uploaded_file):
    try:
        import io
        bytes_data = uploaded_file.read()
        reader = PyPDF2.PdfReader(io.BytesIO(bytes_data))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        st.error(f"PDF Error: {e}")
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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content.strip()

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
            "suggestions": ["Could not parse response. Please try again."],
            "summary": "An error occurred. Please try again."
        }
    except Exception as e:
        st.error(f"Groq Error: {e}")
        return None
