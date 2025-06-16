"""
Simple Nuitka build test for Hello World
This validates the basic Nuitka compilation process for SPIKE-1
"""

import subprocess
import sys
import os
from pathlib import Path

def build_hello_world():
    """Build hello_world.py with Nuitka"""
    print("=== Nuitka Hello World Build Test ===")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print(f"Working directory: {os.getcwd()}")
    
    # Check if Nuitka is available
    try:
        result = subprocess.run([sys.executable, "-m", "nuitka", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"Nuitka version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Nuitka not available: {e}")
        return False
    except FileNotFoundError:
        print("❌ Nuitka not found. Install with: pip install nuitka")
        return False
    
    # Build command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--main=hello_world.py",
        "--output-filename=hello_world_test",
        "--standalone",
        "--assume-yes-for-downloads",
        "--remove-output",
        "--verbose"
    ]
    
    print(f"Build command: {' '.join(cmd)}")
    
    try:
        print("Starting Nuitka compilation...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Compilation successful!")
        print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        
        # Check if executable was created
        if sys.platform == "win32":
            exe_path = backend_dir / "hello_world_test.exe"
        else:
            exe_path = backend_dir / "hello_world_test"
            
        if exe_path.exists():
            file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
            print(f"✅ Executable created: {exe_path}")
            print(f"   File size: {file_size:.2f} MB")
            
            # Test the executable
            print("Testing executable...")
            test_result = subprocess.run([str(exe_path)], 
                                       capture_output=True, text=True, timeout=30)
            
            if test_result.returncode == 0:
                print("✅ Executable test passed!")
                print("Output:", test_result.stdout)
                return True
            else:
                print(f"❌ Executable test failed with return code {test_result.returncode}")
                print("STDERR:", test_result.stderr)
                return False
        else:
            print(f"❌ Executable not found at {exe_path}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("❌ Executable test timed out")
        return False

def main():
    """Main entry point"""
    success = build_hello_world()
    
    if success:
        print("\n🎉 SPIKE-1 Hello World test PASSED!")
        print("Nuitka build environment is working correctly.")
    else:
        print("\n❌ SPIKE-1 Hello World test FAILED!")
        print("Nuitka build environment needs attention.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
