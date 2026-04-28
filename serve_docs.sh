#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo
echo "========================================"
echo "  Metamorphic Efforts Docs Server"
echo "  Serving: docs/"
echo "  http://localhost:8080/Metamorphic_Efforts.html"
echo "  Press Ctrl+C to stop"
echo "========================================"
echo

if [ ! -f "docs/Metamorphic_Efforts.html" ]; then
  echo "Could not find docs/Metamorphic_Efforts.html"
  echo "Make sure the docs folder is populated first."
  exit 1
fi

python3 -m http.server 8080 -d docs
