#!/bin/bash
set -e

echo "========================================="
echo "  ABB Simulation Platform Setup"
echo "========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 20+ from https://nodejs.org/"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm not found. Installing pnpm..."
    npm install -g pnpm
fi

echo "✓ Node.js $(node --version)"
echo "✓ Python $(python3 --version)"
echo "✓ pnpm $(pnpm --version)"
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies with pip..."
pip install -r requirements.txt

echo "✓ Backend setup complete"
cd ..
echo ""

# Frontend setup
echo "Setting up frontend..."
cd frontend

echo "Installing pnpm dependencies..."
pnpm install

echo "✓ Frontend setup complete"
cd ..
echo ""

# Success message
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "To start development:"
echo ""
echo "  Backend:"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    uvicorn app.main:app --reload"
echo ""
echo "  Frontend:"
echo "    cd frontend"
echo "    pnpm dev"
echo ""
echo "  Access:"
echo "    Frontend: http://localhost:5173"
echo "    Backend:  http://localhost:8000/docs"
echo ""
