#!/bin/env bash

# This script creates a .envrc file for automatic Python virtual environment
# creation and loadingthe specified python version
# because mise still doesn't populate the virtualenv for you.

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Check for an argument
if [[ $# -gt 1 ]]; then
    case "$1" in
        -h|--help|help)
            echo "Usage: make_envrc.sh [python_version]"
            echo ""
            echo "Create a .envrc file to create and populate a local Python virtualenv."
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

    # If a version specified, call mise use with it
    mise use python@$1
fi

version=${1:-$(python -V|cut -d' ' -f2)}

echo Using version: $version

# If pyproject.toml doesn't exist, ask the user if they plan to create one.
if [[ ! -f pyproject.toml ]]; then
    # Use find to search for a requirements.txt file
    requirements=$(find . -name requirements.txt)
    if [[ -n "$requirements" ]]; then
        uvcmd="uv venv && uv pip install -r $requirements"
    else
        read -p "pyproject.toml not found. Do you plan to create one? [y/N] " create_pyproject
        if [[ "${create_pyproject,,}" == "y" ]]; then
            uvcmd="uv sync"
        else
            uvcmd="uv venv"
        fi
    fi
else
    uvcmd="uv sync"
fi

echo "$uvcmd
source .venv/bin/activate
unset PS1" > .envrc
