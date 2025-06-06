#!/usr/bin/env bash

set -e

# Neovim configuration directories
NVIM_DIRS=(
    "$HOME/.config/nvim"
    "$HOME/.local/share/nvim"
    "$HOME/.local/state/nvim"
    "$HOME/.cache/nvim"
)

# Function to list available configurations
list_configs() {
    echo "Available Neovim configurations:"
    
    # Get unique extensions from config directory
    for ext in $(find $HOME/.config -maxdepth 1 -name "nvim.*" -type d | sed 's|.*/nvim\.||' | sort); do
        echo "  $ext"
    done
    
    # Check if any current config exists
    local any_exists=0
    for dir in "${NVIM_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            any_exists=1
            break
        fi
    done
    
    echo
    if [[ $any_exists -eq 1 ]]; then
        echo "There is currently an active config."
    else
        echo "There is no active config."
    fi
}

# Function to backup current config with an extension
backup_config() {
    local ext=$1
    
    # Check if any of the directories exist
    local any_exists=0
    for dir in "${NVIM_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            any_exists=1
            break
        fi
    done
    
    if [[ $any_exists -eq 0 ]]; then
        echo "No active Neovim configuration found."
        return 1
    fi
    
    echo "Backing up current config as '$ext'..."
    for dir in "${NVIM_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            mv "$dir" "${dir}.$ext"
            echo "  $dir → ${dir}.$ext"
        fi
    done
}

# Function to restore config from an extension
restore_config() {
    local ext=$1
    
    # Check if config with this extension exists
    if [[ ! -d "$HOME/.config/nvim.$ext" ]]; then
        echo "Configuration '$ext' not found."
        return 1
    fi
    
    echo "Restoring config '$ext'..."
    for dir in "${NVIM_DIRS[@]}"; do
        local ext_dir="${dir}.$ext"
        if [[ -d "$ext_dir" ]]; then
            mv "$ext_dir" "$dir"
            echo "  $ext_dir → $dir"
        fi
    done
}

# Function to swap between two configs
swap_configs() {
    local backup_ext=$1
    local restore_ext=$2
    
    backup_config "$backup_ext" && restore_config "$restore_ext"
}

# Main script logic
if [[ $# -eq 0 || "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $(basename $0) [OPTIONS] [COMMAND]"
    echo
    echo "Swap between different Neovim configurations."
    echo
    echo "Options:"
    echo "  -l, --list        List available configurations"
    echo "  -h, --help        Show this help message"
    echo
    echo "Commands:"
    echo "  $(basename $0) EXTENSION               Backup current config as EXTENSION or restore EXTENSION if no config active"
    echo "  $(basename $0) BACKUP_EXT RESTORE_EXT  Backup current as BACKUP_EXT and restore RESTORE_EXT"
    exit 0
elif [[ "$1" == "--list" || "$1" == "-l" ]]; then
    list_configs
elif [[ $# -eq 1 ]]; then
    # Check if any current config exists
    any_exists=0
    for dir in "${NVIM_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            any_exists=1
            break
        fi
    done
    
    if [[ $any_exists -eq 0 ]]; then
        # No active config, try to restore the specified one
        restore_config "$1"
    else
        # Active config exists, back it up
        backup_config "$1"
    fi
elif [[ $# -eq 2 ]]; then
    swap_configs "$1" "$2"
else
    echo "Error: Invalid arguments"
    echo "Run '$(basename $0) --help' for usage information"
    exit 1
fi
