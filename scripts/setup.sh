#!/bin/bash
# Resume Analyzer Development Environment Setup Script (Unix/macOS)
# This script sets up the development environment for the Resume Analyzer project

set -e  # Exit on any error

SKIP_VENV=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--skip-venv] [--force]"
            exit 1
            ;;
    esac
done

echo "=== Resume Analyzer Development Setup ==="

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo "Project root: $PROJECT_ROOT"
echo "Backend directory: $BACKEND_DIR"

# Check Python installation
echo ""
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.11+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Check version
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Error: Python 3.11+ required. Found: $PYTHON_VERSION"
    exit 1
fi

# Set up virtual environment
if [ "$SKIP_VENV" = false ]; then
    echo ""
    echo "Setting up Python virtual environment..."
    
    VENV_PATH="$BACKEND_DIR/venv"
    
    if [ -d "$VENV_PATH" ]; then
        if [ "$FORCE" = true ]; then
            echo "Removing existing virtual environment..."
            rm -rf "$VENV_PATH"
        else
            echo "Virtual environment already exists. Use --force to recreate."
            VENV_EXISTS=true
        fi
    fi
    
    if [ "$VENV_EXISTS" != true ]; then
        echo "Creating virtual environment..."
        cd "$BACKEND_DIR"
        python3 -m venv venv
        
        if [ ! -d "$VENV_PATH" ]; then
            echo "Error: Failed to create virtual environment"
            exit 1
        fi
    fi
    
    # Activate virtual environment
    ACTIVATE_SCRIPT="$VENV_PATH/bin/activate"
    if [ -f "$ACTIVATE_SCRIPT" ]; then
        echo "Activating virtual environment..."
        source "$ACTIVATE_SCRIPT"
    else
        echo "Error: Virtual environment activation script not found"
        exit 1
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
cd "$BACKEND_DIR"

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt

echo "Dependencies installed successfully!"

# Download spaCy model
echo ""
echo "Downloading spaCy model..."
if python3 -m spacy download en_core_web_sm; then
    echo "spaCy model downloaded successfully!"
else
    echo "Warning: Failed to download spaCy model. You may need to run this manually."
fi

# Test the environment
echo ""
echo "Testing build environment..."
if python3 test_build.py; then
    echo "Environment test completed!"
else
    echo "Warning: Environment test failed. Check the output above for issues."
fi

# Create necessary directories
echo ""
echo "Creating project directories..."
DIRECTORIES=(
    "backend/src/api"
    "backend/src/services"
    "backend/src/models"
    "backend/tests"
    "backend/dist"
    "frontend/src"
    "frontend/public"
    "frontend/dist"
    "docs"
    "tests"
)

for DIR in "${DIRECTORIES[@]}"; do
    FULL_PATH="$PROJECT_ROOT/$DIR"
    if [ ! -d "$FULL_PATH" ]; then
        mkdir -p "$FULL_PATH"
        echo "Created: $DIR"
    fi
done

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. To activate the virtual environment: source backend/venv/bin/activate"
echo "2. To test the backend: cd backend && python src/main.py"
echo "3. To build with Nuitka: cd backend && python build/nuitka_config.py"
echo "4. To run tests: cd backend && python test_build.py"
