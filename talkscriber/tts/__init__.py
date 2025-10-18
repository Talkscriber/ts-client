"""
Talkscriber Text-to-Speech Module

This module provides text-to-speech conversion capabilities with
ultra-low latency streaming using WebSocket connections.

Key Features:
- Ultra-low latency streaming (speech starts in <0.1 seconds)
- Real-time audio playback
- Multiple voice options
- Audio file saving
- Configurable buffering for optimal performance

Example:
    from talkscriber.tts import TalkScriberTTSClient
    
    client = TalkScriberTTSClient(
        api_key="your_api_key",
        text="Hello, world!",
        speaker_name="tara"
    )
    client.run_simple_test()
"""

try:
    from .client import TalkScriberTTSClient
    
    __all__ = [
        "TalkScriberTTSClient",
    ]
except ImportError as e:
    # Handle case where dependencies are not installed
    if "dependencies are not installed" in str(e):
        # This is expected when dependencies are missing
        pass
    else:
        # Re-raise other import errors
        raise
    __all__ = []
