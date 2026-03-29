#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Colour

PIDS=()

# ── Cleanup on exit ──────────────────────────────────────────────────────────
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
        fi
    done
    # Wait briefly for graceful shutdown, then force-kill stragglers
    sleep 1
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null
        fi
    done
    echo -e "${GREEN}All services stopped.${NC}"
}
trap cleanup EXIT INT TERM

# ── Backend setup ─────────────────────────────────────────────────────────────
echo -e "${CYAN}=== ArmStudio Dev Environment ===${NC}\n"

if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}Creating Python venv...${NC}"
    python3 -m venv backend/venv
fi

echo -e "${CYAN}Installing backend dependencies...${NC}"
backend/venv/bin/pip install -q -r backend/requirements.txt

# ── Frontend setup ────────────────────────────────────────────────────────────
echo -e "${CYAN}Installing frontend dependencies...${NC}"
(cd frontend && pnpm install --silent)

# ── Start backend ─────────────────────────────────────────────────────────────
echo -e "\n${GREEN}Starting backend (http://localhost:8000/docs)${NC}"
(cd backend && ../backend/venv/bin/uvicorn app.main:app --reload --port 8000) &
PIDS+=($!)

# ── Start frontend ────────────────────────────────────────────────────────────
echo -e "${GREEN}Starting frontend (http://localhost:3000)${NC}\n"
(cd frontend && pnpm dev --port 3000) &
PIDS+=($!)

# ── Wait for all ──────────────────────────────────────────────────────────────
wait
