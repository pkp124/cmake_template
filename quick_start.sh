#!/bin/bash
# Quick Start Script for ADS Testbench Development Framework

set -e

echo "======================================================================"
echo "  ADS Testbench Development Framework - Quick Start Setup"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Install package in development mode
echo "Installing package in development mode..."
pip install -e .
echo -e "${GREEN}✓${NC} Package installed"
echo ""

# Create configuration file
echo "Setting up configuration..."
if [ ! -f "config/.env" ]; then
    cp config/env.template config/.env
    echo -e "${GREEN}✓${NC} Configuration file created: config/.env"
    echo -e "${YELLOW}⚠${NC} Please edit config/.env with your ADS and AEDT paths"
else
    echo -e "${YELLOW}⚠${NC} Configuration file already exists: config/.env"
fi
echo ""

# Create directories for output
echo "Creating output directories..."
mkdir -p logs
mkdir -p output
mkdir -p workflow_output
echo -e "${GREEN}✓${NC} Output directories created"
echo ""

# Run tests
echo "Running tests..."
if pytest tests/ -v --tb=short > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} All tests passed"
else
    echo -e "${YELLOW}⚠${NC} Some tests failed (this is expected if PyAEDT is not installed)"
fi
echo ""

echo "======================================================================"
echo "  Setup Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "  1. Edit config/.env with your ADS and AEDT installation paths"
echo "  2. Review documentation in docs/getting_started.md"
echo "  3. Try examples in examples/ directory"
echo ""
echo "To activate the environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "Useful commands:"
echo "  make test       - Run tests"
echo "  make lint       - Run linters"
echo "  make format     - Format code"
echo "  make help       - Show all available commands"
echo ""
echo "Happy developing!"
echo "======================================================================"
