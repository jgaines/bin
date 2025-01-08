#!/usr/bin/env bash
# This script creates symlinks to all the executables in the latest version of all mise installed packages.

set -o errexit
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

rm -rf ~/.local/latest
mkdir -p ~/.local/latest
cd ~/.local/latest
for d in ~/.local/share/mise/installs/*/latest; do
    # if there is a bin folder, symlink all the executables
    if [[ -d $d/bin ]]; then
        for f in $d/bin/*; do
            if [[ ! -f $f ]]; then
                continue
            fi
            if [[ $f == *.cjs ]] || [[ $f == *.py ]]; then
                continue
            fi
            if [[ $f == *1 ]] || [[ $f == *2 ]] || [[ $f == *3 ]]; then
                continue
            fi
            # If there is a file with the same name in the current directory, print a warning and skip it
            if [[ -e $(basename $f) ]]; then
                echo "Warning: $(basename $f) already exists in the current directory. Skipping: $f"
                continue
            fi
            ln -s $f .
        done
    else
        # if there is no bin folder, symlink any executables in the root
        find -L $d -type f -executable -exec ln -s {} \;
    fi
done
cd - > /dev/null
