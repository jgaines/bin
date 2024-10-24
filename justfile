_default:
    @just --list

# Add justfile syntax to bat (assumes bat is installed).
justbat:
    #!/usr/bin/env bash
    bat --version || { echo "Please install bat"; exit 1; }
    mkdir -p "$(bat --config-dir)/syntaxes"
    cd "$(bat --config-dir)/syntaxes"
    git clone https://github.com/nk9/just_sublime.git
    rm 'just_sublime/Syntax/Embeddings/Python (for Just).sublime-syntax' \
        'just_sublime/Syntax/Embeddings/ShellScript (for Just).sublime-syntax'
    bat cache --build

# Remove justfile syntax from bat (assumes bat is installed).
notjustbat:
    @bat --version
    rm -rf "$(bat --config-dir)/syntaxes/just_sublime"
    bat cache --build
    