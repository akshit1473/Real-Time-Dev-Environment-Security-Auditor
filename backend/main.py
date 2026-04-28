from fastapi import FastAPI
from executor import run_script
from risk_engine import analyze_risk

app = FastAPI()


@app.get("/")
def root():
    return {"status": "working"}


# 🔍 Audit endpoint
@app.get("/api/audit/path")
def audit_path():
    raw = run_script("scripts/path_auditor.sh")
    return analyze_risk(raw)


# 🔥 Attack endpoint (only if vulnerable)
@app.get("/api/simulate/path")
def simulate_path():
    raw = run_script("scripts/path_auditor.sh")
    analysis = analyze_risk(raw)

    if not analysis["vulnerable"]:
        return {
            "status": "blocked",
            "message": "No vulnerability detected"
        }

    return run_script("scripts/path_hijack_demo.sh")


# 📊 Summary endpoint (for UI)
@app.get("/api/summary")
def summary():
    raw = run_script("scripts/path_auditor.sh")
    analysis = analyze_risk(raw)

    return {
        "overall_risk": "HIGH" if analysis["vulnerable"] else "LOW",
        "risk_score": analysis["risk_score"],
        "issues": analysis["issues"]
    }
