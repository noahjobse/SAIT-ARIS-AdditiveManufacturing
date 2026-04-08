#!/usr/bin/env bash
# start.sh — Setup (if needed) and run backend + frontend in a single terminal
# Usage:
#   ./start.sh           # Start dev servers (auto-installs on first run)
#   ./start.sh --check   # Only run prerequisite checks, don't start servers
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── Prerequisite checks ──────────────────────────────────────────────────────
echo -e "${CYAN}=== ArmStudio Dev Environment ===${NC}\n"

prereq_check() {
  local fail=0
  echo "Checking prerequisites..."

  # Python 3.11+
  if command -v python3 &> /dev/null; then
    local py_ver
    py_ver=$(python3 --version | awk '{print $2}')
    local py_major py_minor
    py_major=$(echo "$py_ver" | cut -d. -f1)
    py_minor=$(echo "$py_ver" | cut -d. -f2)
    if [ "$py_major" -ge 3 ] && [ "$py_minor" -ge 11 ]; then
      echo -e "  ${GREEN}✓${NC} Python $py_ver"
    else
      echo -e "  ${RED}✗${NC} Python $py_ver (need 3.11+)"
      fail=1
    fi
  else
    echo -e "  ${RED}✗${NC} Python not found (need 3.11+)"
    fail=1
  fi

  # Node 20+
  if command -v node &> /dev/null; then
    local node_ver
    node_ver=$(node --version | tr -d 'v')
    local node_major
    node_major=$(echo "$node_ver" | cut -d. -f1)
    if [ "$node_major" -ge 20 ]; then
      echo -e "  ${GREEN}✓${NC} Node.js $node_ver"
    else
      echo -e "  ${RED}✗${NC} Node.js $node_ver (need 20+)"
      fail=1
    fi
  else
    echo -e "  ${RED}✗${NC} Node.js not found (need 20+)"
    fail=1
  fi

  # pnpm (auto-install if missing)
  if command -v pnpm &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} pnpm $(pnpm --version)"
  else
    echo -e "  ${YELLOW}!${NC} pnpm not found — installing via npm..."
    npm install -g pnpm
    echo -e "  ${GREEN}✓${NC} pnpm $(pnpm --version)"
  fi

  if [ "$fail" -ne 0 ]; then
    echo ""
    echo -e "${RED}Missing prerequisites. Please install them and retry.${NC}"
    exit 1
  fi
  echo ""
}

prereq_check

if [ "${1:-}" = "--check" ]; then
  echo "Prerequisite check complete."
  exit 0
fi

PIDS=()

cleanup() {
  echo -e "\n${YELLOW}Shutting down...${NC}"
  for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null
    fi
  done
  sleep 1
  for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null
    fi
  done
  echo -e "${GREEN}All services stopped.${NC}"
}
trap cleanup EXIT INT TERM

# ── Backend (FastAPI) ─────────────────────────────────────────────────────────
if [ ! -d "$ROOT/backend/venv" ]; then
  echo -e "${YELLOW}Creating Python venv...${NC}"
  python3 -m venv "$ROOT/backend/venv"
fi

echo -e "${CYAN}Installing backend dependencies...${NC}"
"$ROOT/backend/venv/bin/pip" install -q -r "$ROOT/backend/requirements.txt"

# ── Frontend (Next.js) ────────────────────────────────────────────────────────
if [ ! -d "$ROOT/frontend/node_modules" ]; then
  echo -e "${CYAN}Installing frontend dependencies...${NC}"
  (cd "$ROOT/frontend" && pnpm install --silent)
fi

# ── Start services ────────────────────────────────────────────────────────────
echo -e "\n${GREEN}Starting backend (http://localhost:8000/docs)${NC}"
(
  cd "$ROOT/backend"
  source venv/bin/activate
  PYTHONUNBUFFERED=1 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 2>&1 | \
    sed "s/^/$(printf "${RED}[backend]${NC} ")/"
) &
PIDS+=($!)

echo -e "${GREEN}Starting frontend (http://localhost:3000)${NC}\n"
(
  cd "$ROOT/frontend"
  pnpm dev --port 3000 2>&1 | sed "s/^/$(printf "${GREEN}[frontend]${NC} ")/"
) &
PIDS+=($!)

echo ""
echo "  Backend:  http://localhost:8000/docs"
echo "  Frontend: http://localhost:3000"
echo "  Press Ctrl+C to stop all"
echo ""

wait
