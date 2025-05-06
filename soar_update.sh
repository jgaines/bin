#!/usr/bin/env bash
# Just combines the two commands to update soar then the tools it manages
# Called from my start script

set -o errexit
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Until "soar self update" actually works, use my new check and update scripts:
check soar || update soar

soar update
