#!/usr/bin/env python3
"""
Simple Python WebSocket Client for TTS Server
Usage script that imports the TalkScriberTTSClient class
"""

import sys
from loguru import logger
from client.tts_client import TalkScriberTTSClient

def main():
    """Main function to run the simple client"""
    
    your_api_key = ""
    
    if not your_api_key:
        logger.error("API key is not set")
        return 1
    
    # 5. Audio playback enabled, save to file
    client = TalkScriberTTSClient(
        enable_playback=False,  # Enable real-time audio playback
        save_audio_path="./output/audio.wav",  # Save audio to file
        api_key=your_api_key,
        text="Hello, this is a test of the text-to-speech system.",
        speaker_name="tara"
    )
    
    success = client.run_simple_test()
    
    if success:
        logger.info("Interactive session completed successfully")
    else:
        logger.error("Interactive session failed")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1) 