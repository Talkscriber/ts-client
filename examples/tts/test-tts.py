#!/usr/bin/env python3
"""
Comprehensive test script for Talkscriber TTS (Text-to-Speech) client
"""

import os
import sys
import time
import signal
from talkscriber.tts import TalkScriberTTSClient

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nStopping TTS...")
    sys.exit(0)

def test_tts_import():
    """Test that TTS classes can be imported"""
    print("Testing TTS imports...")
    try:
        from talkscriber.tts import TalkScriberTTSClient
        print("✓ TTS classes imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import TTS classes: {e}")
        return False

def test_tts_instantiation():
    """Test that TTS client can be instantiated"""
    print("\nTesting TTS client instantiation...")
    
    # Check if API key is set
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  TALKSCRIBER_API_KEY environment variable not set")
        print("   Set it with: export TALKSCRIBER_API_KEY='your_api_key_here'")
        print("   Get your API key from: https://app.talkscriber.com")
        return False
    
    try:
        # Test basic instantiation
        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Hello, this is a test of the text-to-speech system.",
            speaker_name="tara"
        )
        print("✓ TalkScriberTTSClient instantiated successfully")
        
        # Test with different configurations
        custom_client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a custom configuration test.",
            speaker_name="tara",
            enable_playback=True,
            save_audio_path="test_output.wav"
        )
        print("✓ Custom TalkScriberTTSClient instantiated")
        
        # Test with different voice
        voice_client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing different voice options.",
            speaker_name="tara",  # You can change this to test different voices
            enable_playback=False  # Silent mode for testing
        )
        print("✓ Voice-specific TalkScriberTTSClient instantiated")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to instantiate TTS client: {e}")
        return False

def test_basic_tts():
    """Test basic TTS functionality"""
    print("\nTesting basic TTS functionality...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping basic TTS test - no API key")
        return False
    
    try:
        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Hello! This is a basic test of the Talkscriber text-to-speech system. The audio you're hearing is being generated in real-time.",
            speaker_name="tara",
            enable_playback=True
        )
        
        print("🔊 Starting basic TTS generation...")
        print("   You should hear audio playback")
        print("-" * 50)
        
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, signal_handler)
        
        # Run the TTS
        success = client.run_simple_test()
        
        if success:
            print("✓ Basic TTS test completed successfully")
            return True
        else:
            print("✗ Basic TTS test failed")
            return False
        
    except KeyboardInterrupt:
        print("\n✓ TTS test stopped by user")
        return True
    except Exception as e:
        print(f"✗ Basic TTS test failed: {e}")
        return False

def test_silent_tts():
    """Test TTS in silent mode (no audio playback)"""
    print("\nTesting silent TTS (no audio playback)...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping silent TTS test - no API key")
        return False
    
    try:
        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a silent test of the text-to-speech system. No audio will be played.",
            speaker_name="tara",
            enable_playback=False
        )
        
        print("🔇 Starting silent TTS generation...")
        print("   No audio will be played - testing generation only")
        print("-" * 50)
        
        # Run the TTS
        success = client.run_simple_test()
        
        if success:
            print("✓ Silent TTS test completed successfully")
            return True
        else:
            print("✗ Silent TTS test failed")
            return False
        
    except Exception as e:
        print(f"✗ Silent TTS test failed: {e}")
        return False

def test_file_save_tts():
    """Test TTS with file saving"""
    print("\nTesting TTS with file saving...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping file save TTS test - no API key")
        return False
    
    output_file = "test_tts_output.wav"
    
    try:
        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This audio is being saved to a file for testing purposes. The file will be created in the current directory.",
            speaker_name="tara",
            enable_playback=True,
            save_audio_path=output_file
        )
        
        print(f"💾 Starting TTS with file saving to: {output_file}")
        print("   Audio will be played and saved to file")
        print("-" * 50)
        
        # Run the TTS
        success = client.run_simple_test()
        
        if success:
            # Check if file was created
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ TTS file save test completed successfully")
                print(f"   File created: {output_file} ({file_size:,} bytes)")
                return True
            else:
                print("✗ TTS file save test failed - no output file created")
                return False
        else:
            print("✗ TTS file save test failed")
            return False
        
    except Exception as e:
        print(f"✗ TTS file save test failed: {e}")
        return False

