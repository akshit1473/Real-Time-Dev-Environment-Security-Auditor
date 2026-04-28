def analyze_risk(raw):
    issues = raw.get("data", {}).get("issues", [])

    score = 0
    for i in issues:
        if "CRITICAL" in i:
            score += 3
        elif "WARN" in i:
            score += 1

    return {
        "risk_score": min(score, 10),
        "vulnerable": score > 0,
        "issues": issues
    }
