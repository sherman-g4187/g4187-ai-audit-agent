
def compute_priority_score(impact, ease, urgency, roi):
    return round((impact*0.4)+(ease*0.2)+(urgency*0.2)+(roi*0.2),2)
