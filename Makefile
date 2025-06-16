# Resume Analyzer Build System
# Cross-platform build automation

.PHONY: help setup test build clean docker-build validate

# Default target
help:
	@echo "Resume Analyzer Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  setup          - Set up development environment"
	@echo "  test           - Run build environment tests"
	@echo "  build          - Build for current platform"
	@echo "  build-windows  - Build Windows executable"
	@echo "  build-macos    - Build macOS executable"
	@echo "  docker-build   - Build using Docker containers"
	@echo "  validate       - Validate build environment"
	@echo "  clean          - Clean build artifacts"
	@echo "  help           - Show this help message"

# Development setup
setup:
ifeq ($(OS),Windows_NT)
	@echo "Setting up Windows development environment..."
	powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
else
	@echo "Setting up Unix development environment..."
	chmod +x scripts/setup.sh
	./scripts/setup.sh
endif

# Test build environment
test:
	@echo "Testing build environment..."
	cd backend && python test_build.py

# Build for current platform
build:
ifeq ($(OS),Windows_NT)
	@echo "Building for Windows..."
	cd backend && python build/nuitka_config.py
else
	@echo "Building for macOS/Linux..."
	cd backend && python build/nuitka_config.py
endif

# Platform-specific builds
build-windows:
	@echo "Building Windows executable..."
	powershell -ExecutionPolicy Bypass -File build/scripts/build_windows.ps1

build-macos:
	@echo "Building macOS executable..."
	chmod +x build/scripts/build_macos.sh
	./build/scripts/build_macos.sh

# Docker-based builds
docker-build:
	@echo "Building with Docker..."
	cd build && docker-compose --profile validate up --build validate-env

docker-build-windows:
	@echo "Building Windows executable with Docker..."
	cd build && docker-compose --profile windows up --build build-windows

docker-build-macos:
	@echo "Building macOS executable with Docker..."
	cd build && docker-compose --profile macos up --build build-macos

# Validate environment
validate:
	@echo "Validating build environment..."
	cd build && docker-compose --profile validate up --build validate-env

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/dist/
	rm -rf backend/build/
	rm -rf backend/*.exe
	rm -rf backend/resume_analyzer_backend*
	rm -rf build/output/
	rm -rf frontend/dist/
	rm -rf frontend/build/

# Install dependencies
install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd backend && python -m spacy download en_core_web_sm

# Development server
dev:
	@echo "Starting development server..."
	cd backend && python src/main.py

# Quick test build (no optimization)
quick-build:
	@echo "Quick test build..."
	cd backend && python -m nuitka --main=src/main.py --output-filename=test_build --standalone --assume-yes-for-downloads

# Full CI build
ci-build: validate test build

# Development workflow
dev-setup: setup install test
	@echo "Development environment ready!"

# Production build workflow
prod-build: clean validate build
	@echo "Production build complete!"
