# Integration Examples

This directory contains examples demonstrating integration patterns between Talkscriber's STT and TTS services.

## Examples

### 1. STT to TTS Pipeline (`stt_to_tts.py`)
Complete voice processing pipeline: Speech → Text → Processing → Speech.

```bash
python examples/integration/stt_to_tts.py
```

**Features:**
- Real-time speech transcription
- Text processing and modification
- Text-to-speech generation
- Complete voice processing workflow
- Customizable text processing logic

### 2. Comprehensive Demo (`comprehensive_demo.py`)
Interactive demo showcasing both STT and TTS capabilities.

```bash
python examples/integration/comprehensive_demo.py
```

**Features:**
- Interactive menu system
- Both STT and TTS examples
- File transcription example
- User-friendly interface
- Complete workflow demonstration

## Use Cases

### Voice Assistants
- Voice command processing
- Response generation
- Interactive conversations

### Content Creation
- Voice-to-text transcription
- Text processing and editing
- Audio content generation

### Accessibility Tools
- Screen reader integration
- Voice navigation
- Audio feedback systems

### Language Learning
- Pronunciation practice
- Language translation
- Interactive exercises

## Architecture Patterns

### Pipeline Pattern
```
Audio Input → STT → Text Processing → TTS → Audio Output
```

### Event-Driven Pattern
```
STT Events → Text Processing → TTS Events → Audio Playback
```

### Batch Processing Pattern
```
File Input → STT → Text Processing → TTS → File Output
```

## Configuration

### STT Configuration
```python
stt_client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=api_key,
    language="en",
    multilingual=False,
    translate=False,
    enable_turn_detection=True,
    turn_detection_timeout=0.6
)
```

### TTS Configuration
```python
tts_client = TalkScriberTTSClient(
    host="api.talkscriber.com",
    port=9099,
    text=processed_text,
    speaker_name="tara",
    api_key=api_key,
    enable_playback=True,
    save_audio_path=None
)
```

## Customization

### Text Processing
Modify the `process_text()` method in `stt_to_tts.py` to add your own logic:

```python
def process_text(self, text):
    """Custom text processing logic"""
    # Add your processing here:
    # - Text filtering
    # - Language translation
    # - Content modification
    # - Command processing
    # - Intent recognition
    
    processed_text = f"Processed: {text}"
    return processed_text
```

### Error Handling
Implement robust error handling for production use:

```python
try:
    # STT processing
    transcribed_text = self.transcribe_speech()
    if not transcribed_text:
        return False
    
    # Text processing
    processed_text = self.process_text(transcribed_text)
    
    # TTS processing
    success = self.generate_speech(processed_text)
    return success
    
except Exception as e:
    logger.error(f"Pipeline error: {e}")
    return False
```

## Prerequisites

Before running integration examples:

1. **Install the package:**
   ```bash
   pip install -e .
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
   - Ensure speakers/headphones are connected
   - Test both input and output before running

## Troubleshooting

### Common Issues

1. **Audio feedback loops**
   - Use headphones to prevent microphone picking up speaker output
   - Implement proper audio routing

2. **Processing delays**
   - Optimize text processing logic
   - Use appropriate timeouts
   - Consider async processing

3. **Memory usage**
   - Clear audio buffers between processing cycles
   - Implement proper cleanup
   - Monitor memory usage in long-running processes

### Getting Help

- **Documentation:** [https://docs.talkscriber.com](https://docs.talkscriber.com)
- **Dashboard:** [https://app.talkscriber.com](https://app.talkscriber.com)
- **Support:** Contact support through the dashboard
