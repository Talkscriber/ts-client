#!/usr/bin/env python3
"""
Configuration Example for Talkscriber Client

This example demonstrates how to configure the Talkscriber clients with
various options and settings for different use cases.

Requirements:
- Talkscriber API key
- Internet connection

Usage:
    python config_example.py
"""

import os
import sys
from talkscriber.stt import TranscriptionClient
from talkscriber.tts import TalkScriberTTSClient


def demonstrate_stt_configurations():
    """Demonstrate different STT client configurations"""
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        return
    
    print("=== STT Configuration Examples ===\n")
    
    # Configuration 1: Basic English transcription
    print("1. Basic English Transcription:")
    stt_basic = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language="en",
        multilingual=False,
        translate=False,
        enable_turn_detection=False,
        turn_detection_timeout=0.6
    )
    print("   - Language: English")
    print("   - Multilingual: False")
    print("   - Translation: False")
    print("   - Turn detection: False")
    print()
    
    # Configuration 2: Multilingual with turn detection
    print("2. Multilingual with Smart Turn Detection:")
    stt_multilingual = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language=None,  # Not needed when multilingual=True
        multilingual=True,
        translate=False,
        enable_turn_detection=True,
        turn_detection_timeout=0.8
    )
    print("   - Language: Auto-detect")
    print("   - Multilingual: True")
    print("   - Translation: False")
    print("   - Turn detection: True (0.8s timeout)")
    print()
    
    # Configuration 3: Translation enabled
    print("3. Spanish with Translation to English:")
    stt_translate = TranscriptionClient(
        host="wss://api.talkscriber.com",
        port=9090,
        api_key=api_key,
        language="es",  # Spanish
        multilingual=False,
        translate=True,  # Translate to English
        enable_turn_detection=True,
        turn_detection_timeout=0.6
    )
    print("   - Language: Spanish")
    print("   - Multilingual: False")
    print("   - Translation: True (to English)")
    print("   - Turn detection: True (0.6s timeout)")
    print()
    
    # Configuration 4: Custom server settings
    print("4. Custom Server Configuration:")
    stt_custom = TranscriptionClient(
        host="wss://custom.talkscriber.com",  # Custom host
        port=9091,  # Custom port
        api_key=api_key,
        language="fr",  # French
        multilingual=False,
        translate=False,
        enable_turn_detection=True,
        turn_detection_timeout=1.0  # Longer timeout
    )
    print("   - Host: wss://custom.talkscriber.com")
    print("   - Port: 9091")
    print("   - Language: French")
    print("   - Turn detection: True (1.0s timeout)")
    print()


def demonstrate_tts_configurations():
    """Demonstrate different TTS client configurations"""
    
    api_key = os.getenv("TALKSCRIBER_API_KEY")
    if not api_key:
        print("Error: Please set your TALKSCRIBER_API_KEY environment variable")
        return
    
    print("=== TTS Configuration Examples ===\n")
    
    # Configuration 1: Basic TTS with playback
    print("1. Basic TTS with Real-time Playback:")
    tts_basic = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text="Hello, this is basic TTS configuration.",
        speaker_name="tara",
        api_key=api_key,
        enable_playback=True,
        save_audio_path=None
    )
    print("   - Host: api.talkscriber.com")
    print("   - Port: 9099")
    print("   - Speaker: tara")
    print("   - Playback: Enabled")
    print("   - Save file: No")
    print()
    
    # Configuration 2: TTS with file saving
    print("2. TTS with File Saving:")
    tts_save = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text="This audio will be saved to a file.",
        speaker_name="tara",
        api_key=api_key,
        enable_playback=True,
        save_audio_path="output.wav"
    )
    print("   - Speaker: tara")
    print("   - Playback: Enabled")
    print("   - Save file: output.wav")
    print()
    
    # Configuration 3: Silent TTS (file only)
    print("3. Silent TTS (File Generation Only):")
    tts_silent = TalkScriberTTSClient(
        host="api.talkscriber.com",
        port=9099,
        text="This will be generated silently.",
        speaker_name="tara",
        api_key=api_key,
        enable_playback=False,  # No playback
        save_audio_path="silent_output.wav"
    )
    print("   - Speaker: tara")
    print("   - Playback: Disabled")
    print("   - Save file: silent_output.wav")
    print()
    
    # Configuration 4: Custom server with different voice
    print("4. Custom Server with Different Voice:")
    tts_custom = TalkScriberTTSClient(
        host="custom.tts.talkscriber.com",  # Custom host
        port=9098,  # Custom port
        text="This uses a custom server configuration.",
        speaker_name="custom_voice",  # Custom voice
        api_key=api_key,
        enable_playback=True,
        save_audio_path="custom_output.wav"
    )
    print("   - Host: custom.tts.talkscriber.com")
    print("   - Port: 9098")
    print("   - Speaker: custom_voice")
    print("   - Playback: Enabled")
    print("   - Save file: custom_output.wav")
    print()


