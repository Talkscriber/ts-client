"""
Talkscriber Live Transcription Module

This module provides real-time speech-to-text transcription capabilities
using WebSocket connections to Talkscriber's transcription services.

Key Features:
- Real-time audio streaming and transcription
- Support for multiple languages
- Smart turn detection using ML models
- Translation capabilities
- File and microphone input support

Example:
    from talkscriber.live import TranscriptionClient
    
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key="your_api_key",
        language="en"
    )
    client()  # Start live transcription
"""

try:
    from .client import TranscriptionClient, Client
    
    __all__ = [
        "TranscriptionClient",
        "Client",
    ]
except ImportError:
    # Handle case where dependencies are not installed
    __all__ = []
