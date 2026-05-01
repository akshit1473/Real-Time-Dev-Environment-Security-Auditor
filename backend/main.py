from fastapi import FastAPI
from executor import run_script
from risk_engine import analyze_risk
from fastapi.responses import FileResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_AUDITOR_SCRIPT = os.path.join(
    BASE_DIR, "..", "scripts", "path_auditor_hackathon.sh"
)

PATH_ATTACK_SCRIPT = os.path.join(
    BASE_DIR, "..", "scripts", "path_hijack_hackathon.sh"
)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui():
    return FileResponse("../frontend/index.html")


@app.get("/")
def root():
    return {"status": "working"}


@app.get("/api/audit/path")
def audit_path():
    raw = run_script(PATH_AUDITOR_SCRIPT, ["--json"])
    return analyze_risk(raw)


@app.get("/api/simulate/attack")
def simulate_attack():
    audit = run_script(PATH_AUDITOR_SCRIPT, ["--json"])
    analysis = analyze_risk(audit)

    if not analysis.get("vulnerable"):
        return {
            "status": "blocked",
            "message": "No vulnerability detected",
            "analysis": analysis
        }

    exploit = run_script(PATH_ATTACK_SCRIPT)

    return {
        "status": exploit["execution"]["status"],
        "output": exploit.get("output") or exploit.get("data"),
        "analysis": analysis
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