def demonstrate_advanced_configurations():
    """Demonstrate advanced configuration patterns"""
    
    print("=== Advanced Configuration Patterns ===\n")
    
    # Pattern 1: Configuration class
    print("1. Configuration Class Pattern:")
    print("""
class TalkscriberConfig:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stt_host = "wss://api.talkscriber.com"
        self.stt_port = 9090
        self.tts_host = "api.talkscriber.com"
        self.tts_port = 9099
        self.default_language = "en"
        self.default_voice = "tara"
        self.enable_turn_detection = True
        self.turn_detection_timeout = 0.6
    
    def create_stt_client(self, **kwargs):
        return TranscriptionClient(
            host=self.stt_host,
            port=self.stt_port,
            api_key=self.api_key,
            language=kwargs.get('language', self.default_language),
            multilingual=kwargs.get('multilingual', False),
            translate=kwargs.get('translate', False),
            enable_turn_detection=kwargs.get('enable_turn_detection', self.enable_turn_detection),
            turn_detection_timeout=kwargs.get('turn_detection_timeout', self.turn_detection_timeout)
        )
    
    def create_tts_client(self, text, **kwargs):
        return TalkScriberTTSClient(
            host=self.tts_host,
            port=self.tts_port,
            text=text,
            speaker_name=kwargs.get('speaker_name', self.default_voice),
            api_key=self.api_key,
            enable_playback=kwargs.get('enable_playback', True),
            save_audio_path=kwargs.get('save_audio_path', None)
        )
""")
    print()
    
    # Pattern 2: Environment-based configuration
    print("2. Environment-based Configuration:")
    print("""
# Set environment variables for configuration
export TALKSCRIBER_STT_HOST="wss://api.talkscriber.com"
export TALKSCRIBER_STT_PORT="9090"
export TALKSCRIBER_TTS_HOST="api.talkscriber.com"
export TALKSCRIBER_TTS_PORT="9099"
export TALKSCRIBER_DEFAULT_LANGUAGE="en"
export TALKSCRIBER_DEFAULT_VOICE="tara"
export TALKSCRIBER_TURN_DETECTION="true"
export TALKSCRIBER_TURN_TIMEOUT="0.6"

# Use in code
stt_host = os.getenv("TALKSCRIBER_STT_HOST", "wss://api.talkscriber.com")
stt_port = int(os.getenv("TALKSCRIBER_STT_PORT", "9090"))
tts_host = os.getenv("TALKSCRIBER_TTS_HOST", "api.talkscriber.com")
tts_port = int(os.getenv("TALKSCRIBER_TTS_PORT", "9099"))
default_language = os.getenv("TALKSCRIBER_DEFAULT_LANGUAGE", "en")
default_voice = os.getenv("TALKSCRIBER_DEFAULT_VOICE", "tara")
enable_turn_detection = os.getenv("TALKSCRIBER_TURN_DETECTION", "true").lower() == "true"
turn_timeout = float(os.getenv("TALKSCRIBER_TURN_TIMEOUT", "0.6"))
""")
    print()
    
    # Pattern 3: Configuration file
    print("3. Configuration File Pattern:")
    print("""
# config.json
{
    "stt": {
        "host": "wss://api.talkscriber.com",
        "port": 9090,
        "default_language": "en",
        "multilingual": false,
        "translate": false,
        "enable_turn_detection": true,
        "turn_detection_timeout": 0.6
    },
    "tts": {
        "host": "api.talkscriber.com",
        "port": 9099,
        "default_voice": "tara",
        "enable_playback": true
    }
}

# Use in code
import json

with open('config.json', 'r') as f:
    config = json.load(f)

stt_client = TranscriptionClient(
    host=config['stt']['host'],
    port=config['stt']['port'],
    api_key=api_key,
    language=config['stt']['default_language'],
    multilingual=config['stt']['multilingual'],
    translate=config['stt']['translate'],
    enable_turn_detection=config['stt']['enable_turn_detection'],
    turn_detection_timeout=config['stt']['turn_detection_timeout']
)
""")


def main():
    """Main function"""
    
    print("Talkscriber Configuration Examples")
    print("==================================")
    print()
    
    # Check if API key is set
    if not os.getenv("TALKSCRIBER_API_KEY"):
        print("Note: TALKSCRIBER_API_KEY not set. Some examples will show configuration only.")
        print("Set your API key to test the actual configurations:")
        print("export TALKSCRIBER_API_KEY='your_api_key_here'")
        print()
    
    # Demonstrate different configurations
    demonstrate_stt_configurations()
    demonstrate_tts_configurations()
    demonstrate_advanced_configurations()
    
    print("=== Configuration Tips ===")
    print()
    print("1. Use environment variables for sensitive data (API keys)")
    print("2. Create configuration classes for reusable settings")
    print("3. Use configuration files for complex applications")
    print("4. Test different timeout values for turn detection")
    print("5. Experiment with different voices for TTS")
    print("6. Use multilingual mode for international applications")
    print("7. Enable translation for cross-language communication")
    print("8. Use silent TTS mode for batch processing")
    print("9. Save audio files for offline playback")
    print("10. Customize server endpoints for different environments")


if __name__ == "__main__":
    main()
