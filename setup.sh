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

# Remind about .env for AI mode
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  For AI mode, create a .env file with:"
    echo "   echo \"ANTHROPIC_API_KEY=your_key\" > .env"
    echo "   Get key from: https://console.anthropic.com"
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
