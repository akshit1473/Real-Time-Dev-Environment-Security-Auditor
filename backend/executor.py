import subprocess
import json
import time
from datetime import datetime


def run_script(script, args=None):
    start = time.time()

    cmd = ["bash", script, "--json"]
    if args:
        cmd.extend(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    duration = int((time.time() - start) * 1000)

    if result.returncode != 0:
        return {
            "execution": {
                "status": "error",
                "time_ms": duration
            },
            "meta": {
                "script": script,
                "timestamp": datetime.utcnow().isoformat()
            },
            "error": result.stderr
        }

    try:
        parsed = json.loads(result.stdout)

        return {
            "execution": {
                "status": "success",
                "time_ms": duration
            },
            "meta": {
                "script": script,
                "timestamp": datetime.utcnow().isoformat()
            },
            "data": parsed.get("data", parsed)
        }

    except:
        return {
            "execution": {
                "status": "parse_error",
                "time_ms": duration
            },
            "meta": {
                "script": script,
                "timestamp": datetime.utcnow().isoformat()
            },
            "raw": result.stdout
        }
