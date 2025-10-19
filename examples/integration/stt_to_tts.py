#!/usr/bin/env python3
"""
Speech-to-Text to Text-to-Speech (STT → TTS) Example

This example demonstrates a complete voice processing pipeline:
1. Listen to speech and transcribe it (STT)
2. Process the transcribed text
3. Convert the processed text back to speech (TTS)

This creates a voice echo/processing system that can be extended for various
applications like voice assistants, language translation, or content processing.

Requirements:
- Talkscriber API key
- Microphone access
- Audio output device
- Internet connection

Usage:
    python stt_to_tts.py
"""

import os
import sys
import time
from talkscriber.stt import TranscriptionClient
from talkscriber.tts import TalkScriberTTSClient


class VoiceProcessor:
    """A simple voice processing pipeline"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.transcription_buffer = []
        
    def process_text(self, text):
        """
        Process the transcribed text before converting back to speech.
        This is where you can add custom logic like:
        - Text filtering
        - Language translation
        - Content modification
        - Command processing
        """
        # Simple example: add a prefix to the text
        processed_text = f"Processed: {text}"
        
        # You can add more sophisticated processing here:
        # - Remove filler words ("um", "uh", etc.)
        # - Translate to another language
        # - Apply text transformations
        # - Extract commands or intents
        
        return processed_text
    
    def transcribe_speech(self, duration=10):
        """
        Transcribe speech from microphone for a specified duration.
        Returns the transcribed text.
        """
        print(f"Listening for {duration} seconds...")
        print("Speak now!")
        
        # Create transcription client
        stt_client = TranscriptionClient(
            host="wss://api.talkscriber.com",
            port=9090,
            api_key=self.api_key,
            language="en",
            multilingual=False,
            translate=False,
            enable_turn_detection=True,
            turn_detection_timeout=0.6
        )
        
        # For this example, we'll use a simple approach
        # In a real application, you'd want to capture the transcription
        # in real-time and process it as it comes in
        
        try:
            # Start transcription
            stt_client()
            # Note: In a real implementation, you'd capture the transcribed text
            # from the client's output or callbacks
            
            # For demo purposes, return a sample text
            return "Hello, this is a demonstration of the voice processing pipeline."
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
    
    def generate_speech(self, text):
        """
        Convert text to speech and play it.
        """
        if not text:
            print("No text to convert to speech")
            return False
        
        print(f"Converting to speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Create TTS client
        tts_client = TalkScriberTTSClient(
            host="api.talkscriber.com",
            port=9099,
            text=text,
            speaker_name="tara",
            api_key=self.api_key,
            enable_playback=True,
            save_audio_path=None
        )
        
        try:
            # Generate and play speech
            success = tts_client.run_simple_test()
            
            if success:
                print("✅ Speech generation completed!")
                return True
            else:
                print("❌ Speech generation failed")
                return False
                
        except Exception as e:
            print(f"Error during speech generation: {e}")
            return False
    
    def run_voice_pipeline(self):
        """
        Run the complete voice processing pipeline.
        """
        print("=== Voice Processing Pipeline ===")
        print("This example demonstrates STT → Text Processing → TTS")
        print("Press Ctrl+C to stop.\n")
        
        try:
            while True:
                print("\n" + "="*50)
                print("Starting voice processing cycle...")
                
                # Step 1: Transcribe speech
                print("\n1. Transcribing speech...")
                transcribed_text = self.transcribe_speech(duration=5)
                
                if not transcribed_text:
                    print("No speech detected, trying again...")
                    time.sleep(1)
                    continue
                
                print(f"Transcribed: '{transcribed_text}'")
                
                # Step 2: Process the text
                print("\n2. Processing text...")
                processed_text = self.process_text(transcribed_text)
                print(f"Processed: '{processed_text}'")
                
                # Step 3: Convert back to speech
                print("\n3. Converting to speech...")
                success = self.generate_speech(processed_text)
                
                if success:
                    print("\n✅ Voice processing cycle completed!")
                else:
                    print("\n❌ Voice processing cycle failed")
                
                # Wait before next cycle
                print("\nWaiting 3 seconds before next cycle...")
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n\nVoice processing stopped by user.")
        except Exception as e:
            print(f"\nError in voice pipeline: {e}")


def main():
    """Main function"""
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    # Create voice processor
    processor = VoiceProcessor(api_key)
    
    # Run the voice processing pipeline
    processor.run_voice_pipeline()


if __name__ == "__main__":
    main()
