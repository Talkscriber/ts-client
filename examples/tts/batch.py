#!/usr/bin/env python3
"""
Batch Text-to-Speech (TTS) Processing Example

This example demonstrates how to process multiple text inputs in batch,
generating audio files for each one. Useful for creating audio content
from text files, generating voiceovers, or processing large datasets.

Requirements:
- Talkscriber API key
- Text file with content to process
- Internet connection

Usage:
    python batch_tts.py input.txt
    python batch_tts.py input.txt --voice tara --output-dir audio_output
"""

import os
import sys
import argparse
import time
from pathlib import Path
from talkscriber.tts import TalkScriberTTSClient


def read_text_file(file_path):
    """Read text file and split into sentences or paragraphs"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split by double newlines (paragraphs) or single newlines (sentences)
        if '\n\n' in content:
            texts = [text.strip() for text in content.split('\n\n') if text.strip()]
        else:
            texts = [text.strip() for text in content.split('\n') if text.strip()]
        
        return texts
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


def generate_audio_for_text(text, index, voice, api_key, output_dir):
    """Generate audio for a single text"""
    output_file = output_dir / f"audio_{index:03d}.wav"
    
    print(f"Processing text {index}: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    # Create TTS client
    tts_client = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text=text,
        speaker_name=voice,
        api_key=api_key,
        enable_playback=False,  # Silent mode for batch processing
        save_audio_path=str(output_file)
    )
    
    try:
        # Generate speech
        success = tts_client.run_simple_test()
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            audio_info = tts_client.get_audio_info()
            print(f"  ✅ Generated: {output_file.name} ({file_size:,} bytes, {audio_info['duration_seconds']:.2f}s)")
            return True
        else:
            print(f"  ❌ Failed to generate: {output_file.name}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error generating audio: {e}")
        return False


def main():
    """Main batch processing function"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Batch TTS processing from text file")
    parser.add_argument("input_file", help="Text file containing content to process")
    parser.add_argument("--voice", default="tara", help="Voice to use (default: tara)")
    parser.add_argument("--output-dir", default="batch_audio_output", help="Output directory (default: batch_audio_output)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds (default: 1.0)")
    parser.add_argument("--sample", action="store_true", help="Use sample text file from data/ directory")
    
    args = parser.parse_args()
    
    # Handle sample file option
    if args.sample:
        # Use the sample text file from data directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_file = os.path.join(script_dir, "..", "data", "sample_text.txt")
        args.input_file = sample_file
        print(f"Using sample text file: {args.input_file}")
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Get API key from environment variable
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        print("Get your API key from: https://app.talkscriber.com")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("=== Batch TTS Processing ===")
    print(f"Input file: {args.input_file}")
    print(f"Voice: {args.voice}")
    print(f"Output directory: {output_dir}")
    print(f"Delay between requests: {args.delay}s")
    print()
    
    # Read and parse input file
    print("Reading input file...")
    texts = read_text_file(args.input_file)
    
    if not texts:
        print("No text content found in input file.")
        sys.exit(1)
    
    print(f"Found {len(texts)} text segments to process")
    print()
    
    # Process each text segment
    successful = 0
    failed = 0
    
    for i, text in enumerate(texts, 1):
        print(f"[{i}/{len(texts)}] ", end="")
        
        success = generate_audio_for_text(text, i, args.voice, api_key, output_dir)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Add delay between requests to avoid rate limiting
        if i < len(texts):  # Don't delay after the last item
            time.sleep(args.delay)
    
    # Summary
    print("\n" + "="*50)
    print("Batch Processing Summary:")
    print(f"Total segments: {len(texts)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/len(texts)*100):.1f}%")
    
    if successful > 0:
        print(f"\nGenerated audio files in: {output_dir}")
        print("Files:")
        for audio_file in sorted(output_dir.glob("audio_*.wav")):
            file_size = audio_file.stat().st_size
            print(f"  - {audio_file.name} ({file_size:,} bytes)")


if __name__ == "__main__":
    main()
