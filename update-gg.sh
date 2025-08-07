#!/usr/bin/env bash

# update-gg.sh - Update gg AppImage to latest release
# PERMANENT SCRIPT: Downloads latest gg AppImage and updates symlinks
# Pulls from https://github.com/gulbanana/gg releases

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Configuration
APPS_DIR="$HOME/apps"
BIN_DIR="$HOME/.local/bin"
REPO="gulbanana/gg"
SYMLINK_NAME="gg"

# Check for GitHub token for API rate limiting
GITHUB_TOKEN=""
if [[ -f "$HOME/.ssh/github_releases_token" ]]; then
    GITHUB_TOKEN=$(cat "$HOME/.ssh/github_releases_token")
fi

# Error handling function
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Function to get latest release info
get_latest_release() {
    local release_data
    local curl_cmd
    
    echo "Fetching latest release information..." >&2
    
    if [[ -n "$GITHUB_TOKEN" ]]; then
        curl_cmd="curl -s -H \"Authorization: Bearer $GITHUB_TOKEN\" \"https://api.github.com/repos/$REPO/releases/latest\""
    else
        curl_cmd="curl -s \"https://api.github.com/repos/$REPO/releases/latest\""
    fi
    
    # Get the raw data first
    if ! release_data=$(eval "$curl_cmd"); then
        echo "Error: Failed to fetch release information from GitHub API" >&2
        exit 1
    fi
    
    # Clean control characters
    release_data=$(echo "$release_data" | tr -d '\000-\037')
    
    # Check for API rate limit or other errors
    if echo "$release_data" | jq -e '.message' >/dev/null 2>&1; then
        local error_msg=$(echo "$release_data" | jq -r '.message')
        echo "Error: GitHub API error: $error_msg" >&2
        exit 1
    fi
    
    echo "$release_data"
}

# Function to find AppImage download URL
get_appimage_url() {
    local release_data="$1"
    local download_url
    
    echo "Searching for AppImage in release assets..." >&2
    
    # Debug: Show what we're working with
    if [[ "${TRACE-0}" == "1" ]]; then
        echo "Release data length: $(echo "$release_data" | wc -c)" >&2
        echo "Assets found: $(echo "$release_data" | jq '.assets | length' 2>/dev/null || echo "jq failed")" >&2
    fi
    
    # Look for gg_*_amd64.AppImage in the assets
    if ! download_url=$(echo "$release_data" | jq -r '.assets[] | select(.name | test("gg_.*_amd64\\.AppImage$")) | .browser_download_url' 2>/dev/null | head -n1); then
        echo "Error: jq failed to parse release data" >&2
        exit 1
    fi
    
    if [[ -z "$download_url" || "$download_url" == "null" ]]; then
        echo "Error: Could not find gg_*_amd64.AppImage in the latest release" >&2
        exit 1
    fi
    
    echo "$download_url"
}

