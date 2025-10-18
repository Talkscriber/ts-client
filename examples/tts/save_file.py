#!/usr/bin/env python3
"""
Text-to-Speech (TTS) with File Saving Example

This example demonstrates how to generate speech and save it to an audio file
using Talkscriber's TTS service.

Requirements:
- Talkscriber API key
- Internet connection

Usage:
    python tts_save_file.py
"""

import os
import sys
from talkscriber.tts import TalkScriberTTSClient


def main():
    """TTS example with file saving"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber TTS with File Saving Example ===")
    print("This example will generate speech and save it to an audio file.\n")
    
    # Text to convert to speech
    text = "This is a test of the Talkscriber text-to-speech system. " \
           "The generated audio will be saved to a WAV file for later use."
    
    # Output file path
    output_file = "generated_speech.wav"
    
    # Create TTS client
    tts_client = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text=text,
        speaker_name="tara",
        api_key=api_key,
        enable_playback=True,  # Also play the audio
        save_audio_path=output_file  # Save to file
    )
    
    try:
        print(f"Text to speak: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"Speaker: {tts_client.speaker_name}")
        print(f"Output file: {output_file}")
        print("\nGenerating speech...")
        
        # Generate speech
        success = tts_client.run_simple_test()
        
        if success:
            print("\n✅ TTS generation completed successfully!")
            
            # Check if file was created
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ Audio file saved: {output_file} ({file_size:,} bytes)")
            else:
                print(f"⚠️  Audio file not found: {output_file}")
            
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
