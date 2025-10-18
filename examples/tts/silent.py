#!/usr/bin/env python3
"""
Silent Text-to-Speech (TTS) Example

This example demonstrates how to generate speech without playing it back,
useful for batch processing or when you only want to save audio files.

Requirements:
- Talkscriber API key
- Internet connection

Usage:
    python tts_silent.py
"""

import os
import sys
from talkscriber.tts import TalkScriberTTSClient


def main():
    """Silent TTS example (no audio playback)"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber Silent TTS Example ===")
    print("This example will generate speech without playing it back.")
    print("Useful for batch processing or when you only want to save files.\n")
    
    # Text to convert to speech
    text = "This is a silent generation of speech. The audio will be saved " \
           "to a file but not played through your speakers."
    
    # Output file path
    output_file = "silent_speech.wav"
    
    # Create TTS client with playback disabled
    tts_client = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text=text,
        speaker_name="tara",
        api_key=api_key,
        enable_playback=False,  # Disable audio playback
        save_audio_path=output_file  # Save to file
    )
    
    try:
        print(f"Text to generate: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"Speaker: {tts_client.speaker_name}")
        print(f"Output file: {output_file}")
        print("Playback: Disabled (silent mode)")
        print("\nGenerating speech...")
        
        # Generate speech (silently)
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
            
            print(f"\nYou can now play the file manually: {output_file}")
        else:
            print("\n❌ TTS generation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nError during TTS generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