def test_different_voices():
    """Test TTS with different voice options"""
    print("\nTesting TTS with different voices...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping voice test - no API key")
        return False
    
    # Common voice options (adjust based on available voices)
    voices = ["tara"]  # Add more voices as available
    
    try:
        for voice in voices:
            print(f"🎭 Testing voice: {voice}")
            
            client = TalkScriberTTSClient(
                api_key=api_key,
                text=f"This is a test of the {voice} voice for text-to-speech conversion.",
                speaker_name=voice,
                enable_playback=True
            )
            
            success = client.run_simple_test()
            
            if success:
                print(f"✓ Voice {voice} test completed")
            else:
                print(f"✗ Voice {voice} test failed")
                return False
            
            # Small delay between voices
            time.sleep(1)
        
        print("✓ All voice tests completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Voice test failed: {e}")
        return False

def test_tts_cli():
    """Test TTS CLI tools"""
    print("\nTesting TTS CLI tools...")
    
    import subprocess
    import shutil
    
    # Find the correct CLI tool path
    cli_path = shutil.which('talkscriber-tts')
    if not cli_path:
        print("✗ TTS CLI tool not found in PATH")
        return False
    
    # Test TTS CLI help
    try:
        result = subprocess.run([
            cli_path, 
            '--help'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✓ TTS CLI tool available")
            return True
        else:
            print("✗ TTS CLI tool failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ TTS CLI test failed: {e}")
        return False

def test_tts_cli_with_api_key():
    """Test TTS CLI with actual API key"""
    print("\nTesting TTS CLI with API key...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping CLI API test - no API key")
        return False
    
    import subprocess
    import shutil
    
    # Find the correct CLI tool path
    cli_path = shutil.which('talkscriber-tts')
    if not cli_path:
        print("✗ TTS CLI tool not found in PATH")
        return False
    
    try:
        # Test basic TTS CLI command
        result = subprocess.run([
            cli_path,
            '--api-key', api_key,
            '--text', 'This is a CLI test of the text-to-speech system.',
            '--speaker', 'tara'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ TTS CLI with API key works")
            return True
        else:
            print("✗ TTS CLI with API key failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ TTS CLI API test failed: {e}")
        return False

def test_audio_info():
    """Test getting audio information from TTS client"""
    print("\nTesting audio information retrieval...")
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("⚠️  Skipping audio info test - no API key")
        return False
    
    try:
        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a test for retrieving audio information from the TTS system.",
            speaker_name="tara",
            enable_playback=False  # Silent mode for info testing
        )
        
        print("📊 Testing audio information retrieval...")
        
        # Run TTS to generate audio
        success = client.run_simple_test()
        
        if success:
            # Get audio information
            audio_info = client.get_audio_info()
            print("✓ Audio information retrieved successfully:")
            print(f"   Chunks: {audio_info['chunks_count']}")
            print(f"   Total bytes: {audio_info['total_bytes']:,}")
            print(f"   Duration: {audio_info['duration_seconds']:.2f} seconds")
            print(f"   Sample rate: {audio_info['sample_rate']} Hz")
            print(f"   Channels: {audio_info['channels']}")
            print(f"   Bits per sample: {audio_info['bits_per_sample']}")
            return True
        else:
            print("✗ Audio info test failed - TTS generation failed")
            return False
        
    except Exception as e:
        print(f"✗ Audio info test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Talkscriber TTS Client Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Run basic tests
    tests = [
        ("Import Test", test_tts_import),
        ("Instantiation Test", test_tts_instantiation),
        ("CLI Tools Test", test_tts_cli),
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
        print("1. Basic TTS (with audio playback)")
        print("2. Silent TTS (no audio playback)")
        print("3. TTS with file saving")
        print("4. Different voices test")
        print("5. Audio information test")
        print("6. CLI test with API key")
        print("7. Run all interactive tests")
        print("8. Skip interactive tests")
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                test_basic_tts()
            elif choice == "2":
                test_silent_tts()
            elif choice == "3":
                test_file_save_tts()
            elif choice == "4":
                test_different_voices()
            elif choice == "5":
                test_audio_info()
            elif choice == "6":
                test_tts_cli_with_api_key()
            elif choice == "7":
                print("Running all interactive tests...")
                test_basic_tts()
                test_silent_tts()
                test_file_save_tts()
                test_different_voices()
                test_audio_info()
                test_tts_cli_with_api_key()
            elif choice == "8":
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
