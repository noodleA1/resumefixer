# Resume Analyzer Development Environment Setup Script (Windows)
# This script sets up the development environment for the Resume Analyzer project

param(
    [switch]$SkipVenv = $false,
    [switch]$Force = $false
)

Write-Host "=== Resume Analyzer Development Setup ===" -ForegroundColor Green

$ErrorActionPreference = "Stop"

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackendDir = Join-Path $ProjectRoot "backend"

Write-Host "Project root: $ProjectRoot" -ForegroundColor Yellow
Write-Host "Backend directory: $BackendDir" -ForegroundColor Yellow

# Check Python installation
Write-Host "`nChecking Python installation..." -ForegroundColor Cyan
try {
    $PythonVersion = python --version
    Write-Host "Found: $PythonVersion" -ForegroundColor Green
    
    # Check version
    $VersionMatch = $PythonVersion -match "Python (\d+)\.(\d+)"
    if ($VersionMatch) {
        $Major = [int]$Matches[1]
        $Minor = [int]$Matches[2]
        
        if ($Major -lt 3 -or ($Major -eq 3 -and $Minor -lt 11)) {
            Write-Error "Python 3.11+ required. Found: $PythonVersion"
            exit 1
        }
    }
} catch {
    Write-Error "Python not found. Please install Python 3.11+ from https://python.org"
    exit 1
}

# Set up virtual environment
if (-not $SkipVenv) {
    Write-Host "`nSetting up Python virtual environment..." -ForegroundColor Cyan
    
    $VenvPath = Join-Path $BackendDir "venv"
    
    if (Test-Path $VenvPath) {
        if ($Force) {
            Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
            Remove-Item $VenvPath -Recurse -Force
        } else {
            Write-Host "Virtual environment already exists. Use -Force to recreate." -ForegroundColor Yellow
            $VenvExists = $true
        }
    }
    
    if (-not $VenvExists) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        Set-Location $BackendDir
        python -m venv venv
        
        if (-not (Test-Path $VenvPath)) {
            Write-Error "Failed to create virtual environment"
            exit 1
        }
    }
    
    # Activate virtual environment
    $ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
    if (Test-Path $ActivateScript) {
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        & $ActivateScript
    } else {
        Write-Error "Virtual environment activation script not found"
        exit 1
    }
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Cyan
Set-Location $BackendDir

try {
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Error "Failed to install dependencies: $_"
    exit 1
}

# Download spaCy model
Write-Host "`nDownloading spaCy model..." -ForegroundColor Cyan
try {
    python -m spacy download en_core_web_sm
    Write-Host "spaCy model downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Warning "Failed to download spaCy model. You may need to run this manually."
}

# Test the environment
Write-Host "`nTesting build environment..." -ForegroundColor Cyan
try {
    python test_build.py
    Write-Host "Environment test completed!" -ForegroundColor Green
} catch {
    Write-Warning "Environment test failed. Check the output above for issues."
}

# Create necessary directories
Write-Host "`nCreating project directories..." -ForegroundColor Cyan
$Directories = @(
    "backend/src/api",
    "backend/src/services", 
    "backend/src/models",
    "backend/tests",
    "backend/dist",
    "frontend/src",
    "frontend/public",
    "frontend/dist",
    "docs",
    "tests"
)

foreach ($Dir in $Directories) {
    $FullPath = Join-Path $ProjectRoot $Dir
    if (-not (Test-Path $FullPath)) {
        New-Item -ItemType Directory -Path $FullPath -Force | Out-Null
        Write-Host "Created: $Dir" -ForegroundColor Gray
    }
}

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. To activate the virtual environment: backend\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. To test the backend: cd backend && python src/main.py" -ForegroundColor White
Write-Host "3. To build with Nuitka: cd backend && python build/nuitka_config.py" -ForegroundColor White
Write-Host "4. To run tests: cd backend && python test_build.py" -ForegroundColor White
