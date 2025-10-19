#!/usr/bin/env python3
"""
Simple test script to verify package structure without requiring dependencies
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_package_structure():
    """Test that the package structure is correct"""
    print("Testing package structure...")
    
    # Test main package import
    try:
        import talkscriber
        print("✓ Main package imports successfully")
        print(f"  Version: {talkscriber.__version__}")
        print(f"  Author: {talkscriber.__author__}")
    except ImportError as e:
        print(f"✗ Failed to import main package: {e}")
        return False
    
    # Test that we can access the classes (even if they can't be instantiated)
    try:
        from talkscriber.stt import TranscriptionClient, Client
        print("✓ Live transcription classes accessible")
    except ImportError as e:
        if "dependencies are not installed" in str(e) or "Required dependencies" in str(e):
            print("✓ Live transcription classes (dependencies not installed - expected)")
        else:
            print(f"✗ Failed to import live transcription classes: {e}")
            return False
    
    try:
        from talkscriber.tts import TalkScriberTTSClient
        print("✓ TTS class accessible")
    except ImportError as e:
        if "dependencies are not installed" in str(e) or "Required dependencies" in str(e):
            print("✓ TTS class (dependencies not installed - expected)")
        else:
            print(f"✗ Failed to import TTS class: {e}")
            return False
    
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "setup.py",
        "pyproject.toml",
        "MANIFEST.in",
        "README.md",
        "LICENSE.md",
        "talkscriber/__init__.py",
        "talkscriber/live/__init__.py",
        "talkscriber/live/client.py",
        "talkscriber/live/cli.py",
        "talkscriber/tts/__init__.py",
        "talkscriber/tts/client.py",
        "talkscriber/tts/cli.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def test_setup_py():
    """Test that setup.py can be parsed"""
    print("\nTesting setup.py...")
    
    try:
        # Test that setup.py can be executed
        import subprocess
        result = subprocess.run([sys.executable, "setup.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ setup.py can be executed")
            return True
        else:
            print(f"✗ setup.py execution failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ setup.py test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Talkscriber Package Structure Test")
    print("==================================")
    
    tests = [
        test_file_structure,
        test_package_structure,
        test_setup_py,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print("Test Results:")
    print(f"Files structure: {'PASS' if results[0] else 'FAIL'}")
    print(f"Package imports: {'PASS' if results[1] else 'FAIL'}")
    print(f"Setup.py: {'PASS' if results[2] else 'FAIL'}")
    
    if all(results):
        print("\n🎉 All tests passed! Package structure is correct.")
        print("\nTo install the package in development mode:")
        print("pip install -e .")
        print("\nTo build the package:")
        print("python -m build")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
