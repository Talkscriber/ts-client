# Talkscriber Test Suite

This directory contains the test suite for the Talkscriber Python client library.

## Prerequisites

1. Install test dependencies:
```bash
pip install -e ".[dev]"
```

2. Set up your API key:
```bash
export TALKSCRIBER_API_KEY="your_api_key_here"
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest talkscriber/tests/tts/test_tts_maya.py
```

### Run specific test class
```bash
pytest talkscriber/tests/tts/test_tts_maya.py::TestTTSBasic
```

### Run specific test
```bash
pytest talkscriber/tests/tts/test_tts_maya.py::TestTTSBasic::test_basic_tts_with_default_settings
```

### Run tests with markers
```bash
# Run only integration tests
pytest -m integration

# Run only unit tests
pytest -m unit

# Run tests excluding slow tests
pytest -m "not slow"
```

### Show test output (print statements)
```bash
pytest -s
```

### Generate coverage report
```bash
pip install pytest-cov
pytest --cov=talkscriber --cov-report=html
```

## Test Structure

```
talkscriber/tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared pytest fixtures and configuration
├── README.md                # This file
└── tts/
    ├── __init__.py          # TTS test package initialization
    └── test_tts_maya.py     # Maya TTS API tests
```

## Test Categories

### TTS Tests (`tts/test_tts_maya.py`)

**TestTTSBasic**: Basic TTS functionality tests
- `test_basic_tts_with_default_settings` - Basic TTS generation
- `test_tts_with_short_text` - Short text handling
- `test_tts_with_long_text` - Long text handling

**TestMayaGenerationConfig**: Maya generation configuration tests
- `test_conservative_config` - Conservative settings (consistent output)
- `test_expressive_config` - Expressive settings (varied output)
- `test_balanced_config` - Balanced settings (natural output)
- `test_custom_temperature` - Temperature parameter
- `test_custom_top_p` - Top-p parameter
- `test_custom_repetition_penalty` - Repetition penalty parameter
- `test_all_parameters_combined` - All parameters together

**TestSpeakerDescriptions**: Different speaker voice tests
- `test_male_voice` - Male voice description
- `test_female_voice` - Female voice description
- `test_narrator_voice` - Narrator voice description

**TestAudioMetrics**: Audio metrics and measurements
- `test_ttft_measurement` - Time To First Token measurement
- `test_audio_info_accuracy` - Audio metadata accuracy

## Fixtures

Available fixtures (defined in `conftest.py`):

- `api_key`: Provides API key from environment variable
- `test_output_dir`: Temporary directory for test output files
- `tts_config_default`: Default TTS configuration
- `maya_config_conservative`: Conservative generation config
- `maya_config_expressive`: Expressive generation config
- `maya_config_balanced`: Balanced generation config

## Test Configuration

The test configuration is defined in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["talkscriber/tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Notes

- All TTS tests are marked as `@pytest.mark.integration` as they require API access
- Audio playback is disabled during tests (files are saved only)
- Test output files are created in a temporary directory
- Tests automatically skip if `TALKSCRIBER_API_KEY` is not set

## Troubleshooting

### Tests are skipped
```
SKIPPED [1] talkscriber/tests/conftest.py:12: TALKSCRIBER_API_KEY environment variable not set
```
**Solution**: Set the `TALKSCRIBER_API_KEY` environment variable

### Import errors
**Solution**: Make sure you've installed the package in development mode:
```bash
pip install -e .
```

### Audio playback errors
**Solution**: Tests should not attempt audio playback. If you see playback errors, ensure `enable_playback=False` is set in test configurations.

## Contributing

When adding new tests:

1. Follow pytest naming conventions (`test_*.py`, `Test*`, `test_*`)
2. Use appropriate markers (`@pytest.mark.integration`, `@pytest.mark.unit`)
3. Add fixtures to `conftest.py` for shared test data
4. Disable audio playback in tests
5. Use temporary directories for output files
6. Add docstrings to explain what each test verifies

