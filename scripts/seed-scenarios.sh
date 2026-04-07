#!/usr/bin/env bash
# seed-scenarios.sh — Upload sample RAPID programs and obstacles to the running API
# Usage:
#   ./scripts/seed-scenarios.sh                # Seed all scenarios
#   ./scripts/seed-scenarios.sh --rapid-only   # Seed only RAPID programs
#   ./scripts/seed-scenarios.sh --check        # Just verify API is reachable
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURES="$ROOT/backend/tests/fixtures/rapid"
API_BASE="${API_URL:-http://localhost:8000}"

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TOTAL=0
SUCCESS=0
FAILED=0

log_ok()   { echo -e "  ${GREEN}OK${NC}   $1"; }
log_fail() { echo -e "  ${RED}FAIL${NC} $1"; }
log_info() { echo -e "  ${YELLOW}INFO${NC} $1"; }

# ── Parse arguments ──────────────────────────────────────────────────────────
MODE="${1:---all}"

# ── API health check ────────────────────────────────────────────────────────
echo "========================================="
echo "  Scenario Seeder"
echo "  API: $API_BASE"
echo "========================================="
echo ""
echo "Checking API health..."

HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/health" 2>/dev/null || echo "000")
if [ "$HEALTH" != "200" ]; then
    echo -e "${RED}ERROR:${NC} API not reachable at $API_BASE (HTTP $HEALTH)"
    echo "Start the backend first: ./start.sh"
    exit 1
fi
log_ok "API is healthy"

if [ "$MODE" = "--check" ]; then
    echo "Health check passed. Exiting."
    exit 0
fi

# ── Seed RAPID programs ─────────────────────────────────────────────────────
echo ""
echo "Uploading RAPID programs..."

# Find all .mod fixture files and upload each one
for RAPID_FILE in "$FIXTURES"/*.mod; do
    FILENAME=$(basename "$RAPID_FILE")
    TOTAL=$((TOTAL + 1))

    # Upload via the /api/upload/rapid endpoint
    RESPONSE=$(curl -s -w "\n%{http_code}" \
        -X POST "$API_BASE/api/upload/rapid" \
        -F "file=@$RAPID_FILE" 2>/dev/null)

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
        # Extract procedure count using grep and awk
        PROC_COUNT=$(echo "$BODY" | grep -oP '"procedures"\s*:\s*\[' | wc -l || echo "?")
        log_ok "$FILENAME (HTTP $HTTP_CODE)"
        SUCCESS=$((SUCCESS + 1))
    else
        log_fail "$FILENAME (HTTP $HTTP_CODE)"
        # Show error detail from response body
        ERROR_MSG=$(echo "$BODY" | grep -oP '"detail"\s*:\s*"\K[^"]+' 2>/dev/null || echo "unknown error")
        log_info "  Error: $ERROR_MSG"
        FAILED=$((FAILED + 1))
    fi
done

# ── Seed simulation runs (parse + simulate each program) ─────────────────────
if [ "$MODE" != "--rapid-only" ]; then
    echo ""
    echo "Running simulation seeds..."

    # Simulate each RAPID program by reading file content and posting to /api/simulate
    for RAPID_FILE in "$FIXTURES"/*.mod; do
        FILENAME=$(basename "$RAPID_FILE")
        TOTAL=$((TOTAL + 1))

        # Read file content into variable
        CODE=$(cat "$RAPID_FILE")

        # First parse the code
        PARSE_RESPONSE=$(curl -s -w "\n%{http_code}" \
            -X POST "$API_BASE/api/parse" \
            -H "Content-Type: application/json" \
            -d "{\"code\": $(echo "$CODE" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
            2>/dev/null)

        PARSE_CODE=$(echo "$PARSE_RESPONSE" | tail -1)
        PARSE_BODY=$(echo "$PARSE_RESPONSE" | sed '$d')

        if [ "$PARSE_CODE" = "200" ]; then
            # Count waypoints or procedures in parse output
            MOVE_COUNT=$(echo "$PARSE_BODY" | grep -oP '"type"\s*:\s*"Move' | wc -l || echo "0")
            log_ok "Parse $FILENAME — $MOVE_COUNT move commands (HTTP $PARSE_CODE)"
            SUCCESS=$((SUCCESS + 1))
        else
            log_fail "Parse $FILENAME (HTTP $PARSE_CODE)"
            ERROR_MSG=$(echo "$PARSE_BODY" | grep -oP '"detail"\s*:\s*"\K[^"]+' 2>/dev/null || echo "unknown")
            log_info "  Error: $ERROR_MSG"
            FAILED=$((FAILED + 1))
        fi
    done
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "========================================="
echo "  Seeding Complete"
echo "  Total:   $TOTAL operations"
echo "  Success: $SUCCESS"
echo "  Failed:  $FAILED"
echo "========================================="

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi
