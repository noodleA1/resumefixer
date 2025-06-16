"""
Quick environment test for Resume Analyzer
Tests the basic setup without complex dependencies
"""

import sys
import os
from pathlib import Path

def test_python():
    """Test Python installation"""
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    return True

def test_project_structure():
    """Test project structure"""
    required_dirs = [
        "backend",
        "backend/src", 
        "backend/build",
        "build/docker",
        "build/scripts"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
            return False
    
    return True

def test_virtual_env():
    """Test virtual environment"""
    venv_python = Path("backend/venv/Scripts/python.exe")
    if venv_python.exists():
        print(f"✅ Virtual environment: {venv_python}")
        return True
    else:
        print(f"❌ Virtual environment not found")
        return False

def main():
    """Run all tests"""
    print("=== Resume Analyzer Environment Test ===\n")
    
    tests = [
        ("Python Installation", test_python),
        ("Project Structure", test_project_structure), 
        ("Virtual Environment", test_virtual_env),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        if test_func():
            passed += 1
            print("✅ PASSED\n")
        else:
            print("❌ FAILED\n")
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Environment setup is working!")
        print("\nNext steps:")
        print("1. Test Nuitka compilation: cd backend && python build_hello_world.py")
        print("2. Test spaCy installation: cd backend && python test_build.py")
        return True
    else:
        print("❌ Environment needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
