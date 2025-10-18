#!/usr/bin/env python3
"""
Basic Text-to-Speech (TTS) Example

This example demonstrates the basic usage of Talkscriber's text-to-speech
service. It converts text to speech and plays it in real-time.

Requirements:
- Talkscriber API key
- Audio output device
- Internet connection

Usage:
    python tts_basic.py
"""

import os
import sys
from talkscriber.tts import TalkScriberTTSClient


def main():
    """Basic TTS example"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber Basic TTS Example ===")
    print("This example will convert text to speech and play it in real-time.\n")
    
    # Text to convert to speech
    text = "Hello! This is a demonstration of the Talkscriber text-to-speech system. " \
           "The audio you're hearing is being generated in real-time with ultra-low latency."
    
    # Create TTS client
    tts_client = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text=text,
        speaker_name="tara",  # Default voice
        api_key=api_key,
        enable_playback=True,  # Enable real-time audio playback
        save_audio_path=None   # Don't save to file for this example
    )
    
    try:
        print(f"Text to speak: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"Speaker: {tts_client.speaker_name}")
        print("\nGenerating speech...")
        
        # Generate and play speech
        success = tts_client.run_simple_test()
        
        if success:
            print("\n✅ TTS generation completed successfully!")
            
            # Show audio information
            audio_info = tts_client.get_audio_info()
            print(f"Audio info: {audio_info['chunks_count']} chunks, "
                  f"{audio_info['total_bytes']:,} bytes, "
                  f"{audio_info['duration_seconds']:.2f}s duration")
        else:
            print("\n❌ TTS generation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nError during TTS generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
