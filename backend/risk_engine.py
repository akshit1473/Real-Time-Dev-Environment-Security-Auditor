def analyze_risk(raw):

    if raw.get("execution", {}).get("status") != "success":
        return {
            "risk_score": 0,
            "vulnerable": False,
            "issues": [],
            "error": "execution_failed"
        }

    data = raw.get("data", {})

    # Handle both formats
    issues = data.get("issues") or raw.get("issues") or []

    score = 0

    for issue in issues:
        if issue.startswith("CRITICAL"):
            score += 3
        elif issue.startswith("WARN"):
            score += 1

    return {
        "risk_score": min(score, 10),
        "vulnerable": score > 0,
        "issues": issues
    }
