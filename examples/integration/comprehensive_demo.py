#!/usr/bin/env python3
"""
Example script demonstrating Talkscriber Python Client usage

This script shows how to use both the Live Transcription and Text-to-Speech
capabilities of the Talkscriber client library.
"""

import os
import sys
from talkscriber.stt import TranscriptionClient
from talkscriber.tts import TalkScriberTTSClient


def example_live_transcription():
    """Example of live transcription usage"""
    print("=== Live Transcription Example ===")
    
    # You need to set your API key
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Please set TALKSCRIBER_API_KEY environment variable")
        return
    
    # Create transcription client
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language="en",
        enable_turn_detection=True
    )
    
    print("Starting live transcription from microphone...")
    print("Press Ctrl+C to stop")
    
    try:
        # Start transcription (this will use microphone input)
        client()
    except KeyboardInterrupt:
        print("\nTranscription stopped by user")


def example_tts():
    """Example of text-to-speech usage"""
    print("\n=== Text-to-Speech Example ===")
    
    # You need to set your API key
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Please set TALKSCRIBER_API_KEY environment variable")
        return
    
    # Create TTS client
    tts_client = TalkScriberTTSClient(
        api_key=api_key,
        text="Hello! This is a demonstration of the Talkscriber text-to-speech system. "
             "The audio you're hearing is being generated in real-time with ultra-low latency.",
        speaker_name="tara",
        enable_playback=True,
        save_audio_path="example_output.wav"
    )
    
    print("Generating speech...")
    success = tts_client.run_simple_test()
    
    if success:
        print("TTS generation completed successfully!")
        print(f"Audio saved to: example_output.wav")
        
        # Show audio information
        audio_info = tts_client.get_audio_info()
        print(f"Audio info: {audio_info['chunks_count']} chunks, "
              f"{audio_info['total_bytes']:,} bytes, "
              f"{audio_info['duration_seconds']:.2f}s duration")
    else:
        print("TTS generation failed")


def example_file_transcription():
    """Example of transcribing an audio file"""
    print("\n=== File Transcription Example ===")
    
    # You need to set your API key
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Please set TALKSCRIBER_API_KEY environment variable")
        return
    
    # Check if example audio file exists
    audio_file = "example_audio.wav"
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found. Skipping file transcription example.")
        return
    
    # Create transcription client
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language="en"
    )
    
    print(f"Transcribing audio file: {audio_file}")
    
    try:
        # Transcribe the audio file
        client(audio_file)
    except Exception as e:
        print(f"Error transcribing file: {e}")


def main():
    """Main example function"""
    print("Talkscriber Python Client Examples")
    print("==================================")
    
    # Check if API key is set
    if not os.getenv("TALKSCRIBER_API_KEY"):
        print("\nTo run these examples, you need to set your Talkscriber API key:")
        print("export TALKSCRIBER_API_KEY='your_api_key_here'")
        print("\nGet your API key from: https://app.talkscriber.com")
        return
    
    # Run examples
    try:
        # TTS example (doesn't require user interaction)
        example_tts()
        
        # Ask user if they want to run live transcription
        print("\nWould you like to run the live transcription example? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes']:
            example_live_transcription()
        
        # File transcription example
        example_file_transcription()
        
    except KeyboardInterrupt:
        print("\nExamples stopped by user")
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    main()
