#!/bin/bash
# RA Language Installer (Unix)
# Usage: chmod +x install.sh && ./install.sh

set -e

REPO_URL="https://github.com/RA-Lang/RA/releases"
VERSION="${1:-latest}"
INSTALL_DIR="${HOME}/.ra-lang"

echo "RA Language Installer"
echo "====================="

# Detect OS
case "$(uname -s)" in
    Linux*)     OS=linux;;
    Darwin*)    OS=macos;;
    *)          echo "Unsupported OS"; exit 1;;
esac

echo "Downloading RA for ${OS}..."
DOWNLOAD_URL="${REPO_URL}/download/${VERSION}/RA-${VERSION}-${OS}-x86_64.tar.gz"
TMP_FILE="/tmp/ra-lang.tar.gz"

if command -v curl &> /dev/null; then
    curl -L "$DOWNLOAD_URL" -o "$TMP_FILE"
elif command -v wget &> /dev/null; then
    wget -O "$TMP_FILE" "$DOWNLOAD_URL"
else
    echo "Neither curl nor wget found. Install one of them first."
    exit 1
fi

mkdir -p "$INSTALL_DIR"
tar -xzf "$TMP_FILE" -C "$INSTALL_DIR"

# Add to PATH if not already present
if [[ ":$PATH:" != *":$INSTALL_DIR/bin:"* ]]; then
    echo "export PATH=\"\$PATH:$INSTALL_DIR/bin\"" >> "$HOME/.bashrc"
    echo "Added to PATH in ~/.bashrc"
fi

echo ""
echo "RA Language installed to: $INSTALL_DIR"
echo "Run 'ra --version' to verify."
echo "Restart your terminal or run: source ~/.bashrc"