# Function to extract version from filename
get_version_from_url() {
    local url="$1"
    local filename=$(basename "$url")
    
    # Extract version from gg_X.Y.Z_amd64.AppImage
    if [[ "$filename" =~ gg_([0-9]+\.[0-9]+\.[0-9]+)_amd64\.AppImage ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        error_exit "Could not extract version from filename: $filename"
    fi
}

# Function to check if we already have this version
check_existing_version() {
    local version="$1"
    local target_file="$APPS_DIR/gg_${version}_amd64.AppImage"
    
    if [[ -f "$target_file" ]]; then
        echo "Version $version is already installed at $target_file"
        return 0
    else
        return 1
    fi
}

# Function to download and install AppImage
install_appimage() {
    local download_url="$1"
    local version="$2"
    local filename=$(basename "$download_url")
    local target_file="$APPS_DIR/$filename"
    local temp_file="$target_file.tmp"
    
    echo "Downloading $filename..."
    echo "URL: $download_url"
    
    # Create apps directory if it doesn't exist
    mkdir -p "$APPS_DIR"
    
    # Download the AppImage
    if ! curl -L -o "$temp_file" "$download_url"; then
        rm -f "$temp_file"
        error_exit "Failed to download AppImage from $download_url"
    fi
    
    # Verify the download
    if [[ ! -f "$temp_file" ]]; then
        error_exit "Downloaded file does not exist: $temp_file"
    fi
    
    # Check if it's a valid AppImage (basic check)
    if ! file "$temp_file" | grep -q "executable"; then
        rm -f "$temp_file"
        error_exit "Downloaded file does not appear to be an executable AppImage"
    fi
    
    # Move to final location and make executable
    mv "$temp_file" "$target_file"
    chmod +x "$target_file"
    
    echo "Installed: $target_file"
    echo "$target_file"
}

# Function to update symlink
update_symlink() {
    local appimage_path="$1"
    local symlink_path="$BIN_DIR/$SYMLINK_NAME"
    
    # Create bin directory if it doesn't exist
    mkdir -p "$BIN_DIR"
    
    # Ensure the AppImage is executable
    if [[ ! -x "$appimage_path" ]]; then
        echo "Making AppImage executable: $appimage_path"
        chmod +x "$appimage_path"
    fi
    
    # Remove existing symlink if it exists
    if [[ -L "$symlink_path" ]]; then
        echo "Removing existing symlink: $symlink_path"
        rm "$symlink_path"
    elif [[ -f "$symlink_path" ]]; then
        echo "Warning: $symlink_path exists but is not a symlink"
        read -p "Remove it and create symlink? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "$symlink_path"
        else
            echo "Error: Aborted: $symlink_path already exists and is not a symlink" >&2
            exit 1
        fi
    fi
    
    # Create new symlink
    ln -s "$appimage_path" "$symlink_path"
    echo "Created symlink: $symlink_path -> $appimage_path"
    
    # Verify the symlink works
    if ! "$symlink_path" --version >/dev/null 2>&1; then
        echo "Warning: The new gg installation may not be working properly"
    else
        echo "Installation verified successfully"
    fi
}

# Function to clean up old versions (optional)
cleanup_old_versions() {
    local current_version="$1"
    local old_files
    
    echo "Checking for old gg AppImage versions..."
    
    # Find old gg AppImages
    old_files=$(find "$APPS_DIR" -name "gg_*_amd64.AppImage" -not -name "gg_${current_version}_amd64.AppImage" 2>/dev/null || true)
    
    if [[ -n "$old_files" ]]; then
        echo "Found old versions:"
        echo "$old_files"
        read -p "Remove old versions? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "$old_files" | xargs rm -f
            echo "Old versions removed"
        fi
    else
        echo "No old versions found"
    fi
}

# Main execution
main() {
    echo "=== gg AppImage Updater ==="
    
    # Check dependencies
    for cmd in curl jq file; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            error_exit "$cmd is required but not installed"
        fi
    done
    
    # Get latest release information
    local release_data
    release_data=$(get_latest_release)
    
    # Get download URL and version
    local download_url
    download_url=$(get_appimage_url "$release_data")
    
    local version
    version=$(get_version_from_url "$download_url")
    
    echo "Latest version: $version"
    
    # Check if we already have this version
    if check_existing_version "$version"; then
        echo "Updating symlink to existing version..."
        local existing_file="$APPS_DIR/gg_${version}_amd64.AppImage"
        update_symlink "$existing_file"
    else
        # Download and install new version
        local installed_file
        installed_file=$(install_appimage "$download_url" "$version")
        
        # Update symlink
        update_symlink "$installed_file"
        
        # Offer to clean up old versions
        cleanup_old_versions "$version"
    fi
    
    echo "=== Update complete ==="
    echo "gg is now available at: $BIN_DIR/$SYMLINK_NAME"
    
    # Show version info
    if command -v "$BIN_DIR/$SYMLINK_NAME" >/dev/null 2>&1; then
        echo "Current version: $("$BIN_DIR/$SYMLINK_NAME" --version 2>/dev/null || echo "Version check failed")"
    fi
}

# Run main function
main "$@"
