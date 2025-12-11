#!/usr/bin/env python3
"""
Command-line interface for Talkscriber Live Transcription
"""

import argparse
import sys
import json
from .client import TranscriptionClient
from .batch_client import BatchTranscriptionClient


def run_batch_processing(args):
    """
    Run batch processing mode

    Args:
        args: Parsed command-line arguments
    """
    # Validate file argument
    if not args.file:
        print("[ERROR]: --file argument is required for offline mode")
        sys.exit(1)

    print("[INFO]: Starting offline batch processing...")
    print(f"[INFO]: Audio file: {args.file}")
    print(f"[INFO]: Language: {args.language}")
    print(f"[INFO]: Translation: {'enabled' if args.translate else 'disabled'}")
    print()

    try:
        # Create batch client
        client = BatchTranscriptionClient(api_url=args.batch_host, api_key=args.api_key)

        # Determine task type
        task = "translate" if args.translate else "transcribe"

        # Prepare features list from command-line arguments
        features = args.features if args.features else []
        if features:
            print(f"[INFO]: Features enabled: {', '.join(features)}")
            print()

        # Create batch job
        print("[INFO]: Submitting job to batch API...")
        job_response = client.create_batch_job(
            audio_file_path=args.file,
            language=args.language,
            task=task,
            features=features,
        )

        job_id = job_response.get("id")
        if not job_id:
            print("[ERROR]: Failed to get job ID from response")
            sys.exit(1)

        print("[INFO]: Job submitted successfully")
        print(f"[INFO]: Job ID: {job_id}")
        print()

        # Wait for completion
        final_status = client.wait_for_job_completion(job_id)

        # Display results
        print()
        print("=" * 80)
        print("TRANSCRIPTION RESULTS")
        print("=" * 80)
        print()

        # Parse and display transcription
        results = final_status.get("results")
        if results:
            # Handle both string and dict results
            if isinstance(results, str):
                try:
                    results = json.loads(results)
                except json.JSONDecodeError:
                    print("[WARNING]: Could not parse results as JSON")
                    print(results)
                    return

            # Extract transcription from results
            transcribe_data = results.get("transcribe", [])

            if transcribe_data:
                # Check if word-level timestamps are available
                has_word_timestamps = any(
                    segment.get("words") for segment in transcribe_data
                )

                # Display segments
                for i, segment in enumerate(transcribe_data, 1):
                    text = segment.get("text", "")
                    start = segment.get("start", 0)
                    end = segment.get("end", 0)

                    print(f"[{start:.2f}s - {end:.2f}s]: {text}")

                    # Display word-level timestamps if available
                    if has_word_timestamps and segment.get("words"):
                        words = segment.get("words", [])
                        print("  Word-level timestamps:")
                        for word_data in words:
                            word_text = word_data.get("word", "")
                            word_start = word_data.get("start", 0)
                            word_end = word_data.get("end", 0)
                            print(
                                f"    [{word_start:.2f}s - {word_end:.2f}s]: {word_text}"
                            )
                        print()

                print()
                print("-" * 80)

                # Display full transcript
                full_transcript = " ".join(
                    [seg.get("text", "") for seg in transcribe_data]
                )
                print("Full Transcript:")
                print(full_transcript)
            else:
                print("[INFO]: No transcription data available")
        else:
            print("[INFO]: No results available")

        print()
        print("=" * 80)

    except FileNotFoundError as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)


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

  # Offline mode with features
  talkscriber-stt --api-key YOUR_KEY --file audio.wav --offline --features sentiment redaction
        """,
    )

    # Required arguments
    parser.add_argument(
        "--api-key",
        required=True,
        help="Talkscriber API key (get from https://app.talkscriber.com)",
    )

    # Connection arguments
    parser.add_argument(
        "--host",
        default="wss://api.talkscriber.com",
        help="WebSocket host URL (default: wss://api.talkscriber.com)",
    )
    parser.add_argument(
        "--port", type=int, default=9090, help="WebSocket port (default: 9090)"
    )

    # Language arguments
    parser.add_argument(
        "--language", default="en", help="Language code for transcription (default: en)"
    )
    parser.add_argument(
        "--multilingual",
        action="store_true",
        help="Enable multilingual detection (auto-detect language)",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Enable translation of transcribed text",
    )

    # Turn detection arguments
    parser.add_argument(
        "--turn-detection",
        action="store_true",
        help="Enable smart turn detection using ML model",
    )
    parser.add_argument(
        "--turn-detection-timeout",
        type=float,
        default=0.6,
        help="Timeout for turn detection in seconds (default: 0.6)",
    )

    # Input arguments
    parser.add_argument(
        "--file", help="Audio file to transcribe (if not provided, uses microphone)"
    )

    # Offline/Batch mode arguments
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use offline batch processing mode instead of live streaming",
    )
    parser.add_argument(
        "--batch-host",
        default="https://api.talkscriber.com/api/jobs",
        help="Batch API endpoint URL (default: https://api.talkscriber.com/api/jobs)",
    )
    parser.add_argument(
        "--features",
        nargs="+",
        help="Features to enable for offline mode (e.g., sentiment redaction)",
    )

    args = parser.parse_args()

    try:
        # Check if offline mode is enabled
        if args.offline:
            # Use batch processing mode
            run_batch_processing(args)
        else:
            # Use live streaming mode
            # Create transcription client
            client = TranscriptionClient(
                host=args.host,
                port=args.port,
                api_key=args.api_key,
                multilingual=args.multilingual,
                language=args.language,
                translate=args.translate,
                enable_turn_detection=args.turn_detection,
                turn_detection_timeout=args.turn_detection_timeout,
            )

            print("[INFO]: Starting transcription...")
            print(
                f"[INFO]: Language: {args.language if not args.multilingual else 'auto-detect'}"
            )
            print(f"[INFO]: Translation: {'enabled' if args.translate else 'disabled'}")
            print(
                f"[INFO]: Turn detection: {'enabled' if args.turn_detection else 'disabled'}"
            )
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
