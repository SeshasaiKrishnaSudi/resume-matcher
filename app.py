import streamlit as st
from utils import extract_text_from_pdf, analyze_resume

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="centered"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .title { font-size: 2.5rem; font-weight: 800; color: white; text-align: center; }
    .subtitle { font-size: 1rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .score-box { padding: 1.5rem; border-radius: 12px; text-align: center; font-size: 3rem; font-weight: 900; margin: 1rem 0; }
    .score-high  { background: #d4edda; color: #155724; border: 2px solid #28a745; }
    .score-mid   { background: #fff3cd; color: #856404; border: 2px solid #ffc107; }
    .score-low   { background: #f8d7da; color: #721c24; border: 2px solid #dc3545; }
    .section-card { background: black; padding: 1.2rem 1.5rem; border-radius: 10px;
                    margin: 0.8rem 0; box-shadow: 0 2px 6px rgba(0,0,0,0.07); }
    .tag { display: inline-block; background: #e8f4f8; color: #0077b6;
           padding: 4px 10px; border-radius: 20px; margin: 3px; font-size: 0.85rem; }
    .tag-missing { background: #fdecea; color: #c0392b; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="title">📄 Resume Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your resume & paste a job description — get instant AI feedback!</div>', unsafe_allow_html=True)
st.divider()

# ─── Inputs ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📎 Upload Your Resume")
    uploaded_file = st.file_uploader("PDF format only", type=["pdf"], label_visibility="collapsed")

with col2:
    st.markdown("### 💼 Paste Job Description")
    job_description = st.text_area("Job description here...", height=200, label_visibility="collapsed",
                                   placeholder="Paste the full job description here...")

st.divider()

# ─── Analyze Button ──────────────────────────────────────────────────────────
analyze_btn = st.button("🚀 Analyze My Resume", use_container_width=True, type="primary")

# ─── Results ─────────────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_file:
        st.warning("⚠️ Please upload your resume PDF.")
    elif not job_description.strip():
        st.warning("⚠️ Please paste a job description.")
    else:
        with st.spinner("🤖 AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text:
                st.error("❌ Could not read the PDF. Make sure it contains selectable text.")
            else:
                result = analyze_resume(resume_text, job_description)

        if result:
            st.success("✅ Analysis Complete!")
            st.divider()

            score = result.get("score", 0)
            if score >= 70:
                score_class = "score-high"
                emoji = "🟢"
            elif score >= 40:
                score_class = "score-mid"
                emoji = "🟡"
            else:
                score_class = "score-low"
                emoji = "🔴"

            st.markdown(f"### {emoji} Match Score")
            st.markdown(f'<div class="score-box {score_class}">{score} / 100</div>', unsafe_allow_html=True)

            st.markdown("### ✅ Matching Skills Found")
            matching = result.get("matching_skills", [])
            if matching:
                tags = " ".join([f'<span class="tag">✔ {s}</span>' for s in matching])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No strong matches found.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### ❌ Missing Keywords / Skills")
            missing = result.get("missing_skills", [])
            if missing:
                tags = " ".join([f'<span class="tag tag-missing">✘ {s}</span>' for s in missing])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No major gaps found!")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### 💡 Suggestions to Improve Your Resume")
            suggestions = result.get("suggestions", [])
            for i, tip in enumerate(suggestions, 1):
                st.markdown(f'<div class="section-card">💡 <b>Tip {i}:</b> {tip}</div>', unsafe_allow_html=True)

            summary = result.get("summary", "")
            if summary:
                st.markdown("### 📝 Overall Summary")
                st.markdown(f'<div class="section-card">{summary}</div>', unsafe_allow_html=True)

