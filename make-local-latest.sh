#!/usr/bin/env bash
# This script creates symlinks to all the executables in the latest version of all installed packages.
rm -rf ~/.local/latest
mkdir -p ~/.local/latest
cd ~/.local/latest
ls -L ~/.local/share/mise/installs/**/latest/bin/* | grep -vE '\.cjs|\.py|[1-3]' | xargs -I {} ln -s {} .
cd -
