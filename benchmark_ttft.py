#!/usr/bin/env python3
"""
TTFT Benchmark Script for TalkScriber TTS Client

This script runs 100 inference tests and measures Time To First Token (TTFT)
to calculate p50 and p95 latency statistics.
"""

import argparse
import os
import statistics
import sys
import time
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from talkscriber.tts import TalkScriberTTSClient


def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculate the percentile of a list of values"""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    index = (len(sorted_data) - 1) * percentile / 100.0
    lower = int(index)
    upper = lower + 1
    weight = index - lower
    
    if upper >= len(sorted_data):
        return sorted_data[lower]
    
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


def run_benchmark(api_key: str, num_runs: int = 100, host: str = "api.talkscriber.com", 
                  port: int = 9099, speaker_name: str = "tara"):
    """Run TTFT benchmark"""
    
    # Text that generates approximately 10 seconds of audio
    # At typical speech rate of ~150 words per minute, 10 seconds = ~25 words
    benchmark_text = (
        "The future of artificial intelligence is fascinating and rapidly evolving. "
    )
    
    print("=" * 80)
    print("TalkScriber TTS - TTFT Benchmark")
    print("=" * 80)
    print(f"Configuration:")
    print(f"  Host: {host}:{port}")
    print(f"  Speaker: {speaker_name}")
    print(f"  Number of runs: {num_runs}")
    print(f"  Text length: {len(benchmark_text)} characters, {len(benchmark_text.split())} words")
    print(f"  Text preview: '{benchmark_text[:60]}...'")
    print("=" * 80)
    print()
    
    ttft_measurements = []
    successful_runs = 0
    failed_runs = 0
    
    for i in range(num_runs):
        print(f"Run {i+1}/{num_runs}...", end=" ", flush=True)
        
        try:
            # Create client with playback disabled for faster benchmarking
            client = TalkScriberTTSClient(
                host=host,
                port=port,
                text=benchmark_text,
                speaker_name=speaker_name,
                api_key=api_key,
                enable_playback=False,  # Disable playback for benchmarking
                save_audio_path=None
            )
            
            # Run the test
            success = client.run_simple_test()
            
            if success:
                # Get TTFT metrics
                ttft_metrics = client.get_ttft_metrics()
                
                if ttft_metrics['ttft_seconds'] is not None:
                    ttft_ms = ttft_metrics['ttft_ms']
                    ttft_measurements.append(ttft_ms)
                    successful_runs += 1
                    print(f"✓ TTFT: {ttft_ms:.2f}ms")
                else:
                    failed_runs += 1
                    print("✗ No TTFT recorded")
            else:
                failed_runs += 1
                print("✗ Failed")
        
        except KeyboardInterrupt:
            print("\n\nBenchmark interrupted by user")
            break
        except Exception as e:
            failed_runs += 1
            print(f"✗ Error: {e}")
        
        # Small delay between runs to avoid overwhelming the server
        if i < num_runs - 1:
            time.sleep(0.5)
    
    print()
    print("=" * 80)
    print("Benchmark Results")
    print("=" * 80)
    
    if not ttft_measurements:
        print("ERROR: No successful measurements collected!")
        return False
    
    # Calculate statistics
    p50 = calculate_percentile(ttft_measurements, 50)
    p95 = calculate_percentile(ttft_measurements, 95)
    p99 = calculate_percentile(ttft_measurements, 99)
    mean = statistics.mean(ttft_measurements)
    median = statistics.median(ttft_measurements)
    std_dev = statistics.stdev(ttft_measurements) if len(ttft_measurements) > 1 else 0
    min_ttft = min(ttft_measurements)
    max_ttft = max(ttft_measurements)
    
    print(f"Total runs: {num_runs}")
    print(f"Successful: {successful_runs}")
    print(f"Failed: {failed_runs}")
    print()
    print("TTFT Latency Statistics (milliseconds):")
    print(f"  Min:       {min_ttft:8.2f} ms")
    print(f"  Max:       {max_ttft:8.2f} ms")
    print(f"  Mean:      {mean:8.2f} ms")
    print(f"  Median:    {median:8.2f} ms")
    print(f"  Std Dev:   {std_dev:8.2f} ms")
    print()
    print("Percentiles:")
    print(f"  P50:       {p50:8.2f} ms  ⭐")
    print(f"  P95:       {p95:8.2f} ms  ⭐")
    print(f"  P99:       {p99:8.2f} ms")
    print("=" * 80)
    
    # Save results to file
    output_file = f"ttft_benchmark_results_{int(time.time())}.txt"
    with open(output_file, 'w') as f:
        f.write("TalkScriber TTS - TTFT Benchmark Results\n")
        f.write("=" * 80 + "\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Host: {host}:{port}\n")
        f.write(f"Speaker: {speaker_name}\n")
        f.write(f"Text: {benchmark_text}\n")
        f.write("\n")
        f.write(f"Total runs: {num_runs}\n")
        f.write(f"Successful: {successful_runs}\n")
        f.write(f"Failed: {failed_runs}\n")
        f.write("\n")
        f.write("TTFT Latency Statistics (milliseconds):\n")
        f.write(f"  Min:       {min_ttft:8.2f} ms\n")
        f.write(f"  Max:       {max_ttft:8.2f} ms\n")
        f.write(f"  Mean:      {mean:8.2f} ms\n")
        f.write(f"  Median:    {median:8.2f} ms\n")
        f.write(f"  Std Dev:   {std_dev:8.2f} ms\n")
        f.write("\n")
        f.write("Percentiles:\n")
        f.write(f"  P50:       {p50:8.2f} ms\n")
        f.write(f"  P95:       {p95:8.2f} ms\n")
        f.write(f"  P99:       {p99:8.2f} ms\n")
        f.write("\n")
        f.write("Raw measurements (ms):\n")
        for idx, ttft in enumerate(ttft_measurements, 1):
            f.write(f"  Run {idx:3d}: {ttft:.2f}\n")
    
    print(f"\nResults saved to: {output_file}")
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TTFT Benchmark for TalkScriber TTS Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python benchmark_ttft.py --api-key YOUR_KEY --runs 100
  
  python benchmark_ttft.py --api-key YOUR_KEY --runs 50 --host localhost --port 9099
        """
    )
    
    parser.add_argument(
        "--api-key",
        required=True,
        help="Talkscriber API key"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=100,
        help="Number of benchmark runs (default: 100)"
    )
    parser.add_argument(
        "--host",
        default="api.talkscriber.com",
        help="TTS server hostname (default: api.talkscriber.com)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9099,
        help="TTS server port (default: 9099)"
    )
    parser.add_argument(
        "--speaker",
        default="tara",
        help="Speaker voice to use (default: tara)"
    )
    
    args = parser.parse_args()
    
    try:
        success = run_benchmark(
            api_key=args.api_key,
            num_runs=args.runs,
            host=args.host,
            port=args.port,
            speaker_name=args.speaker
        )
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

