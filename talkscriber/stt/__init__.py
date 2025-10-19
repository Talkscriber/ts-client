"""
Talkscriber Speech-to-Text (STT) Module

This module provides speech-to-text transcription capabilities
using WebSocket connections to Talkscriber's transcription services.

Key Features:
- Real-time audio streaming and transcription
- File-based audio transcription
- Support for multiple languages
- Smart turn detection using ML models
- Translation capabilities
- Both live microphone and file input support

Example:
    from talkscriber.stt import TranscriptionClient
    
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
