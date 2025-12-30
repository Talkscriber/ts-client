# TSClient - Talkscriber Python Client

[![PyPI version](https://badge.fury.io/py/tsclient.svg)](https://badge.fury.io/py/tsclient)
[![Python Support](https://img.shields.io/pypi/pyversions/tsclient.svg)](https://pypi.org/project/tsclient/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/tsclient)](https://pepy.tech/project/tsclient)
[![GitHub stars](https://img.shields.io/github/stars/Talkscriber/ts-client.svg)](https://github.com/Talkscriber/ts-client)

A comprehensive Python client library for Talkscriber's Live Transcription and Text-to-Speech services. This package provides easy-to-use APIs for real-time speech-to-text transcription and ultra-low latency text-to-speech conversion.

## Features

### Live Transcription
- Real-time speech-to-text transcription via WebSocket
- Support for 50+ languages
- Smart turn detection using ML models
- Emotion classification (text + audio) returned on end-of-utterance segments (always on)
- Translation capabilities
- File and microphone input support

### Text-to-Speech
- Ultra-low latency streaming (speech starts in <0.1 seconds)
- Real-time audio playback
- Multiple voice options
- Audio file saving
- Configurable buffering for optimal performance

## Installation

### Quick Install

```bash
pip install tsclient
```

### System Dependencies

The package requires some system-level dependencies for audio processing:

**macOS:**
```bash
# Install PortAudio (required for PyAudio)
brew install portaudio

# Then install the package
pip install tsclient
```

**Ubuntu/Debian:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install libasound2-dev portaudio19-dev python3-dev

# Then install the package
pip install tsclient
```

**Windows:**
```bash
# No additional setup required - just install the package
pip install tsclient
```

**CentOS/RHEL/Fedora:**
```bash
# Install system dependencies
sudo yum install portaudio-devel python3-devel
# or for newer versions:
sudo dnf install portaudio-devel python3-devel

# Then install the package
pip install tsclient
```

### Development Install

For development or to run examples:

```bash
git clone https://github.com/Talkscriber/ts-client.git
cd ts-client
pip install -e .
```

## Quick Start

### Get Your API Key

1. Visit [Talkscriber Dashboard](https://app.talkscriber.com)
2. Sign up or log in
3. Generate an API key
4. Set it as an environment variable:

```bash
export TALKSCRIBER_API_KEY="your_api_key_here"
```

### Live Transcription

```python
from talkscriber.stt import TranscriptionClient

# Initialize client
client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key="your_api_key",
    language="en"
)

# Start live transcription from microphone
client()

# Or transcribe from file
client("audio_file.wav")
```

### Text-to-Speech

```python
from talkscriber.tts import TalkScriberTTSClient

# Initialize TTS client
tts_client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="Hello, world!",
    model="TTS_MAYA"
)

# Generate and play speech
tts_client.run_simple_test()

# Advanced usage with generation config
tts_client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="Hello, world!",
    model="TTS_MAYA",
    maya_generation_config={
        "temperature": 0.8,
        "top_p": 0.9,
        "repetition_penalty": 1.2
    }
)
tts_client.run_simple_test()
```

## Command Line Interface

The package includes convenient CLI tools:

### Live Transcription CLI

```bash
# Transcribe from microphone (live streaming)
talkscriber-stt --api-key YOUR_KEY --language en

# Transcribe from file (live streaming)
talkscriber-stt --api-key YOUR_KEY --file audio.wav

# Enable multilingual detection
talkscriber-stt --api-key YOUR_KEY --multilingual

# Offline batch processing mode
talkscriber-stt --api-key YOUR_KEY --file audio.wav --offline

# Offline mode with translation
talkscriber-stt --api-key YOUR_KEY --file audio.wav --offline --translate
```

### Text-to-Speech CLI

```bash
# Basic TTS
talkscriber-tts --api-key YOUR_KEY --text "Hello, world!"

# Save to file
talkscriber-tts --api-key YOUR_KEY --text "Hello" --save output.wav

# Advanced: Control generation parameters
talkscriber-tts --api-key YOUR_KEY --text "Hello" --temperature 0.8 --top-p 0.9

# Full control with all parameters
talkscriber-tts --api-key YOUR_KEY --text "Hello" \
  --model TTS_MAYA \
  --temperature 0.8 \
  --top-p 0.9 \
  --top-k 50 \
  --repetition-penalty 1.2 \
  --save output.wav
```

## Transcription Modes

The client supports two transcription modes:

### Live Streaming Mode (Default)
- Real-time transcription via WebSocket
- Supports both microphone and file input
- Results appear as audio is processed
- Best for: Real-time applications, live conversations, immediate feedback

### Offline Batch Mode
- Submit audio file for processing via REST API
- File input only (no microphone support)
- Results appear after full processing completes
- Best for: Pre-recorded audio, batch processing, non-real-time workflows

To enable offline mode, use the `--offline` flag:

```bash
talkscriber-stt --api-key YOUR_KEY --file audio.wav --offline
```

**Note**: Offline mode requires the `--file` argument. Microphone input is not supported in offline mode.

## API Reference

### Live Transcription

#### TranscriptionClient

```python
TranscriptionClient(
    host: str,
    port: int,
    api_key: str,
    multilingual: bool = False,
    language: str = None,
    translate: bool = False,
    enable_turn_detection: bool = False,
    turn_detection_timeout: float = 0.6
)
```

**Parameters:**
- `host`: WebSocket host URL
- `port`: WebSocket port number
- `api_key`: Your Talkscriber API key
- `multilingual`: Enable auto language detection
- `language`: Language code (e.g., "en", "es", "fr")
- `translate`: Enable translation
- `enable_turn_detection`: Enable ML-based turn detection
- `turn_detection_timeout`: Timeout for turn detection

#### Transcription result: segment payload fields

When you receive streaming STT results over WebSocket, each `segment` may include additional metadata alongside `start`, `end`, `text`, etc.

**Emotion classification (always on):**

- `emotion`: **Text-based** emotion scores for the segment text. This is a dictionary mapping emotion name → score (float in \([0, 1]\)).
  - Text emotion labels: `anger`, `disgust`, `fear`, `joy`, `neutral`, `sadness`, `surprise`
- `emotion_audio`: **Audio-based** emotion scores computed from the audio corresponding to the segment. This is a dictionary mapping label → score (float in \([0, 1]\)).
  - Audio emotion labels: `neu`, `hap`, `ang`, `sad`
- These emotion fields are returned **alongside end-of-utterance segments**, i.e. when `EOS` is `true`. (They may be omitted on non-EOS partial segments.)

Example segment (truncated):

```json
{
  "start": 0,
  "end": 2.9978125,
  "text": "Hello can you hear me?",
  "emotion": {
    "anger": 0.02,
    "disgust": 0.01,
    "fear": 0.04,
    "joy": 0.02,
    "neutral": 0.72,
    "sadness": 0.02,
    "surprise": 0.17
  },
  "emotion_audio": {
    "sad": 0.47
  },
  "speaker_name": "-",
  "speaker_id": "0000",
  "EOS": true,
  "segment_id": 0
}
```

### Text-to-Speech

#### TalkScriberTTSClient

```python
TalkScriberTTSClient(
    host: str = "api.talkscriber.com",
    port: int = 9099,
    text: str,
    api_key: str,
    enable_playback: bool = True,
    save_audio_path: str = None,
    model: str = "TTS_MAYA",
    maya_generation_config: dict = None
)
```

**Parameters:**
- `host`: TTS server hostname
- `port`: TTS server port
- `text`: Text to convert to speech
- `api_key`: Your Talkscriber API key
- `enable_playback`: Enable real-time audio playback
- `save_audio_path`: Optional path to save audio file
- `model`: TTS model to use (default: "TTS_MAYA")
- `maya_generation_config`: Optional dict with generation parameters (see below)

**Maya Generation Config Options:**

The `maya_generation_config` parameter accepts a dictionary with the following optional keys:

- `temperature` (float): Controls randomness in generation. Higher values (e.g., 0.8-1.0) make output more varied and expressive, lower values (e.g., 0.3-0.5) make it more consistent and predictable. Range: 0.0-2.0, typical: 0.6-0.9
- `top_p` (float): Nucleus sampling parameter. Controls diversity by considering tokens with cumulative probability up to this value. Range: 0.0-1.0, typical: 0.85-0.95
- `top_k` (int): Limits sampling to the top K most likely tokens. Lower values make output more focused. Range: 1-100, typical: 40-60
- `max_tokens` (int): Maximum number of tokens to generate (controls output length)
- `repetition_penalty` (float): Penalizes repetitive speech patterns. Higher values (>1.0) reduce repetition. Range: 1.0-2.0, typical: 1.1-1.3

**Example with generation config:**

```python
client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="Hello, world!",
    model="TTS_MAYA",
    maya_generation_config={
        "temperature": 0.8,      # More expressive
        "top_p": 0.9,           # Diverse sampling
        "top_k": 50,            # Consider top 50 tokens
        "repetition_penalty": 1.2  # Reduce repetition
    }
)
```

## Maya Generation Configuration

The TTS client supports fine-grained control over speech generation through the `maya_generation_config` parameter. This allows you to customize the voice characteristics and generation behavior.

### Configuration Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `temperature` | float | 0.0-2.0 | 0.7 | Controls expressiveness and variation. Higher = more varied/expressive, Lower = more consistent/predictable |
| `top_p` | float | 0.0-1.0 | 0.9 | Nucleus sampling. Controls diversity by limiting to tokens with cumulative probability up to this value |
| `top_k` | int | 1-100 | 50 | Limits sampling to top K most likely tokens. Lower = more focused output |
| `max_tokens` | int | >0 | auto | Maximum number of tokens to generate (controls output length) |
| `repetition_penalty` | float | 1.0-2.0 | 1.0 | Penalizes repetitive patterns. Higher values reduce repetition |

### Usage Examples

**Consistent and Predictable Voice:**
```python
maya_generation_config={
    "temperature": 0.5,
    "top_p": 0.85,
    "repetition_penalty": 1.1
}
```

**Expressive and Varied Voice:**
```python
maya_generation_config={
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 60,
    "repetition_penalty": 1.2
}
```

**Focused and Natural Voice (Recommended):**
```python
maya_generation_config={
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.15
}
```

### CLI Usage

```bash
# Consistent voice
talkscriber-tts --api-key YOUR_KEY --text "Your text" \
  --temperature 0.5 --top-p 0.85 --repetition-penalty 1.1

# Expressive voice
talkscriber-tts --api-key YOUR_KEY --text "Your text" \
  --temperature 0.9 --top-p 0.95 --repetition-penalty 1.2
```

## Supported Languages

The client supports 50+ languages including English, Spanish, French, German, Chinese, Japanese, and many more. See the [full language list](https://docs.talkscriber.com/languages) in our documentation.

## Examples

Check out the `examples/` directory for comprehensive examples organized by category:

### Quick Start
```bash
# First, install the package
pip install tsclient

# Then run examples
# Interactive demo (recommended for beginners)
python examples/integration/comprehensive_demo.py

# Basic STT (microphone)
python examples/stt/basic.py

# Basic TTS (text-to-speech)
python examples/tts/basic.py
```

### Example Categories

**Speech-to-Text (STT):**
- **`stt/basic.py`** - Real-time microphone transcription
- **`stt/file.py`** - Transcribe audio files
- **`stt/multilingual.py`** - Automatic language detection

**Text-to-Speech (TTS):**
- **`tts/basic.py`** - Basic TTS with real-time playback
- **`tts/save_file.py`** - Generate and save audio files
- **`tts/silent.py`** - Silent TTS generation
- **`tts/different_voices.py`** - Multiple voice comparison
- **`tts/batch.py`** - Batch processing from text files

**Integration:**
- **`integration/stt_to_tts.py`** - Complete voice processing pipeline
- **`integration/comprehensive_demo.py`** - Interactive demo

**Configuration:**
- **`configuration/config_patterns.py`** - Configuration patterns and best practices

See the [examples README](examples/README.md) for detailed usage instructions and the complete directory structure.

## Documentation

- [Full Documentation](https://docs.talkscriber.com)
- [API Reference](https://docs.talkscriber.com/api)
- [Language Support](https://docs.talkscriber.com/languages)

## Links

- [Talkscriber Dashboard](https://app.talkscriber.com) - Get your API key
- [Official Website](https://talkscriber.com)
- [GitHub Repository](https://github.com/Talkscriber/ts-client)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

