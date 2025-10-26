#!/bin/bash
# Setup script for Robot Driver Automation

echo "=================================="
echo "Robot Driver Automation - Setup"
echo "=================================="

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY for AI mode"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the basic robot driver:"
echo "  python robot_driver.py"
echo ""
echo "To run the AI-powered driver:"
echo "  python ai_robot_driver.py"
echo ""
echo "To start the API server:"
echo "  python api.py"
echo ""
echo "For AI mode, remember to set ANTHROPIC_API_KEY in .env"
echo "=================================="
