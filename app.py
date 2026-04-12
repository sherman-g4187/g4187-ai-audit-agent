import os
import json
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()

def get_secret(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

API_KEY = get_secret("OPENAI_API_KEY")
MODEL = get_secret("OPENAI_MODEL", "gpt-4.1-mini")

st.set_page_config(page_title="G4187 Audit Chatbot", page_icon="⚙️", layout="centered")

st.title("G4187 AI Audit Chatbot")
st.caption("Answer a few questions and get your top automation opportunities.")

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

questions = [
    ("industry", "What industry are you in?"),
    ("bottlenecks", "What are your biggest bottlenecks right now?"),
    ("manual_tasks", "What repetitive manual tasks take the most time?"),
    ("delays", "Where do delays usually happen?"),
    ("goal", "What would you most like to improve in the next 90 days?"),
]

with st.sidebar:
    st.subheader("Lead info")
    name = st.text_input("Full Name", value=st.session_state.answers.get("name", ""))
    email = st.text_input("Email", value=st.session_state.answers.get("email", ""))
    company = st.text_input("Company", value=st.session_state.answers.get("company", ""))

    if name:
        st.session_state.answers["name"] = name
    if email:
        st.session_state.answers["email"] = email
    if company:
        st.session_state.answers["company"] = company

st.markdown("### Chat")

if st.session_state.step < len(questions):
    key, question = questions[st.session_state.step]
    st.write(f"**Bot:** {question}")
    answer = st.text_area("Your answer", key=f"answer_{key}")

    if st.button("Next"):
        if not st.session_state.answers.get("email"):
            st.error("Enter an email in the sidebar first.")
        elif not answer.strip():
            st.error("Please answer the question before continuing.")
        else:
            st.session_state.answers[key] = answer.strip()
            st.session_state.step += 1
            st.rerun()

else:
    st.success("Thanks — generating your audit now.")

    if st.button("Generate Audit"):
        if not API_KEY:
            st.error("Missing OPENAI_API_KEY. Add it to .env or Streamlit secrets.")
        else:
            client = OpenAI(api_key=API_KEY)

            prompt = f"""
You are the G4187 AI Audit Chatbot.

Analyze this company intake and return valid JSON only.

Company: {st.session_state.answers.get('company', '')}
Name: {st.session_state.answers.get('name', '')}
Email: {st.session_state.answers.get('email', '')}
Industry: {st.session_state.answers.get('industry', '')}
Bottlenecks: {st.session_state.answers.get('bottlenecks', '')}
Manual tasks: {st.session_state.answers.get('manual_tasks', '')}
Delays: {st.session_state.answers.get('delays', '')}
Goal: {st.session_state.answers.get('goal', '')}

Return this JSON schema:
{{
  "summary": "string",
  "top_opportunities": ["string", "string", "string"],
  "quick_win": "string",
  "estimated_roi": "string",
  "next_step": "string"
}}
"""

            response = client.responses.create(
                model=MODEL,
                input=prompt
            )

            raw = response.output_text.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(raw)

            st.markdown("## Your Audit Results")
            st.write(f"**Summary:** {data['summary']}")

            st.write("**Top Opportunities:**")
            for item in data["top_opportunities"]:
                st.write(f"- {item}")

            st.write(f"**Quick Win:** {data['quick_win']}")
            st.write(f"**Estimated ROI:** {data['estimated_roi']}")
            st.write(f"**Recommended Next Step:** {data['next_step']}")

            report = f"""
# G4187 AI Audit

Company: {st.session_state.answers.get('company', '')}
Generated for: {st.session_state.answers.get('name', '')}

## Summary
{data['summary']}

## Top Opportunities
- {data['top_opportunities'][0]}
- {data['top_opportunities'][1]}
- {data['top_opportunities'][2]}

## Quick Win
{data['quick_win']}

## Estimated ROI
{data['estimated_roi']}

## Next Step
{data['next_step']}
"""

            st.download_button(
                "Download Audit",
                data=report,
                file_name="g4187_audit_report.md",
                mime="text/markdown"
            )

            st.link_button(
                "Book a Strategy Call",
                "https://calendar.app.google/3BWPWeE4Kw8HZ86M7"
            )

            st.json(st.session_state.answers)

if st.button("Start Over"):
    st.session_state.step = 0
    st.session_state.answers = {}
    st.rerun()