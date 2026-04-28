from fastapi import FastAPI
from executor import run_script
from risk_engine import analyze_risk

app = FastAPI()


@app.get("/")
def root():
    return {"status": "working"}


@app.get("/api/audit/path")
def audit_path():
    raw = run_script("../scripts/path_auditor_hackathon.sh")

    if raw.get("execution", {}).get("status") != "success":
        return {"error": "Audit script failed", "details": raw}

    return analyze_risk(raw)


@app.get("/api/simulate/path")
def simulate_path():
    raw = run_script("../scripts/path_auditor_hackathon.sh")

    if raw.get("execution", {}).get("status") != "success":
        return {"error": "Audit script failed", "details": raw}

    analysis = analyze_risk(raw)

    if not analysis.get("vulnerable"):
        return {
            "status": "blocked",
            "message": "No vulnerability detected"
        }

    exploit = run_script("../scripts/path_hijack_hackathon.sh")

    return {
        "status": "executed",
        "analysis": analysis,
        "exploit_output": exploit
    }


@app.get("/api/summary")
def summary():
    raw = run_script("../scripts/path_auditor_hackathon.sh")

    if raw.get("execution", {}).get("status") != "success":
        return {"error": "Audit script failed", "details": raw}

    analysis = analyze_risk(raw)

    return {
        "overall_risk": "HIGH" if analysis.get("vulnerable") else "LOW",
        "risk_score": analysis.get("risk_score"),
        "vulnerable": analysis.get("vulnerable"),
        "issues": analysis.get("insights", [])
    }
