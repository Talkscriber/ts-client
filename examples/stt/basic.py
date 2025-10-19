#!/usr/bin/env python3
"""
Basic Speech-to-Text (STT) Example

This example demonstrates the basic usage of Talkscriber's live transcription
service. It shows how to transcribe speech from a microphone in real-time.

Requirements:
- Talkscriber API key
- Microphone access
- Internet connection

Usage:
    python stt_basic.py
"""

import os
import sys
from talkscriber.stt import TranscriptionClient


def main():
    """Basic STT example using microphone input"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber Basic STT Example ===")
    print("This example will transcribe speech from your microphone in real-time.")
    print("Press Ctrl+C to stop.\n")
    
    # Create transcription client
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language="en",  # English
        multilingual=False,
        translate=False,
        enable_turn_detection=True,
        turn_detection_timeout=0.6
    )
    
    try:
        print("Starting live transcription...")
        print("Speak into your microphone now!\n")
        
        # Start transcription (uses microphone by default)
        client()
        
    except KeyboardInterrupt:
        print("\n\nTranscription stopped by user.")
    except Exception as e:
        print(f"\nError during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
