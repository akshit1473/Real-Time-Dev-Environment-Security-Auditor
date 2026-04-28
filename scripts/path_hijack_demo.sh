#!/usr/bin/bash

set -e   #exits on error. 

# Basic path hijack demo script that uses binary planting attack method.

echo "[*] Simulating PATH hijack using Binary Planting"

# Check if python3 exists
command -v python3 >/dev/null 2>&1 || {
    echo "python3 not found!, demo may not behave as expected"
    exit 1
}

echo "Original python3 location:"
which python3

#creating the malicious library 
echo -e '#!/bin/bash\necho "PYTHON EXECUTION HIJACKED."' > ./python3
chmod +x ./python3

echo "Entering isolated environment (hijack simulation)..."

(
export PATH=.:$PATH

echo "Hijacked python3 location:"
which python3

echo "executing python3.."
python3
)

rm -f ./python3

echo "DEMO COMPLETE."





