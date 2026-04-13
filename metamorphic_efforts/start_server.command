#!/bin/bash
# Metamorphic Efforts - Local Server (Mac)
# Double-click this file to start. Open http://localhost:8080 in browser.

cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║     Metamorphic Efforts Server       ║"
echo "  ║   http://localhost:8080              ║"
echo "  ║   Press Ctrl+C to stop               ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

if command -v python3 &> /dev/null; then
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    python -m http.server 8080
else
    echo "Error: Python not found."
    echo "Install Python 3 from https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi
