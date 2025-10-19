#!/usr/bin/env python3
"""
Command-line interface for Talkscriber Live Transcription
"""

import argparse
import sys
from .client import TranscriptionClient


def main():
    """Main CLI entry point for live transcription"""
    parser = argparse.ArgumentParser(
        description="Talkscriber Live Transcription Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe from microphone with English
  talkscriber-stt --api-key YOUR_KEY --language en

  # Transcribe from audio file
  talkscriber-stt --api-key YOUR_KEY --file audio.wav

  # Enable multilingual detection
  talkscriber-stt --api-key YOUR_KEY --multilingual

  # Enable translation
  talkscriber-stt --api-key YOUR_KEY --translate

  # Enable smart turn detection
  talkscriber-stt --api-key YOUR_KEY --turn-detection
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--api-key",
        required=True,
        help="Talkscriber API key (get from https://app.talkscriber.com)"
    )
    
    # Connection arguments
    parser.add_argument(
        "--host",
        default="wss://api.talkscriber.com",
        help="WebSocket host URL (default: wss://api.talkscriber.com)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9090,
        help="WebSocket port (default: 9090)"
    )
    
    # Language arguments
    parser.add_argument(
        "--language",
        default="en",
        help="Language code for transcription (default: en)"
    )
    parser.add_argument(
        "--multilingual",
        action="store_true",
        help="Enable multilingual detection (auto-detect language)"
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Enable translation of transcribed text"
    )
    
    # Turn detection arguments
    parser.add_argument(
        "--turn-detection",
        action="store_true",
        help="Enable smart turn detection using ML model"
    )
    parser.add_argument(
        "--turn-detection-timeout",
        type=float,
        default=0.6,
        help="Timeout for turn detection in seconds (default: 0.6)"
    )
    
    # Input arguments
    parser.add_argument(
        "--file",
        help="Audio file to transcribe (if not provided, uses microphone)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create transcription client
        client = TranscriptionClient(
            host=args.host,
            port=args.port,
            api_key=args.api_key,
            multilingual=args.multilingual,
            language=args.language,
            translate=args.translate,
            enable_turn_detection=args.turn_detection,
            turn_detection_timeout=args.turn_detection_timeout
        )
        
        print(f"[INFO]: Starting transcription...")
        print(f"[INFO]: Language: {args.language if not args.multilingual else 'auto-detect'}")
        print(f"[INFO]: Translation: {'enabled' if args.translate else 'disabled'}")
        print(f"[INFO]: Turn detection: {'enabled' if args.turn_detection else 'disabled'}")
        print(f"[INFO]: Input: {'file' if args.file else 'microphone'}")
        print()
        
        # Start transcription
        if args.file:
            print(f"[INFO]: Transcribing file: {args.file}")
            client(args.file)
        else:
            print("[INFO]: Transcribing from microphone (press Ctrl+C to stop)")
            client()
            
    except KeyboardInterrupt:
        print("\n[INFO]: Transcription stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
