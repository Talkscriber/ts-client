# TalkScriber Python TTS Client API Documentation

A comprehensive Python WebSocket client for connecting to TalkScriber TTS servers with real-time audio playback capabilities.

## Overview

The TalkScriber Python TTS Client provides a robust, easy-to-use interface for text-to-speech conversion with ultra-low latency streaming. Built with WebSocket technology, it delivers speech that starts in less than 0.1 seconds, providing near-instantaneous audio playback with configurable buffering for optimal user experience.

### Key Features

- **Ultra-Low Latency Streaming**: Speech starts in less than 0.1 seconds with real-time audio chunk processing
- **Configurable Buffering**: Adjustable buffer size for optimal latency vs. quality balance
- **Thread-Safe Audio**: Separate audio playback thread with proper synchronization
- **Multiple Output Options**: Support for real-time playback, file saving, or both
- **Flexible Configuration**: Customizable server settings, audio parameters, and speaker selection
- **Error Handling**: Comprehensive error handling and connection management
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Supported Audio Formats

- **Sample Rate**: 24kHz (matches server configuration)
- **Channels**: Mono (1 channel)
- **Bit Depth**: 16-bit PCM
- **Protocol**: WebSocket binary streaming

## Installation

Before diving into the API, let's make sure you have everything set up correctly. The installation process is straightforward and we'll cover the dependencies you need.

```bash
pip install -r requirements.txt
```

**PyAudio Installation Notes:**
- **macOS**: `brew install portaudio` then `pip install pyaudio`
- **Ubuntu/Debian**: `sudo apt-get install libasound2-dev portaudio19-dev` then `pip install pyaudio`
- **Windows**: `pip install pyaudio` (should work directly)

Now that you have the dependencies installed, let's get you started with a quick example to verify everything works.

## Quick Start

Ready to get started? Here's the simplest way to use the TalkScriber TTS client:

```python
from client.tts_client import TalkScriberTTSClient

# Basic usage
client = TalkScriberTTSClient(
    api_key="your_api_key_here",
    text="Hello, this is a test message.",
    speaker_name="tara"
)
success = client.run_simple_test()
```

**What to expect:** This example will connect to the TalkScriber TTS server, send a text message, and receive ultra-low latency audio streaming. You'll hear speech start in less than 0.1 seconds, with audio playing immediately as it's generated from the server.

## API Reference

Now that you've seen a quick example, let's dive into the complete API documentation. This section provides detailed documentation of the `TalkScriberTTSClient` class and all its methods. Understanding these will help you build more complex applications.

#### Constructor Parameters

```python
TalkScriberTTSClient(
    host="localhost",           # TTS server hostname
    port=9099,                 # TTS server port
    text="Hello, this is a test...",  # Default text to speak
    speaker_name="tara",       # Speaker voice to use
    api_key=None,              # Required API key for authentication
    enable_playback=True,      # Enable real-time audio playback
    save_audio_path=None       # Optional path to save audio file
)
```

#### Core Methods

Now let's examine each method in detail. These are the primary methods you'll use in your applications:
Runs a complete TTS session: connect, send text, receive audio, and play.

**Returns:** `bool` - True if successful, False otherwise

**Example:**
```python
client = TalkScriberTTSClient(
    api_key="your_key",
    text="Hello world!",
    speaker_name="tara"
)
success = client.run_simple_test()
```

##### `connect()`
Establishes WebSocket connection to the TTS server.

**Returns:** `bool` - True if connection successful

**Example:**
```python
if client.connect():
    print("Connected successfully")
else:
    print("Connection failed")
```

##### `disconnect()`
Closes the WebSocket connection and stops audio playback.

**Example:**
```python
client.disconnect()
```

##### `send_speak_request(text, speaker_name="tara")`
Sends a TTS request to the server.

**Parameters:**
- `text` (str): Text to convert to speech
- `speaker_name` (str): Voice to use (default: "tara")

**Returns:** `bool` - True if request sent successfully

**Note:** The `speaker_name` parameter is currently ignored - the client uses the `speaker_name` from the constructor.

**Example:**
```python
client.send_speak_request("Hello, how are you?")  # speaker_name parameter ignored
```

##### `init_audio()`
Initializes audio playback system.

**Returns:** `bool` - True if audio initialized successfully

**Example:**
```python
if client.init_audio():
    print("Audio system ready")
```

#### Audio Configuration

The client uses several audio configuration constants that you can adjust based on your needs:

## Usage Patterns

Now that you understand the API, let's explore different usage patterns. These examples show how to use the client in various scenarios, from simple one-shot operations to complex interactive applications.

```python
from client.tts_client import TalkScriberTTSClient

# Basic usage with default settings
client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="Hello, this is a simple test.",
    speaker_name="tara"
)
success = client.run_simple_test()
```

### 2. Silent Mode (No Audio Playback)

```python
# Useful for testing or when you only want to save audio
client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="This will be saved but not played.",
    enable_playback=False,
    save_audio_path="./output/silent_audio.wav"
)
success = client.run_simple_test()
```

### 3. Audio File Saving

```python
# Save audio to file with playback
client = TalkScriberTTSClient(
    api_key="your_api_key",
    text="This will be played and saved.",
    enable_playback=True,
    save_audio_path="./output/audio.wav"
)
success = client.run_simple_test()
```

## Configuration Options

Understanding the configuration options is crucial for optimizing performance. This section covers all the settings you can adjust to fine-tune the client behavior.

| Setting | Default | Description |
|---------|---------|-------------|
| `enable_playback` | `True` | Enable real-time audio playback |
| `BUFFER_SIZE_CHUNKS` | `5` | Number of audio chunks to buffer before playback |
| `SAMPLE_RATE` | `24000` | Audio sample rate (must match server) |


### Buffer Size Recommendations

Choosing the right buffer size is essential for balancing latency and audio quality. Here are our recommendations:

## Error Handling

Even with the best setup, you might encounter issues. This section provides guidance on handling common errors and debugging connection problems.

```python
try:
    client = TalkScriberTTSClient(api_key="your_key")
    success = client.run_simple_test()
    if not success:
        print("TTS operation failed")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Connection Issues

Connection problems are common in network applications. Here's how to diagnose and handle them:

## Troubleshooting

When things don't work as expected, this troubleshooting guide will help you identify and resolve common issues.
```python
# Verify PyAudio installation
import pyaudio
print("PyAudio OK")

# Check audio initialization
if client.init_audio():
    print("Audio system ready")
else:
    print("Audio initialization failed")
```

**Choppy audio:**
```python
# Increase buffer size for smoother playback
# Modify BUFFER_SIZE_CHUNKS in the client class
```

### Connection Issues

**WebSocket connection failed:**
- Verify server is running on correct host/port
- Check firewall settings
- Ensure API key is valid