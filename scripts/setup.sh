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

echo "✓ Node.js $(node --version)"
echo "✓ Python $(python3 --version)"
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

echo "Installing Python dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "✓ Backend setup complete"
echo ""

# Frontend setup
echo "Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install --silent
else
    echo "✓ node_modules already exists (skipping npm install)"
fi

echo "✓ Frontend setup complete"
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
echo "    npm run dev"
echo ""
echo "  Access:"
echo "    Frontend: http://localhost:5173"
echo "    Backend:  http://localhost:8000/docs"
echo ""
