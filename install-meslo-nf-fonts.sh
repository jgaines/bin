#!/usr/bin/env bash
#
# Script to download MesloLGS NF fonts for powerlevel10k and configure kitty to use them
# Source: https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#meslo-nerd-font-patched-for-powerlevel10k

set -e

FONT_DIR="$HOME/.local/share/fonts"
KITTY_CONF="$HOME/.config/kitty/kitty.conf"
DOWNLOAD_URLS=(
  "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf"
  "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf"
  "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf"
  "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf"
)

echo "=== Installing MesloLGS NF fonts for powerlevel10k ==="

# Create fonts directory if it doesn't exist
mkdir -p "$FONT_DIR"

# Download the fonts
echo "Downloading fonts..."
for url in "${DOWNLOAD_URLS[@]}"; do
    filename=$(basename "$url" | sed 's/%20/ /g')
    echo "  - $filename"
    curl -fsSL "$url" -o "$FONT_DIR/$filename"
done

# Update font cache
echo "Updating font cache..."
fc-cache -f

# Configure kitty to use the MesloLGS NF fonts
echo "Configuring kitty to use MesloLGS NF fonts..."

# Check if kitty config directory exists
if [ ! -d "$(dirname "$KITTY_CONF")" ]; then
    echo "Creating kitty config directory..."
    mkdir -p "$(dirname "$KITTY_CONF")"
fi

# Check if kitty.conf exists
if [ ! -f "$KITTY_CONF" ]; then
    echo "Creating new kitty.conf..."
    touch "$KITTY_CONF"
fi

# Check if font_family is already set in kitty.conf
if grep -q "^font_family" "$KITTY_CONF"; then
    echo "Updating existing font_family setting in kitty.conf..."
    sed -i 's/^font_family.*$/font_family MesloLGS NF/' "$KITTY_CONF"
else
    echo "Adding font_family setting to kitty.conf..."
    echo "font_family MesloLGS NF" >> "$KITTY_CONF"
fi

echo
echo "✅ All done! MesloLGS NF fonts are installed and kitty is configured."
echo "You may need to restart kitty for changes to take effect."
echo
