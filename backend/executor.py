def run_script(script, args=None):
    import subprocess
    import time
    import json
    from datetime import datetime

    start = time.time()

    cmd = ["bash", script]

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
    # If not JSON, treat as normal output (NOT an error)
    return {
        "execution": {
            "status": "success",
            "time_ms": duration
        },
        "meta": {
            "script": script,
            "timestamp": datetime.utcnow().isoformat()
        },
        "output": result.stdout.strip()
    }
