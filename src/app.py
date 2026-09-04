import streamlit as st
from pypdf import PdfReader
from docx import Document

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)
st.markdown("""
<style>
.main {
    padding: 2rem;
}

h1 {
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume against a job description.")

all_skills = [
    "python", "machine learning", "data analysis", "sql",
    "pandas", "numpy", "deep learning", "tensorflow",
    "pytorch", "excel", "power bi", "tableau",
    "statistics", "nlp", "scikit-learn"
]

def extract_text(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "".join(page.extract_text() or "" for page in reader.pages)

    elif name.endswith(".docx"):
        document = Document(uploaded_file)
        return " ".join(p.text for p in document.paragraphs)

    elif name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    return ""


st.header("1️⃣ Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx", "txt"]
)

st.header("2️⃣ Job Description")

job_description = st.text_area(
    "Paste Job Description",
    height=180
)

if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        resume_text = extract_text(uploaded_file).lower()
        job_text = job_description.lower()

        required_skills = [
            skill for skill in all_skills
            if skill in job_text
        ]

        matched_skills = [
            skill for skill in required_skills
            if skill in resume_text
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill not in matched_skills
        ]

        total = len(required_skills)
        matched = len(matched_skills)

        if total > 0:
            percentage = (matched / total) * 100
        else:
            percentage = 0

        st.header("3️⃣ Resume Analysis Result")

        st.metric("Resume Match", f"{percentage:.1f}%")
        st.metric("Resume Score", f"{matched}/{total}")

        st.progress(int(percentage))

        st.subheader("✅ Skills Matched")

        if matched_skills:
            for skill in matched_skills:
                st.success(skill.title())
        else:
            st.write("No matching skills found.")

        st.subheader("❌ Skills Missing")

        if missing_skills:
            for skill in missing_skills:
                st.error(skill.title())
        else:
            st.success("No required skills are missing!")

        st.subheader("💡 Resume Improvement Suggestions")

        if missing_skills:
            st.write("Consider improving these skills:")
            for skill in missing_skills:
                st.info(f"📌 {skill.title()}")
        else:
            st.success(
                "🎉 Your resume matches all required skills!"
            )

        st.subheader("📊 Final Feedback")

        if percentage >= 80:
            feedback = "Excellent match! Your resume is strongly aligned with the job."
            st.success(feedback)

        elif percentage >= 60:
            feedback = "Good match! Add some relevant skills or projects."
            st.warning(feedback)

        elif percentage >= 40:
            feedback = "Moderate match. Improve your technical skills and projects."
            st.warning(feedback)

        else:
            feedback = "Low match. Tailor your resume to the job requirements."
            st.error(feedback)

        # ---------------- DOWNLOAD REPORT ----------------

        report = f"""
AI RESUME ANALYZER REPORT
=========================

Resume Match: {percentage:.1f}%

Resume Score: {matched}/{total}

Skills Matched:
{chr(10).join(skill.title() for skill in matched_skills)}

Skills Missing:
{chr(10).join(skill.title() for skill in missing_skills)}

Final Feedback:
{feedback}
"""

        st.subheader("📥 Download Report")

        st.download_button(
            label="📥 Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )