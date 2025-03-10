import subprocess
import sys
import os

def check_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_python_version():
    return sys.version_info >= (3, 6)

def main():
    print("Checking Auto Commit requirements...")
    
    # Check Python version
    if check_python_version():
        print("✅ Python 3.6+ detected")
    else:
        print("❌ Python 3.6 or higher required")
        return False
    
    # Check Git installation
    if check_git_installed():
        print("✅ Git is installed")
    else:
        print("❌ Git is not installed or not available in PATH")
        print("   Please install Git and ensure it's available in your PATH")
        return False
    
    print("\nAll requirements satisfied! You can now run Auto Commit with:")
    print("  python main.py [options]")
    print("\nFor available options, run:")
    print("  python main.py --help")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nPlease fix the issues above before running Auto Commit")
        sys.exit(1)
