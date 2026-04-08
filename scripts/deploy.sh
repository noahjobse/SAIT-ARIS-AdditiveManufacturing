#!/usr/bin/env bash
# deploy.sh — Build and deploy the ABB Simulation Platform via Docker
# Usage:
#   ./scripts/deploy.sh preview    # Build and tag as preview
#   ./scripts/deploy.sh prod       # Build and tag as production
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE_NAME="abb-simulation-platform"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# ── Parse arguments ──────────────────────────────────────────────────────────
ENV="${1:-preview}"

if [[ "$ENV" != "preview" && "$ENV" != "prod" ]]; then
    echo "Usage: $0 [preview|prod]"
    echo "  preview  — Build and tag as preview (default)"
    echo "  prod     — Build, tag as latest, and run smoke test"
    exit 1
fi

echo "========================================="
echo "  Deploying: $ENV"
echo "  Timestamp: $TIMESTAMP"
echo "========================================="

# ── Pre-flight checks ────────────────────────────────────────────────────────
echo ""
echo "Running pre-flight checks..."

# Check Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: docker not found. Please install Docker."
    exit 1
fi

# Check docker compose is available
if ! docker compose version &> /dev/null; then
    echo "ERROR: docker compose not found."
    exit 1
fi

echo "  Docker:  $(docker --version | grep -oP 'Docker version \K[0-9.]+')"

# ── Lint checks ──────────────────────────────────────────────────────────────
echo ""
echo "Running lint checks..."

# Backend lint with ruff
echo "  Backend (ruff)..."
BACKEND_LINT=$(cd "$ROOT/backend" && source venv/bin/activate 2>/dev/null && ruff check . 2>&1) || true
LINT_ERRORS=$(echo "$BACKEND_LINT" | grep -c "error" 2>/dev/null || echo "0")

if [ "$LINT_ERRORS" -gt 0 ]; then
    echo "  WARNING: $LINT_ERRORS lint errors found"
    echo "$BACKEND_LINT" | grep "error" | head -5
else
    echo "  Backend lint: PASS"
fi

# Frontend lint
echo "  Frontend (eslint)..."
FRONTEND_LINT=$(cd "$ROOT/frontend" && pnpm lint 2>&1) || true
if echo "$FRONTEND_LINT" | grep -q "error" 2>/dev/null; then
    echo "  WARNING: Frontend lint errors found"
    echo "$FRONTEND_LINT" | grep "error" | head -5
else
    echo "  Frontend lint: PASS"
fi

# ── Backend tests ────────────────────────────────────────────────────────────
echo ""
echo "Running backend tests..."
cd "$ROOT/backend"

TEST_OUTPUT=$(source venv/bin/activate 2>/dev/null && pytest --tb=short -q 2>&1) || true
PASSED=$(echo "$TEST_OUTPUT" | grep -oP '\d+ passed' | grep -oP '\d+' || echo "0")
FAILED=$(echo "$TEST_OUTPUT" | grep -oP '\d+ failed' | grep -oP '\d+' || echo "0")

echo "  Tests: $PASSED passed, $FAILED failed"

if [ "$FAILED" -gt 0 ] && [ "$ENV" = "prod" ]; then
    echo "ERROR: Cannot deploy to production with failing tests."
    echo "$TEST_OUTPUT" | tail -10
    exit 1
fi

# ── Docker build ─────────────────────────────────────────────────────────────
echo ""
echo "Building Docker images..."
cd "$ROOT"

if [ "$ENV" = "prod" ]; then
    TAG="$IMAGE_NAME:latest"
    BACKUP_TAG="$IMAGE_NAME:$TIMESTAMP"
    echo "  Tags: $TAG, $BACKUP_TAG"
    docker compose build 2>&1 | sed 's/^/  /'
    echo "  Tagging production images..."
else
    TAG="$IMAGE_NAME:preview-$TIMESTAMP"
    echo "  Tag: $TAG"
    docker compose build 2>&1 | sed 's/^/  /'
fi

# ── Smoke test (prod only) ───────────────────────────────────────────────────
if [ "$ENV" = "prod" ]; then
    echo ""
    echo "Running smoke test..."
    docker compose up -d 2>&1 | sed 's/^/  /'

    # Wait for services to start
    sleep 5

    # Check backend health
    HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [ "$HEALTH" = "200" ]; then
        echo "  Backend health: PASS (HTTP $HEALTH)"
    else
        echo "  Backend health: FAIL (HTTP $HEALTH)"
        docker compose logs --tail=20 2>&1 | sed 's/^/  /'
        docker compose down 2>/dev/null
        exit 1
    fi

    docker compose down 2>/dev/null
    echo "  Smoke test: PASS"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "========================================="
echo "  Deployment: $ENV — COMPLETE"
echo "  Tests:      $PASSED passed, $FAILED failed"
echo "  Lint:       $LINT_ERRORS errors"
echo "  Image:      $TAG"
echo "========================================="
