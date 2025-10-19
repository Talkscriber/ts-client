#!/usr/bin/env python3
"""
Multilingual Speech-to-Text (STT) Example

This example demonstrates Talkscriber's multilingual transcription capabilities.
It can automatically detect the language being spoken and transcribe accordingly.

Requirements:
- Talkscriber API key
- Microphone access
- Internet connection

Usage:
    python stt_multilingual.py
"""

import os
import sys
from talkscriber.stt import TranscriptionClient


def main():
    """Multilingual STT example using microphone input"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber Multilingual STT Example ===")
    print("This example will automatically detect the language you're speaking")
    print("and transcribe it accordingly. Supported languages include:")
    print("- English, Spanish, French, German, Italian, Portuguese")
    print("- Chinese, Japanese, Korean, Arabic, Hindi, and many more")
    print("\nPress Ctrl+C to stop.\n")
    
    # Create transcription client with multilingual support
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language=None,  # Not needed when multilingual=True
        multilingual=True,  # Enable automatic language detection
        translate=False,
        enable_turn_detection=True,
        turn_detection_timeout=0.6
    )
    
    try:
        print("Starting multilingual transcription...")
        print("Speak in any supported language!\n")
        
        # Start transcription (uses microphone by default)
        client()
        
    except KeyboardInterrupt:
        print("\n\nTranscription stopped by user.")
    except Exception as e:
        print(f"\nError during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
