#!/usr/bin/env python3
"""
Speech-to-Text (STT) File Transcription Example

This example demonstrates how to transcribe an audio file using Talkscriber's
transcription service.

Requirements:
- Talkscriber API key
- Audio file (WAV, MP3, etc.)
- Internet connection

Usage:
    python stt_file.py path/to/audio_file.wav
"""

import os
import sys
import argparse
from talkscriber.stt import TranscriptionClient


def main():
    """STT example using audio file input"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Transcribe an audio file using Talkscriber")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--multilingual", action="store_true", help="Enable multilingual detection")
    parser.add_argument("--translate", action="store_true", help="Enable translation")
    parser.add_argument("--turn-detection", action="store_true", help="Enable smart turn detection")
    
    args = parser.parse_args()
    
    # Check if audio file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file '{args.audio_file}' not found.")
        sys.exit(1)
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber File Transcription Example ===")
    print(f"Transcribing file: {args.audio_file}")
    print(f"Language: {args.language if not args.multilingual else 'auto-detect'}")
    print(f"Translation: {'enabled' if args.translate else 'disabled'}")
    print(f"Turn detection: {'enabled' if args.turn_detection else 'disabled'}")
    print()
    
    # Create transcription client
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language=args.language,
        multilingual=args.multilingual,
        translate=args.translate,
        enable_turn_detection=args.turn_detection,
        turn_detection_timeout=0.6
    )
    
    try:
        print("Starting file transcription...")
        print("Transcription will appear below:\n")
        
        # Transcribe the audio file
        client(args.audio_file)
        
        print("\n\nFile transcription completed!")
        
    except Exception as e:
        print(f"\nError during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
