import streamlit as st
from utils import extract_text_from_pdf, analyze_resume

st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="centered")

st.title("📄 Resume Matcher")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📎 Upload Your Resume")
    uploaded_file = st.file_uploader("PDF format only", type=["pdf"], label_visibility="collapsed")

with col2:
    st.markdown("### 💼 Paste Job Description")
    job_description = st.text_area("Job description here...", height=200, label_visibility="collapsed",
                                   placeholder="Paste the full job description here...")

st.divider()

analyze_btn = st.button("🚀 Analyze My Resume", use_container_width=True, type="primary")

if analyze_btn:
    st.write("✅ Step 1 - Button works!")
    
    if not uploaded_file:
        st.warning("⚠️ Please upload your resume PDF.")
    elif not job_description.strip():
        st.warning("⚠️ Please paste a job description.")
    else:
        st.write("✅ Step 2 - File and job description found!")
        
        resume_text = extract_text_from_pdf(uploaded_file)
        st.write(f"✅ Step 3 - PDF text length: {len(resume_text)}")
        
        if not resume_text:
            st.error("❌ Could not read the PDF.")
        else:
            st.write("✅ Step 4 - Sending to Gemini...")
            result = analyze_resume(resume_text, job_description)
            st.write(f"✅ Step 5 - Result: {result}")