#!/usr/bin/env bash
# This script creates symlinks to all the executables in the latest version of all mise installed packages.

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

rm -rf ~/.local/latest
mkdir -p ~/.local/latest
cd ~/.local/latest

for d in ~/.local/share/mise/installs/*/*latest; do
    # If there is a bin folder, symlink all the executables
    if [[ -d "$d/bin" ]]; then
        for f in "$d/bin"/*; do
            # Skip if not a regular file
            if [[ ! -f "$f" ]]; then
                continue
            fi
            # Skip if not executable
            if [[ ! -x "$f" ]]; then
                continue
            fi
            # Skip cjs (CommonJS) and Python script files
            if [[ $f == *.cjs ]] || [[ $f == *.py ]]; then
                continue
            fi
            # Skip if the file name contains 1, 2, or 3 (to avoid versioned binaries)
            if [[ $f == *1 ]] || [[ $f == *2 ]] || [[ $f == *3 ]]; then
                continue
            fi
            # If there is a file with the same name in the current directory, print a warning and skip it
            if [ -e "$(basename "$f")" ]; then
                echo "Warning: $(basename "$f") already exists. Skipping $f"
                continue
            fi
            ln -s "$f" .
        done
    else
        # If there is no bin folder, symlink any executables in the root
        find -L "$d" -type f -executable -exec ln -s {} . \;
    fi
done

# Create a symlink for every python version (full and major.minor versions)
# Look for both the highest patch versions and create major.minor links in one pass
for p in ~/.local/share/mise/installs/python/*/bin/python; do
    # Extract the version from the path - works with both formats
    if [[ "$p" =~ python/([0-9]+\.[0-9]+(\.[0-9]+)?)/bin/python ]]; then
        version="${BASH_REMATCH[1]}"
        name="python${version}"

        # If there is a file with the same name in the current directory, print a warning and skip it
        if [ -e "$name" ]; then
            echo "Warning: $name already exists. Skipping $p"
            continue
        fi
        ln -s "$p" "$name"
    fi
done

cd - > /dev/null
