"""
Talkscriber Python Client Library

A comprehensive Python client for Talkscriber's Live Transcription and Text-to-Speech services.

This package provides:
- Real-time speech-to-text transcription via WebSocket
- Text-to-speech conversion with ultra-low latency streaming
- Support for multiple languages and voice options
- Easy-to-use Python APIs for both services

Example usage:

    # Speech-to-Text (STT)
    from talkscriber.stt import TranscriptionClient
    
    client = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key="your_api_key",
        language="en"
    )
    client()  # Start live transcription from microphone
    
    # Text-to-Speech
    from talkscriber.tts import TalkScriberTTSClient
    
    tts_client = TalkScriberTTSClient(
        api_key="your_api_key",
        text="Hello, world!",
        speaker_name="tara"
    )
    tts_client.run_simple_test()

For more information, visit: https://docs.talkscriber.com
"""

__version__ = "1.0.0"
__author__ = "Talkscriber"
__email__ = "support@talkscriber.com"

# Import main classes for easy access
try:
    from .stt import TranscriptionClient
    from .tts import TalkScriberTTSClient
    
    __all__ = [
        "TranscriptionClient",
        "TalkScriberTTSClient",
        "__version__",
        "__author__",
        "__email__",
    ]
except ImportError as e:
    # Handle case where dependencies are not installed
    __all__ = [
        "__version__",
        "__author__",
        "__email__",
    ]
    
    def _import_error():
        raise ImportError(
            "Talkscriber client dependencies are not installed. "
            "Please install them with: pip install -r requirements.txt"
        ) from e
    
    # Create placeholder classes that raise helpful errors
    class TranscriptionClient:
        def __init__(self, *args, **kwargs):
            _import_error()
    
    class TalkScriberTTSClient:
        def __init__(self, *args, **kwargs):
            _import_error()
