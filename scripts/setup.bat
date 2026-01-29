@echo off
REM ABB Simulation Platform Setup - Batch File
REM Run from project root: scripts\setup.bat

setlocal enabledelayedexpansion

echo.
echo =========================================
echo   ABB Simulation Platform Setup
echo =========================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 20+ from https://nodejs.org/
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i

echo [OK] Node.js %NODE_VERSION%
echo [OK] Python %PYTHON_VERSION%

REM Check for poetry
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Installing poetry...
    call pip install poetry
    where poetry >nul 2>nul
    if %errorlevel% neq 0 (
        echo [WARN] poetry may require restarting CMD
    ) else (
        echo [OK] poetry installed
    )
) else (
    for /f "tokens=*" %%i in ('poetry --version') do echo [OK] %%i
)

REM Check for pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Installing pnpm...
    call npm install -g pnpm
    where pnpm >nul 2>nul
    if %errorlevel% neq 0 (
        echo [WARN] pnpm may require restarting PowerShell or CMD
    ) else (
        echo [OK] pnpm installed
    )
) else (
    for /f "tokens=*" %%i in ('pnpm --version') do echo [OK] pnpm %%i
)

echo.

REM Backend setup
echo Setting up backend...
cd backend

echo Installing Python dependencies with poetry...
call poetry install --with dev

if %errorlevel% neq 0 (
    echo [ERROR] Backend setup failed
    cd ..
    pause
    exit /b 1
)

echo [OK] Backend setup complete
cd ..
echo.

REM Frontend setup
echo Setting up frontend...
cd frontend

echo Installing pnpm dependencies...
call pnpm install

if %errorlevel% neq 0 (
    echo [ERROR] Frontend setup failed
    cd ..
    pause
    exit /b 1
)

echo [OK] Frontend setup complete
cd ..
echo.

REM Success message
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo To start development:
echo.
echo   Backend:
echo     cd backend
echo     poetry run uvicorn app.main:app --reload
echo.
echo   Frontend:
echo     cd frontend
echo     pnpm dev
echo.
echo   Access:
echo     Frontend: http://localhost:5173
echo     Backend:  http://localhost:8000/docs
echo.

pause
