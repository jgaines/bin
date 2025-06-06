#!/bin/bash
# Test script to verify we're in a clean bash environment

# Print the current shell
echo "Current shell executable: $0"
echo "SHELL variable: $SHELL"

# Check for bash-specific features
if [ -n "$BASH_VERSION" ]; then
    echo "✅ Running in bash version: $BASH_VERSION"
else
    echo "❌ Not running in bash"
fi

# Check for common aliases
echo -n "Checking for 'cm' alias: "
which cm 2>/dev/null && echo "❌ Found" || echo "✅ Not found"

# Count defined aliases
alias_count=$(alias 2>/dev/null | wc -l)
echo "Number of aliases defined: $alias_count"

# Check if we're using profile files
echo -n "BASH_ENV variable: "
if [ -z "$BASH_ENV" ]; then
    echo "✅ Not set"
else
    echo "❌ Set to: $BASH_ENV"
fi

# Print key environment variables
echo "PATH:"
echo "$PATH" | tr ':' '\n' | sed 's/^/  /'

echo
echo "Test complete"
