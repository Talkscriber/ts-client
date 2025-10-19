# Speech-to-Text (STT) Examples

This directory contains examples demonstrating Talkscriber's live transcription capabilities.

## Examples

### 1. Basic STT (`basic.py`)
Simple real-time transcription from microphone input.

```bash
python examples/stt/basic.py
```

**Features:**
- Real-time microphone transcription
- English language
- Smart turn detection
- Live transcription display

### 2. File Transcription (`file.py`)
Transcribe an audio file instead of live microphone input.

```bash
python examples/stt/file.py path/to/audio_file.wav
```

**Features:**
- File-based transcription
- Configurable language
- Optional multilingual detection
- Optional translation
- Command-line arguments

### 3. Multilingual STT (`multilingual.py`)
Automatic language detection and transcription.

```bash
python examples/stt/multilingual.py
```

**Features:**
- Automatic language detection
- Support for 200+ languages
- Real-time language identification
- No need to specify language

### 4. Comprehensive Test (`test.py`)
Complete test suite for STT functionality with interactive options.

```bash
python examples/stt/test.py
```

**Features:**
- Import and instantiation tests
- CLI tools verification
- Interactive microphone transcription
- File-based transcription testing
- Multiple configuration testing
- Graceful error handling
- API key validation

## Prerequisites

Before running any STT examples:

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

4. **Audio setup:**
   - Ensure microphone access is granted
   - Test your microphone before running examples

## Configuration Options

### Language Settings
- **Single language**: Set `language="en"` and `multilingual=False`
- **Multilingual**: Set `multilingual=True` (language parameter ignored)
- **Translation**: Set `translate=True` to translate to English

### Turn Detection
- **Enable**: Set `enable_turn_detection=True`
- **Timeout**: Adjust `turn_detection_timeout` (default: 0.6 seconds)

### Server Settings
- **Host**: Default is `wss://api.talkscriber.com`
- **Port**: Default is `9090`

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
   - Check your microphone settings
   - Ensure microphone is not being used by other applications
   - Test microphone in system audio settings

### Getting Help

- **Documentation:** [https://docs.talkscriber.com](https://docs.talkscriber.com)
- **Dashboard:** [https://app.talkscriber.com](https://app.talkscriber.com)
- **Support:** Contact support through the dashboard
