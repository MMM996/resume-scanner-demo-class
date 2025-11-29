# app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from utils.pdf_parser import extract_text_from_pdf
from utils.scoring import score_resume

# Load environment variables
load_dotenv()
env_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Resume Scanner", layout="centered")

st.title("📄 Resume Scanner Demo")

# Input field only as fallback
user_api_key = st.text_input("Enter OpenAI API Key (leave blank to use .env)", type="password")

api_key = user_api_key if user_api_key else env_api_key

if not api_key:
    st.warning("No API key provided. Add it to .env or enter manually.")
    st.stop()

# Load job descriptions
jd_df = pd.read_csv("job_descriptions.csv")

st.subheader("Select Job Description")
jd_name = st.selectbox("Choose a JD:", jd_df["name"].tolist())

jd_selected = jd_df[jd_df["name"] == jd_name].iloc[0]
jd_text = jd_selected["description"]

st.write("### Job Description Preview")
st.info(jd_text)

# Upload resumes
uploaded_files = st.file_uploader(
    "Upload up to 5 resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 5:
    st.error("Please upload a maximum of 5 files.")
    st.stop()

if st.button("Analyze"):
    if not uploaded_files:
        st.error("Upload at least one PDF.")
        st.stop()

    results = []

    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            resume_text = extract_text_from_pdf(file)
            output = score_resume(resume_text, jd_text, api_key)

            results.append({
                "Resume Name": file.name,
                "Score": output["score"],
                "Explanation": output["explanation"]
            })

    st.success("Analysis complete!")
    st.dataframe(pd.DataFrame(results), use_container_width=True)
