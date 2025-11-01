#!/bin/bash

# srcirpt dir
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "[Top] - Building Chinese book..."
cd "$SCRIPT_DIR"
mdbook build

echo "[Sub - 1] - Building English book..."
cd "$SCRIPT_DIR"
cd en && mdbook build

echo "Build completed."
