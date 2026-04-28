#!/usr/bin/bash

# Basic path hijack demo script that uses binary planting attack method.
echo "[*] Simulating PATH hijack...."

echo -e '#!/bin/bash\necho "PYTHON Hijacked. "' > ./python3
chmod +x ./python3
(
export PATH=.:$PATH
python3
)

rm -f ./python3





