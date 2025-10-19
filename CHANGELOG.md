# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-18

### Added
- Initial release of TSClient (Talkscriber Python Client)
- **Live Transcription (STT)**
  - Real-time speech-to-text transcription via WebSocket
  - Support for 200+ languages
  - Smart turn detection using ML models
  - Translation capabilities
  - File and microphone input support
  - CLI tool: `talkscriber-stt`

- **Text-to-Speech (TTS)**
  - Ultra-low latency streaming (speech starts in <0.1 seconds)
  - Real-time audio playback
  - Multiple voice options
  - Audio file saving
  - Configurable buffering for optimal performance
  - CLI tool: `talkscriber-tts`

- **Comprehensive Examples**
  - Basic STT and TTS examples
  - File-based transcription
  - Multilingual support
  - Batch processing
  - Integration examples
  - Comprehensive test suites

- **Documentation**
  - Complete API reference
  - Installation instructions for multiple platforms
  - Troubleshooting guides
  - Example usage patterns

### Dependencies
- numpy>=1.21.0
- scipy>=1.7.0
- ffmpeg-python>=0.2.0
- PyAudio>=0.2.11
- websocket-client>=1.6.0
- websockets>=11.0.0
- loguru>=0.7.0

### System Requirements
- Python 3.8+
- PortAudio (for audio processing)
- Internet connection (for API access)

### Supported Platforms
- macOS (with Homebrew)
- Ubuntu/Debian
- CentOS/RHEL/Fedora
- Windows

## [Unreleased]

### Changed
- **Package Structure Reorganization**
  - Renamed `talkscriber.live` module to `talkscriber.stt` for clarity
  - Updated CLI tool from `talkscriber-live` to `talkscriber-stt`
  - Consolidated all functionality under `talkscriber/` package
  - Removed legacy duplicate directories (`/tts/`, `/python/`)
  - Updated all import statements and documentation

### Planned Features
- Additional voice options
- Enhanced error handling
- Performance optimizations
- More language support
- Advanced audio processing features
