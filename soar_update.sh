#!/usr/bin/env bash
# Just combines the two commands to update soar then the tools it manages

set -o errexit
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Until "soar self update" actually works, we need to do this:
curl -fsSL https://soar.qaidvoid.dev/install.sh | sh
soar update
