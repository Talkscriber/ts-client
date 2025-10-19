# Talkscriber Examples

This directory contains comprehensive examples demonstrating how to use the Talkscriber Python client library for both Speech-to-Text (STT) and Text-to-Speech (TTS) services.

## Directory Structure

```
examples/
├── stt/                    # Speech-to-Text examples
│   ├── basic.py           # Basic microphone transcription
│   ├── file.py            # File transcription
│   ├── multilingual.py    # Auto language detection
│   └── README.md          # STT-specific documentation
├── tts/                    # Text-to-Speech examples
│   ├── basic.py           # Basic TTS with playback
│   ├── save_file.py       # TTS with file saving
│   ├── silent.py          # Silent TTS generation
│   ├── different_voices.py # Multiple voice comparison
│   ├── batch.py           # Batch processing
│   └── README.md          # TTS-specific documentation
├── integration/            # Integration examples
│   ├── stt_to_tts.py      # Complete voice pipeline
│   ├── comprehensive_demo.py # Interactive demo
│   └── README.md          # Integration documentation
├── configuration/          # Configuration examples
│   ├── config_patterns.py # Configuration patterns
│   └── README.md          # Configuration documentation
├── data/                   # Sample data files
│   └── sample_text.txt    # Sample text for batch processing
└── README.md              # This file
```

## Quick Start

### Prerequisites

1. **Install the package:**
   ```bash
   pip install tsclient
   ```

2. **Get your API key:**
   - Visit [Talkscriber Dashboard](https://app.talkscriber.com)
   - Sign up or log in
   - Generate an API key

3. **Set your API key as an environment variable:**
   ```bash
   export TALKSCRIBER_API_KEY="your_api_key_here"
   ```

### Quick Examples

**Start with the comprehensive demo:**
```bash
python examples/integration/comprehensive_demo.py
```

**Basic STT (microphone):**
```bash
python examples/stt/basic.py
```

**Basic TTS (text-to-speech):**
```bash
python examples/tts/basic.py
```

**Batch TTS processing:**
```bash
python examples/tts/batch.py --sample
```

## Example Categories

### Speech-to-Text (STT)
- **`stt/basic.py`** - Real-time microphone transcription
- **`stt/file.py`** - Transcribe audio files
- **`stt/multilingual.py`** - Automatic language detection

### Text-to-Speech (TTS)
- **`tts/basic.py`** - Basic TTS with real-time playback
- **`tts/save_file.py`** - Generate and save audio files
- **`tts/silent.py`** - Silent TTS generation
- **`tts/different_voices.py`** - Multiple voice comparison
- **`tts/batch.py`** - Batch processing from text files

### Integration
- **`integration/stt_to_tts.py`** - Complete voice processing pipeline
- **`integration/comprehensive_demo.py`** - Interactive demo

### Configuration
- **`configuration/config_patterns.py`** - Configuration patterns and best practices

## Example Outputs

### STT Examples
- **Live transcription:** Real-time text display as you speak
- **File transcription:** Complete transcription of audio files
- **Multilingual:** Language detection + transcription

### TTS Examples
- **Audio playback:** Real-time speech generation
- **File generation:** WAV files saved to disk
- **Voice comparison:** Multiple audio files with different voices

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   ```bash
   # macOS
   brew install portaudio
   pip install pyaudio
   
   # Ubuntu/Debian
   sudo apt-get install libasound2-dev portaudio19-dev
   pip install pyaudio
   
   # Windows
   pip install pyaudio
   ```

2. **"API key not set"**
   ```bash
   export TALKSCRIBER_API_KEY="your_actual_api_key"
   ```

3. **"Connection failed"**
   - Check your internet connection
   - Verify your API key is correct
   - Ensure the Talkscriber service is available

4. **"Audio device not found"**
   - Check your microphone/speaker settings
   - Ensure audio devices are not being used by other applications

### Getting Help

- **Documentation:** [https://docs.talkscriber.com](https://docs.talkscriber.com)
- **Dashboard:** [https://app.talkscriber.com](https://app.talkscriber.com)
- **Support:** Contact support through the dashboard

## Advanced Usage

### Custom Configuration

You can modify the examples to use different settings:

```python
# Custom STT client
client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=api_key,
    language="es",  # Spanish
    multilingual=False,
    translate=True,  # Translate to English
    enable_turn_detection=True,
    turn_detection_timeout=1.0
)

# Custom TTS client
tts_client = TalkScriberTTSClient(
    host="api.talkscriber.com",
    port=9099,
    text="Your custom text here",
    speaker_name="custom_voice",
    api_key=api_key,
    enable_playback=True,
    save_audio_path="custom_output.wav"
)
```

### Integration Examples

These examples can be integrated into larger applications:

- **Voice assistants:** Use STT for voice commands
- **Accessibility tools:** TTS for screen readers
- **Content creation:** Batch TTS generation
- **Language learning:** Multilingual transcription
- **Meeting transcription:** File-based STT processing
