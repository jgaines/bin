#!/usr/bin/env bash
# Just combines the two commands to update and upgrade Homebrew packages

set -o errexit
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

brew update
brew upgrade
