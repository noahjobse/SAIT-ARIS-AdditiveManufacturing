#!/usr/bin/env bash
# demo.sh — SAIT ARIS TCP Tracing Demo (Playwright headed)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_URL="http://localhost:3000"
BACKEND_HEALTH="http://localhost:8000/api/health"
PYTHON="$ROOT/backend/venv/bin/python"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}=== ArmStudio — SAIT ARIS TCP Tracing Demo ===${NC}\n"

# Check if services are already running
backend_up=false
frontend_up=false
curl -sf "$BACKEND_HEALTH" > /dev/null 2>&1 && backend_up=true
curl -sf "$FRONTEND_URL" > /dev/null 2>&1 && frontend_up=true

START_PID=""
if [ "$backend_up" = false ] || [ "$frontend_up" = false ]; then
    echo -e "${YELLOW}Starting services...${NC}"
    "$ROOT/start.sh" &
    START_PID=$!

    echo -n "Waiting for backend"
    for i in $(seq 1 30); do
        curl -sf "$BACKEND_HEALTH" > /dev/null 2>&1 && break
        echo -n "."
        sleep 2
    done
    echo -e " ${GREEN}ready${NC}"

    echo -n "Waiting for frontend"
    for i in $(seq 1 20); do
        curl -sf "$FRONTEND_URL" > /dev/null 2>&1 && break
        echo -n "."
        sleep 2
    done
    echo -e " ${GREEN}ready${NC}"
else
    echo -e "${GREEN}Services already running.${NC}"
fi

echo -e "\n${CYAN}Launching Playwright demo (headed)...${NC}\n"
"$PYTHON" "$ROOT/e2e/tcp_trace_demo.py"

if [ -n "$START_PID" ]; then
    echo -e "\n${YELLOW}Stopping services...${NC}"
    kill "$START_PID" 2>/dev/null || true
fi
