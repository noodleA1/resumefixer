"""
Simple Hello World test for Nuitka compilation
This is the minimal test for SPIKE-1
"""

import sys
import platform

def main():
    print("=== Resume Analyzer Backend - Hello World ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    # Test basic imports
    try:
        import json
        print("✅ JSON module working")
    except ImportError:
        print("❌ JSON module failed")
        return False
    
    try:
        import os
        print("✅ OS module working")
    except ImportError:
        print("❌ OS module failed")
        return False
    
    try:
        import pathlib
        print("✅ Pathlib module working")
    except ImportError:
        print("❌ Pathlib module failed")
        return False
    
    print("🎉 Hello World test completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
