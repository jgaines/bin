#!/usr/bin/env bash

cd ~/projects/werk || exit 1

# Function to check for changes
check_for_changes() {
    # Store the current commit hash before pulling
    OLD_COMMIT=$(git rev-parse HEAD)

    # Pull the latest changes (adjust remote and branch as needed)
    git pull origin main  # Or git pull upstream develop, etc.

    # Store the new commit hash after pulling
    NEW_COMMIT=$(git rev-parse HEAD)

    # Compare the commit hashes
    if [[ "$OLD_COMMIT" != "$NEW_COMMIT" ]]; then
        return 0  # Changes were pulled
    else
        return 1  # No changes were pulled
    fi
}

check_for_changes

if [ $? -eq 0 ]; then
    echo "Changes detected, rebuilding werk"
    cargo install --path werk-cli
else
    echo "No changes detected"
fi

exit 0
