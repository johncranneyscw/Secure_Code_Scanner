#!/bin/bash

echo "=============================================="
echo "  Security Scanner v2.0 - Installation"
echo "=============================================="
echo ""

# Check Python version
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo ""
echo "To start the server, run:"
echo "  python3 app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:8080"
echo ""
echo "For quick start guide, see: QUICKSTART.md"
echo "For full documentation, see: README.md"
echo ""
