#!/usr/bin/env bash
# Just combines the two commands to update soar then the tools it manages

set -o errexit
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

soar self update
soar update
