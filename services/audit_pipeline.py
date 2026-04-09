
import json
from services.openai_client import client, model
from services.scoring import compute_priority_score
from prompts import SUMMARY_PROMPT, OPPORTUNITIES_PROMPT, REPORT_PROMPT

def build_intake_text(data):
    return "\n".join([f"{k}: {v}" for k,v in data.items()])

def summarize_business(text):
    r = client.responses.create(model=model, input=[{"role":"system","content":SUMMARY_PROMPT},{"role":"user","content":text}])
    return r.output_text

def find_opportunities(summary):
    r = client.responses.create(model=model, input=[{"role":"system","content":OPPORTUNITIES_PROMPT},{"role":"user","content":summary}])
    raw = r.output_text.strip().replace("```json","").replace("```","")
    data = json.loads(raw)
    for o in data["opportunities"]:
        o["priority_score"] = compute_priority_score(o["impact_score"],o["ease_score"],o["urgency_score"],o["roi_score"])
    return sorted(data["opportunities"], key=lambda x: x["priority_score"], reverse=True)

def generate_report(summary, opps):
    opp_text = "\n".join([f"{o['title']} (Priority {o['priority_score']})" for o in opps])
    r = client.responses.create(model=model, input=[{"role":"system","content":REPORT_PROMPT},{"role":"user","content":summary+"\n"+opp_text}])
    return r.output_text
