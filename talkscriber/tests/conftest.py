"""
Pytest configuration and fixtures for Talkscriber tests
"""

import os
import pytest


@pytest.fixture(scope="session")
def api_key():
    """Fixture to get API key from environment variable"""
    key = os.getenv("TALKSCRIBER_API_KEY")
    if not key:
        pytest.skip("TALKSCRIBER_API_KEY environment variable not set")
    return key


@pytest.fixture(scope="session")
def test_output_dir(tmp_path_factory):
    """Fixture to create a temporary directory for test outputs"""
    output_dir = tmp_path_factory.mktemp("tts_test_outputs")
    return output_dir


@pytest.fixture
def tts_config_default():
    """Default TTS configuration"""
    return {
        "enable_playback": False,  # Disable playback for tests
        "model": "TTS_MAYA",
    }


@pytest.fixture
def maya_config_conservative():
    """Conservative Maya generation config"""
    return {"temperature": 0.5, "top_p": 0.85, "repetition_penalty": 1.1}


@pytest.fixture
def maya_config_expressive():
    """Expressive Maya generation config"""
    return {"temperature": 0.9, "top_p": 0.95, "top_k": 60, "repetition_penalty": 1.2}


@pytest.fixture
def maya_config_balanced():
    """Balanced Maya generation config"""
    return {"temperature": 0.7, "top_p": 0.9, "top_k": 50, "repetition_penalty": 1.15}
