#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# ── Setup ──────────────────────────────────────────────────────────────────
echo "=== ArmStudio Demo ==="

# Ensure Python venv exists
if [ ! -d "backend/venv" ]; then
    echo "Creating Python venv..."
    python3 -m venv backend/venv
fi

# Install Playwright if missing
if ! backend/venv/bin/python -c "import playwright" 2>/dev/null; then
    echo "Installing Playwright..."
    backend/venv/bin/pip install playwright
    backend/venv/bin/python -m playwright install chromium
fi

# ── Run ────────────────────────────────────────────────────────────────────
# Docker lifecycle + Playwright demo handled inside demo.py
backend/venv/bin/python e2e/demo.py
