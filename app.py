
import streamlit as st
from services.audit_pipeline import build_intake_text, summarize_business, find_opportunities, generate_report

st.set_page_config(page_title="G4187 AI Audit Agent", layout="wide")

st.title("G4187 AI Audit Agent")

with st.form("form"):
    company = st.text_input("Company Name")
    industry = st.text_input("Industry")
    bottlenecks = st.text_area("Top bottlenecks")
    submitted = st.form_submit_button("Run Audit")

if submitted:
    data = {"company":company,"industry":industry,"bottlenecks":bottlenecks}
    intake = build_intake_text(data)
    summary = summarize_business(intake)
    opps = find_opportunities(summary)
    report = generate_report(summary, opps)

    st.subheader("Summary")
    st.write(summary)
    st.subheader("Opportunities")
    st.write(opps)
    st.subheader("Report")
    st.write(report)

    st.download_button("Download Report", report, file_name="audit.md")
