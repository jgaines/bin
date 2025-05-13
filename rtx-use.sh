#!/bin/bash

# This script extracts the Python versions from tracked 
# configuration files because rtx does such a lousy job of it.

# I'm pretty sure this is crap now, but I'd like to write something that can
# scan for and find all rtx/mise files (including the legacy ones like
# .python-version) then either return a list of python versions and their
# counts, or various other formats that will allow me to analyze python usage
# across all my projects.

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

language=python

cd ${HOME}/.local/share/rtx/tracked-config-files

# Find and extract Python versions from tracked configuration files
grep "$language" $(find . -type f -print | xargs realpath) | awk -v LANG="$language" '
BEGIN {
  # Define field separator
  FS = ":"
}

# Match lines containing target language
/"'"LANG"'"'/ {
  # Extract version number
  if ($3 ~ /version=/) {
    version = gensub(/.*=\'([^\']+)\'.*$/, "\\1", 1, $3)
  } else {
    version = $2
  }

  # Print version number
  print version
}


exit 0


grep $language $(ls | xargs realpath) | awk <<'AWKSCRIPT'
  # Define a field separator
  BEGIN { FS = ":" }

  # Match lines containing 'python'
  /python/ {
    # Extract the version number
    if ($3 ~ /version=/) {
      version = gensub(/.*='([^']+)'.*$/, "\\1", 1, $3)
    } else {
      version = $2
    }

    # Print the version number
    print version
  }
AWKSCRIPT
