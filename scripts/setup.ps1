# ABB Simulation Platform Setup - PowerShell
# Run with: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  ABB Simulation Platform Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

$nodeExists = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
$pythonExists = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
$poetryExists = $null -ne (Get-Command poetry -ErrorAction SilentlyContinue)
$pnpmExists = $null -ne (Get-Command pnpm -ErrorAction SilentlyContinue)

if (-not $nodeExists) {
    Write-Host "Failed: Node.js not found" -ForegroundColor Red
    exit 1
}

if (-not $pythonExists) {
    Write-Host "Failed: Python not found" -ForegroundColor Red
    exit 1
}

Write-Host "OK: Node.js $(node --version)" -ForegroundColor Green
Write-Host "OK: Python $(python --version)" -ForegroundColor Green

if (-not $poetryExists) {
    Write-Host "Installing poetry..." -ForegroundColor Yellow
    pip install poetry
}

if (-not $pnpmExists) {
    Write-Host "Installing pnpm..." -ForegroundColor Yellow
    npm install -g pnpm
}

Write-Host ""
Write-Host "Setting up backend..." -ForegroundColor Yellow

cd backend
Write-Host "Installing dependencies with poetry..." -ForegroundColor Cyan
poetry install --with dev
if ($LASTEXITCODE -ne 0) {
    Write-Host "Backend setup failed" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Backend setup complete" -ForegroundColor Green
cd ..

Write-Host ""
Write-Host "Setting up frontend..." -ForegroundColor Yellow

cd frontend
Write-Host "Installing dependencies with pnpm..." -ForegroundColor Cyan
pnpm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend setup failed" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Frontend setup complete" -ForegroundColor Green
cd ..

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start development:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend:" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  poetry run uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Frontend:" -ForegroundColor Cyan
Write-Host "  cd frontend" -ForegroundColor White
Write-Host "  pnpm dev" -ForegroundColor White
Write-Host ""
Write-Host "Access:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
