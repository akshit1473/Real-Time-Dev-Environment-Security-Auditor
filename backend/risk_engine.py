def analyze_risk(raw):
    # Handle execution failure
    if raw.get("execution", {}).get("status") != "success":
        return {
            "risk_score": 0,
            "vulnerable": False,
            "issues": [],
            "error": "analysis_failed"
        }

    issues = raw.get("data", {}).get("issues", [])

    score = 0
    critical = []
    warnings = []

    for i in issues:
        if "CRITICAL" in i:
            score += 3
            critical.append(i)
        elif "WARN" in i:
            score += 1
            warnings.append(i)
        else:
            warnings.append(i)

    sorted_issues = critical + warnings

    return {
        "risk_score": min(score, 10),
        "vulnerable": score > 0,
        "issues": sorted_issues
    }
