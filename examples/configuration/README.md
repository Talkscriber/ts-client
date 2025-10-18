# Configuration Examples

This directory contains examples demonstrating different configuration patterns and best practices for using the Talkscriber client library.

## Examples

### 1. Configuration Patterns (`config_patterns.py`)
Comprehensive examples of different configuration approaches.

```bash
python examples/configuration/config_patterns.py
```

**Features:**
- Multiple configuration patterns
- Environment variable usage
- Configuration classes and files
- Best practices and tips
- Real-world examples

## Configuration Patterns

### 1. Environment Variables
Use environment variables for sensitive data and configuration:

```bash
export TALKSCRIBER_API_KEY="your_api_key_here"
export TALKSCRIBER_STT_HOST="wss://api.talkscriber.com"
export TALKSCRIBER_STT_PORT="9090"
export TALKSCRIBER_TTS_HOST="api.talkscriber.com"
export TALKSCRIBER_TTS_PORT="9099"
export TALKSCRIBER_DEFAULT_LANGUAGE="en"
export TALKSCRIBER_DEFAULT_VOICE="tara"
```

### 2. Configuration Classes
Create reusable configuration classes:

```python
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
```

### 3. Configuration Files
Use JSON or YAML files for complex configurations:

```json
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
```

### 4. Factory Pattern
Create factory functions for different use cases:

```python
def create_production_config(api_key):
    """Production configuration with all features enabled"""
    return {
        'stt': {
            'host': 'wss://api.talkscriber.com',
            'port': 9090,
            'multilingual': True,
            'enable_turn_detection': True,
            'turn_detection_timeout': 0.6
        },
        'tts': {
            'host': 'api.talkscriber.com',
            'port': 9099,
            'enable_playback': True
        }
    }

def create_development_config(api_key):
    """Development configuration with debugging enabled"""
    return {
        'stt': {
            'host': 'wss://api.talkscriber.com',
            'port': 9090,
            'multilingual': False,
            'enable_turn_detection': False
        },
        'tts': {
            'host': 'api.talkscriber.com',
            'port': 9099,
            'enable_playback': False,
            'save_audio_path': 'debug_output.wav'
        }
    }
```

## Best Practices

### 1. Security
- Never hardcode API keys in source code
- Use environment variables for sensitive data
- Implement proper secret management in production

### 2. Environment-Specific Configuration
- Use different configurations for development, staging, and production
- Implement configuration validation
- Use configuration inheritance

### 3. Error Handling
- Validate configuration before creating clients
- Provide helpful error messages for missing configuration
- Implement fallback values where appropriate

### 4. Documentation
- Document all configuration options
- Provide examples for common use cases
- Include troubleshooting information

## Common Configuration Scenarios

### Development
- Local testing with file output
- Debugging enabled
- Minimal features for faster iteration

### Production
- Full feature set enabled
- Optimized for performance
- Proper error handling and logging

### Batch Processing
- Silent mode (no audio playback)
- File-based input/output
- Optimized for throughput

### Real-time Applications
- Low latency configuration
- Turn detection enabled
- Optimized for responsiveness

## Prerequisites

Before running configuration examples:

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

## Troubleshooting

### Common Issues

1. **Configuration not loading**
   - Check file paths and permissions
   - Validate JSON/YAML syntax
   - Ensure environment variables are set

2. **Missing required parameters**
   - Implement configuration validation
   - Provide helpful error messages
   - Use default values where appropriate

3. **Environment-specific issues**
   - Test configurations in target environment
   - Use environment detection
   - Implement proper fallbacks

### Getting Help

- **Documentation:** [https://docs.talkscriber.com](https://docs.talkscriber.com)
- **Dashboard:** [https://app.talkscriber.com](https://app.talkscriber.com)
- **Support:** Contact support through the dashboard
