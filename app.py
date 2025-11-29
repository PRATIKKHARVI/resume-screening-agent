# app.py
import streamlit as st
import pandas as pd
from parser import parse_uploaded_file
from ranker import rank_resumes
from utils import simple_clean
import base64
import io

st.set_page_config(page_title="Resume Screening Agent", layout="wide")

st.title("Resume Screening Agent")
st.markdown("""
Upload a job description (paste or upload a text file) and multiple resumes (PDF/DOCX/TXT).
The agent ranks candidates by semantic similarity and shows matched keywords & highlights.
""")

with st.expander("1) Job Description (paste or upload)"):
    jd_text = st.text_area("Paste job description here", height=200)
    jd_file = st.file_uploader("Or upload a job description file (optional)", type=["txt", "pdf", "docx"])

if jd_file and not jd_text.strip():
    _, jd_text = parse_uploaded_file(jd_file)

st.write("---")
st.header("2) Upload Resumes")
uploaded = st.file_uploader("Upload multiple resumes (PDF, DOCX, TXT).", accept_multiple_files=True, type=["pdf", "docx", "txt"])

if st.button("Rank Resumes"):
    if not jd_text or jd_text.strip() == "":
        st.error("Please provide a job description (paste or upload).")
    elif not uploaded:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Parsing resumes and computing embeddings (this uses Gemini embeddings)..."):
            resumes = []
            for f in uploaded:
                name, text = parse_uploaded_file(f)
                resumes.append({"filename": name, "text": text})

            df = rank_resumes(jd_text, resumes)
        st.success("Done ranking!")
        st.markdown("### Ranked candidates")
        st.dataframe(df[["filename", "score", "matched_keywords", "highlights"]])

        # Allow CSV download
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="ranked_candidates.csv">⬇️ Download ranked CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Show details for top candidate
        st.markdown("---")
        st.subheader("Top candidate details")
        if not df.empty:
            top = df.iloc[0]
            st.write(f"**File:** {top['filename']}")
            st.write(f"**Score:** {top['score']}")
            st.write("**Matched keywords:**", top["matched_keywords"])
            st.write("**Highlights:**")
            st.write(top["highlights"])
            with st.expander("Full parsed resume text"):
                st.write(top["raw_text"])
