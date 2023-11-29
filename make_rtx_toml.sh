#!/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

version=${1:-$(python -V|cut -d' ' -f2)}

echo Using version: $version

echo "[tools]
python = { version='$version', virtualenv='.venv' }" > .rtx.toml
