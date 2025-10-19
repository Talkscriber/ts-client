# Text-to-Speech (TTS) Examples

This directory contains examples demonstrating Talkscriber's text-to-speech capabilities.

## Examples

### 1. Basic TTS (`basic.py`)
Simple text-to-speech with real-time audio playback.

```bash
python examples/tts/basic.py
```

**Features:**
- Real-time audio playback
- Default voice (tara)
- Ultra-low latency streaming
- Audio information display

### 2. TTS with File Saving (`save_file.py`)
Generate speech and save it to an audio file.

```bash
python examples/tts/save_file.py
```

**Features:**
- Audio file generation (WAV format)
- Real-time playback + file saving
- File size and duration information
- Persistent audio storage

### 3. Silent TTS (`silent.py`)
Generate speech without audio playback (useful for batch processing).

```bash
python examples/tts/silent.py
```

**Features:**
- No audio playback
- File-only generation
- Batch processing friendly
- Silent operation

### 4. Different Voices (`different_voices.py`)
Generate the same text with multiple voices for comparison.

```bash
python examples/tts/different_voices.py
```

**Features:**
- Multiple voice generation
- Voice comparison
- Batch file generation
- Audio quality comparison

### 5. Batch Processing (`batch.py`)
Process multiple text inputs from a file in batch.

```bash
# Use your own text file
python examples/tts/batch.py input.txt

# Use sample text file
python examples/tts/batch.py --sample

# Custom options
python examples/tts/batch.py input.txt --voice tara --output-dir my_audio --delay 2.0
```

**Features:**
- Batch processing from text files
- Configurable voice and output settings
- Progress tracking and error handling
- Sample text file included

### 6. Comprehensive Test (`test-tts.py`)
Complete test suite for TTS functionality with interactive options.

```bash
python examples/tts/test-tts.py
```

**Features:**
- Import and instantiation tests
- CLI tools verification
- Interactive TTS generation (with/without audio)
- File saving tests
- Different voices testing
- Audio information retrieval
- Comprehensive error handling
- API key validation

## Prerequisites

Before running any TTS examples:

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
   - Ensure speakers/headphones are connected
   - Test audio output before running examples

## Configuration Options

### Voice Settings
- **Speaker**: Choose from available voices (default: "tara")
- **Custom voices**: Specify different speaker names

### Audio Output
- **Playback**: Enable/disable real-time audio playback
- **File saving**: Optional path to save generated audio
- **Format**: WAV format with 24kHz sample rate

### Server Settings
- **Host**: Default is `api.talkscriber.com`
- **Port**: Default is `9099`

### Batch Processing
- **Input file**: Text file with content to process
- **Output directory**: Where to save generated audio files
- **Delay**: Time between requests (avoid rate limiting)

## Example Outputs

### Basic TTS
- Real-time speech generation
- Audio information display
- Success/failure feedback

### File Generation
- WAV files saved to disk
- File size and duration information
- Persistent audio storage

### Batch Processing
- Multiple audio files generated
- Progress tracking
- Summary statistics

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
   - Check your speaker/headphone settings
   - Ensure audio output is not muted
   - Test audio in system settings

5. **"Choppy audio playback"**
   - Check system performance
   - Close other audio applications
   - Verify internet connection stability

### Getting Help

- **Documentation:** [https://docs.talkscriber.com](https://docs.talkscriber.com)
- **Dashboard:** [https://app.talkscriber.com](https://app.talkscriber.com)
- **Support:** Contact support through the dashboard
