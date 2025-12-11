#!/usr/bin/env python3
"""
Command-line interface for Talkscriber Text-to-Speech
"""

import argparse
import sys
from .client import TalkScriberTTSClient


def main():
    """Main CLI entry point for text-to-speech"""
    parser = argparse.ArgumentParser(
        description="Talkscriber Text-to-Speech Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic TTS with default voice
  talkscriber-tts --api-key YOUR_KEY --text "Hello, world!"

  # Use specific voice
  talkscriber-tts --api-key YOUR_KEY --text "Hello" --speaker tara

  # Save audio to file
  talkscriber-tts --api-key YOUR_KEY --text "Hello" --save output.wav

  # Silent mode (no playback, save only)
  talkscriber-tts --api-key YOUR_KEY --text "Hello" --save output.wav --no-playback

  # Custom server
  talkscriber-tts --api-key YOUR_KEY --text "Hello" --host localhost --port 9099
        """,
    )

    # Required arguments
    parser.add_argument(
        "--api-key",
        required=True,
        help="Talkscriber API key (get from https://app.talkscriber.com)",
    )
    parser.add_argument("--text", required=True, help="Text to convert to speech")

    # Connection arguments
    parser.add_argument(
        "--host",
        default="api.talkscriber.com",
        help="TTS server hostname (default: api.talkscriber.com)",
    )
    parser.add_argument(
        "--port", type=int, default=9099, help="TTS server port (default: 9099)"
    )

    # Voice arguments
    parser.add_argument(
        "--speaker", default="tara", help="Speaker voice to use (default: tara)"
    )

    # Audio output arguments
    parser.add_argument("--save", help="Path to save audio file (optional)")
    parser.add_argument(
        "--no-playback",
        action="store_true",
        help="Disable audio playback (useful when only saving to file)",
    )

    # Maya generation config arguments
    parser.add_argument(
        "--temperature",
        type=float,
        help="Maya temperature parameter (controls randomness)",
    )
    parser.add_argument(
        "--top-p", type=float, help="Maya top_p parameter (nucleus sampling)"
    )
    parser.add_argument(
        "--top-k", type=int, help="Maya top_k parameter (top-k sampling)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maya max_tokens parameter (maximum output length)",
    )
    parser.add_argument(
        "--repetition-penalty",
        type=float,
        help="Maya repetition_penalty parameter (penalize repetitions)",
    )
    parser.add_argument(
        "--model", default="TTS_MAYA", help="TTS model to use (default: TTS_MAYA)"
    )

    args = parser.parse_args()

    try:
        # Build maya_generation_config from command line arguments
        maya_generation_config = {}
        if args.temperature is not None:
            maya_generation_config["temperature"] = args.temperature
        if args.top_p is not None:
            maya_generation_config["top_p"] = args.top_p
        if args.top_k is not None:
            maya_generation_config["top_k"] = args.top_k
        if args.max_tokens is not None:
            maya_generation_config["max_tokens"] = args.max_tokens
        if args.repetition_penalty is not None:
            maya_generation_config["repetition_penalty"] = args.repetition_penalty

        # Create TTS client
        client = TalkScriberTTSClient(
            host=args.host,
            port=args.port,
            text=args.text,
            speaker_name=args.speaker,
            api_key=args.api_key,
            enable_playback=not args.no_playback,
            save_audio_path=args.save,
            model=args.model,
            maya_generation_config=maya_generation_config if maya_generation_config else None,
        )

        print("[INFO]: Starting TTS generation...")
        print(f"[INFO]: Model: {args.model}")
        print(f"[INFO]: Text: '{args.text[:50]}{'...' if len(args.text) > 50 else ''}'")
        print(f"[INFO]: Speaker: {args.speaker}")
        print(f"[INFO]: Playback: {'enabled' if not args.no_playback else 'disabled'}")
        if args.save:
            print(f"[INFO]: Saving to: {args.save}")
        if maya_generation_config:
            print(f"[INFO]: Maya generation config: {maya_generation_config}")
        print()

        # Run TTS
        success = client.run_simple_test()

        if success:
            print("[INFO]: TTS generation completed successfully")

            # Show audio info if available
            audio_info = client.get_audio_info()
            print(
                f"[INFO]: Audio info: {audio_info['chunks_count']} chunks, "
                f"{audio_info['total_bytes']:,} bytes, "
                f"{audio_info['duration_seconds']:.2f}s duration"
            )

            # Show TTFT metrics
            if audio_info.get("ttft_ms") is not None:
                print(
                    "[INFO]: ⚡ TTFT (Time to First Token): " +
                    f"{audio_info['ttft_ms']:.2f}ms"
                )
        else:
            print("[ERROR]: TTS generation failed")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INFO]: TTS generation stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
