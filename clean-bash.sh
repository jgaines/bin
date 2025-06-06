#!/bin/bash
# Script to run commands in a clean bash environment with minimal inherited settings

# Run the provided command with a clean environment
env -i \
    HOME="$HOME" \
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$HOME/.local/bin" \
    TERM="$TERM" \
    USER="$USER" \
    LOGNAME="$USER" \
    /bin/bash --noprofile --norc -c "$*"
