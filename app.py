import streamlit as st
from resume_parser import extract_text_from_pdf
from ats_score import analyze_resume

st.set_page_config(page_title="AI ATS Resume Analyzer",layout="wide")

st.title("🤖 AI ATS Resume Analyzer")

col1,col2 = st.columns(2)

with col1:
    jd = st.text_area("Job Description",height=250)

with col2:
    resume = st.file_uploader("Upload Resume (PDF)",type=["pdf"])


if st.button("Analyze Resume"):

    if resume and jd:

        resume_text = extract_text_from_pdf(resume)

        result = analyze_resume(resume_text,jd)

        st.markdown("---")

        st.subheader("📊 ATS Score")

        st.metric("Overall ATS Score",f"{result['ats_score']}%")

        st.progress(result["ats_score"]/100)

        c1,c2,c3 = st.columns(3)

        c1.metric("Skill Match",f"{result['skill_score']}%")
        c2.metric("Keyword Density",f"{result['keyword_score']}%")
        c3.metric("Resume Structure",f"{result['structure_score']}%")

        if result["ats_score"] > 75:
            st.success("High chance of passing ATS")
        elif result["ats_score"] > 50:
            st.warning("Moderate chance of passing ATS")
        else:
            st.error("Low chance of passing ATS")

        st.markdown("---")

        st.subheader("🧠 Extracted Resume Skills")

        cols = st.columns(5)

        for i,skill in enumerate(result["resume_skills"]):
            cols[i % 5].markdown(
                f"<div style='background:#16a34a;padding:6px;border-radius:6px;text-align:center'>{skill}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        st.subheader("✅ Matched Skills")

        if result["matched"]:
            st.success(", ".join(result["matched"]))
        else:
            st.warning("No skills matched")

        st.subheader("⚠ Missing Skills")

        if result["missing"]:
            st.error(", ".join(result["missing"]))
        else:
            st.success("No missing skills")

        st.markdown("---")

        st.subheader("📈 Suggestions")

        suggestions=[]

        if result["missing"]:
            suggestions.append(
                "Add missing skills if relevant: " +
                ", ".join(result["missing"])
            )

        suggestions.append(
            "Mention skills inside projects and experience sections"
        )

        suggestions.append(
            "Repeat key skills naturally across the resume"
        )

        for tip in suggestions:
            st.write("•",tip)