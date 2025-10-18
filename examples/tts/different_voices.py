#!/usr/bin/env python3
"""
Text-to-Speech (TTS) with Different Voices Example

This example demonstrates how to use different speaker voices with Talkscriber's
TTS service. It generates the same text with multiple voices and saves them
to separate files.

Requirements:
- Talkscriber API key
- Internet connection

Usage:
    python tts_different_voices.py
"""

import os
import sys
from talkscriber.tts import TalkScriberTTSClient


def main():
    """TTS example with different voices"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    print("=== Talkscriber TTS with Different Voices Example ===")
    print("This example will generate the same text with different voices.\n")
    
    # Text to convert to speech
    text = "Hello! This is a demonstration of different voices available " \
           "in the Talkscriber text-to-speech system."
    
    # Available voices (you can modify this list based on available voices)
    voices = ["tara", "tara"]  # Using tara as example - replace with actual available voices
    
    print(f"Text to generate: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    print(f"Voices to try: {', '.join(voices)}")
    print()
    
    successful_generations = 0
    
    for i, voice in enumerate(voices, 1):
        output_file = f"voice_{voice}_{i}.wav"
        
        print(f"Generating speech with voice '{voice}'...")
        
        # Create TTS client for this voice
        tts_client = TalkScriberTTSClient(
            host="api.talkscriber.com",
            port=9099,
            text=text,
            speaker_name=voice,
            api_key=api_key,
            enable_playback=False,  # Disable playback for batch processing
            save_audio_path=output_file
        )
        
        try:
            # Generate speech
            success = tts_client.run_simple_test()
            
            if success:
                print(f"✅ Voice '{voice}' completed successfully!")
                
                # Check if file was created
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"   📁 Saved to: {output_file} ({file_size:,} bytes)")
                    
                    # Show audio information
                    audio_info = tts_client.get_audio_info()
                    print(f"   📊 Audio info: {audio_info['chunks_count']} chunks, "
                          f"{audio_info['duration_seconds']:.2f}s duration")
                    
                    successful_generations += 1
                else:
                    print(f"   ⚠️  File not created: {output_file}")
            else:
                print(f"❌ Voice '{voice}' generation failed")
                
        except Exception as e:
            print(f"❌ Error with voice '{voice}': {e}")
        
        print()  # Empty line for readability
    
    # Summary
    print("=" * 50)
    print(f"Summary: {successful_generations}/{len(voices)} voices generated successfully")
    
    if successful_generations > 0:
        print("\nGenerated files:")
        for i, voice in enumerate(voices, 1):
            output_file = f"voice_{voice}_{i}.wav"
            if os.path.exists(output_file):
                print(f"  - {output_file}")
        
        print(f"\nYou can now play these files to compare the different voices!")


if __name__ == "__main__":
    main()
