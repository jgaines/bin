#!/bin/env bash

# This script creates a .mise.toml file for the specified python version
# because mise still doesn't create the virtualenv bit for you.

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# # Function to get and return chosen Python version
# choose_python_version() {
#     # Get Python versions using jq
#     python_versions=$(mise ls -iJ python | jq '.[].version' | tr -d '"')

#     # Create the pick list using select
#     PS3="Select a Python version: "

#     select version in "${python_versions[@]}"
#     do
#     if [[ $REPLY -ne 0 ]]; then
#         echo "$version"  # Return the chosen version
#         return 0         # Exit the function with success
#     fi
#     done

#     # If no valid selection is made
#     echo "No valid selection made."
#     return 1         # Exit the function with error
# }

case "$1" in
    -h|--help|help)
        echo "Usage: make_mise_toml.sh [python_version]"
        echo ""
        echo "Create a .mise.toml file for the specified python version."
        echo "Default python version to use is the currently active python."
        echo ""
        echo "Options:"
        echo "  -h, --help, help  Show this help message and exit."
        echo "  -l, --list, list  List available python versions."
        echo ""
        exit
    ;;
    -l|--list|list)
        mise ls python
        exit
esac

version=${1:-$(python -V|cut -d' ' -f2)}

echo Using version: $version

echo "[tools]
python = '$version'

[env]
_.python.venv = { path = '.venv', create = true}" > mise.toml
