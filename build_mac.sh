#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
BUILD_DIR="$PROJECT_DIR/build"
OUTPUT_DIR="$PROJECT_DIR/release"

if [[ "$(uname -s)" != "Darwin" ]]; then
    printf 'Error: this script must be run on macOS.\n' >&2
    exit 1
fi

if [[ -x "$PROJECT_DIR/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
else
    printf 'Error: Python 3 was not found. Install Python 3 and try again.\n' >&2
    exit 1
fi

if ! "$PYTHON" -m PyInstaller --version >/dev/null 2>&1; then
    printf 'Error: PyInstaller is missing from %s.\n' "$PYTHON" >&2
    printf 'Install it with: %s -m pip install pyinstaller\n' "$PYTHON" >&2
    exit 1
fi

if ! command -v hdiutil >/dev/null 2>&1; then
    printf 'Error: hdiutil is required to create the disk image.\n' >&2
    exit 1
fi

mkdir -p "$BUILD_DIR" "$OUTPUT_DIR"

"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    --windowed \
    --name GlanceAway \
    --distpath "$OUTPUT_DIR" \
    --workpath "$BUILD_DIR/pyinstaller" \
    --specpath "$BUILD_DIR" \
    "$PROJECT_DIR/app.py"

hdiutil create \
    -volname GlanceAway \
    -srcfolder "$OUTPUT_DIR/GlanceAway.app" \
    -ov \
    -format UDZO \
    "$OUTPUT_DIR/GlanceAway.dmg"

printf '\nCreated: %s\n' "$OUTPUT_DIR/GlanceAway.dmg"
