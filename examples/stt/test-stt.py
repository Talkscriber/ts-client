#!/usr/bin/env python3
"""
Test script for Talkscriber STT (Speech-to-Text) client
"""

import os
import sys
import time
import signal
from talkscriber.stt import TranscriptionClient

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nStopping transcription...")
    sys.exit(0)

def test_stt_import():
    """Test that STT classes can be imported"""
    print("Testing STT imports...")
    try:
        from talkscriber.live import TranscriptionClient, Client
        print("✓ STT classes imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import STT classes: {e}")
        return False

def test_stt_instantiation():
    """Test that STT client can be instantiated"""
    print("\nTesting STT client instantiation...")
    
    # Check if API key is set
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  TALKSCRIBER_API_KEY environment variable not set")
        print("   Set it with: export TALKSCRIBER_API_KEY='your_api_key_here'")
        print("   Get your API key from: https://app.talkscriber.com")
        return False
    
    try:
        # Test basic instantiation
        client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=api_key,
            language="en"
        )
        print("✓ TranscriptionClient instantiated successfully")
        
        # Test with different configurations
        multilingual_client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=api_key,
            multilingual=True
        )
        print("✓ Multilingual TranscriptionClient instantiated")
        
        translation_client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=api_key,
            language="es",  # Spanish
            translate=True  # Translate to English
        )
        print("✓ Translation TranscriptionClient instantiated")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to instantiate STT client: {e}")
        return False

def test_microphone_transcription():
    """Test live microphone transcription"""
    print("\nTesting live microphone transcription...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping microphone test - no API key")
        return False
    
    try:
        client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=api_key,
            language="en",
            enable_turn_detection=True
        )
        
        print("🎤 Starting live transcription from microphone...")
        print("   Speak into your microphone and watch for transcription results")
        print("   Press Ctrl+C to stop")
        print("-" * 50)
        
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start transcription
        client()
        
    except KeyboardInterrupt:
        print("\n✓ Microphone transcription stopped by user")
        return True
    except Exception as e:
        print(f"✗ Microphone transcription failed: {e}")
        return False

def test_file_transcription():
    """Test file-based transcription"""
    print("\nTesting file-based transcription...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping file test - no API key")
        return False
    
    # Check for test audio file
    test_files = [
        "test_audio.wav",
        "test_audio.mp3",
        "sample.wav",
        "sample.mp3"
    ]
    
    audio_file = None
    for file in test_files:
        if os.path.exists(file):
            audio_file = file
            break
    
    if not audio_file:
        print("⚠️  No test audio file found. Looking for:")
        for file in test_files:
            print(f"   - {file}")
        print("   Place an audio file in the current directory to test file transcription")
        return False
    
    try:
        client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=api_key,
            language="en"
        )
        
        print(f"📁 Transcribing audio file: {audio_file}")
        print("-" * 50)
        
        # Transcribe the file
        client(audio_file)
        
        print("✓ File transcription completed")
        return True
        
    except Exception as e:
        print(f"✗ File transcription failed: {e}")
        return False

def test_cli_tools():
    """Test CLI tools"""
    print("\nTesting CLI tools...")
    
    import subprocess
    import shutil
    
    # Find the correct CLI tool path
    cli_path = shutil.which('talkscriber-stt')
    if not cli_path:
        print("✗ STT CLI tool not found in PATH")
        return False
    
    # Test STT CLI help
    try:
        result = subprocess.run([
            cli_path, 
            '--help'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✓ STT CLI tool available")
            return True
        else:
            print("✗ STT CLI tool failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ STT CLI test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Talkscriber STT Client Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Run tests
    tests = [
        ("Import Test", test_stt_import),
        ("Instantiation Test", test_stt_instantiation),
        ("CLI Tools Test", test_cli_tools),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Interactive tests (only if API key is available)
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if api_key:
        print("API key found - running interactive tests...")
        print()
        
        # Ask user which interactive test to run
        print("Choose an interactive test:")
        print("1. Microphone transcription")
        print("2. File transcription")
        print("3. Skip interactive tests")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                test_microphone_transcription()
            elif choice == "2":
                test_file_transcription()
            elif choice == "3":
                print("Skipping interactive tests")
            else:
                print("Invalid choice, skipping interactive tests")
        except KeyboardInterrupt:
            print("\nSkipping interactive tests")
    else:
        print("No API key - skipping interactive tests")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All basic tests passed!")
        if api_key:
            print("   Interactive tests available - run the script again to try them")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
