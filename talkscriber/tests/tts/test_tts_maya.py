#!/usr/bin/env python3
"""
Pytest tests for Talkscriber TTS Maya API
Tests basic functionality and various generation config options
"""

import pytest
from talkscriber.tts import TalkScriberTTSClient


@pytest.mark.integration
class TestTTSBasic:
    """Basic TTS functionality tests"""

    def test_basic_tts_with_default_settings(
        self, api_key, test_output_dir, tts_config_default
    ):
        """Test basic TTS with default Maya settings"""
        output_file = test_output_dir / "test_basic.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Hello, world! This is a test of the Maya text-to-speech API.",
            speaker_name="Realistic male voice in 30s with American accent",
            model=tts_config_default["model"],
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        # Run the test
        success = client.run_simple_test()

        # Assertions
        assert success, "TTS generation should succeed"
        assert output_file.exists(), "Output file should be created"
        assert output_file.stat().st_size > 0, "Output file should not be empty"

        # Check TTFT metrics
        ttft_metrics = client.get_ttft_metrics()
        assert ttft_metrics.get("ttft_ms") is not None, (
            "TTFT metrics should be available"
        )
        assert ttft_metrics["ttft_ms"] > 0, "TTFT should be positive"

        # Check audio info
        audio_info = client.get_audio_info()
        assert audio_info["chunks_count"] > 0, "Should have received audio chunks"
        assert audio_info["total_bytes"] > 0, "Should have received audio data"
        assert audio_info["duration_seconds"] > 0, "Audio should have duration"

    def test_tts_with_short_text(self, api_key, test_output_dir, tts_config_default):
        """Test TTS with very short text"""
        output_file = test_output_dir / "test_short.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Hi!",
            speaker_name="Friendly voice",
            model=tts_config_default["model"],
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Short text TTS should succeed"
        assert output_file.exists(), "Output file should be created"
        assert output_file.stat().st_size > 0, "Output file should contain data"

    def test_tts_with_long_text(self, api_key, test_output_dir, tts_config_default):
        """Test TTS with longer text"""
        output_file = test_output_dir / "test_long.wav"

        long_text = (
            "This is a longer test to verify that the TTS system can handle "
            "extended passages of text. The system should process this smoothly "
            "and generate high-quality audio output that maintains consistency "
            "throughout the entire passage."
        )

        client = TalkScriberTTSClient(
            api_key=api_key,
            text=long_text,
            speaker_name="Professional narrator",
            model=tts_config_default["model"],
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Long text TTS should succeed"
        assert output_file.exists(), "Output file should be created"

        audio_info = client.get_audio_info()
        assert audio_info["duration_seconds"] > 5, (
            "Long text should produce longer audio"
        )


@pytest.mark.integration
class TestMayaGenerationConfig:
    """Tests for different Maya generation configurations"""

    def test_conservative_config(
        self, api_key, test_output_dir, tts_config_default, maya_config_conservative
    ):
        """Test TTS with conservative generation config"""
        output_file = test_output_dir / "test_conservative.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This test uses conservative generation parameters for consistent output.",
            speaker_name="Clear and steady voice",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_conservative,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Conservative config TTS should succeed"
        assert output_file.exists(), "Output file should be created"

        # Verify config was used
        audio_info = client.get_audio_info()
        assert audio_info["chunks_count"] > 0, "Should generate audio"

    def test_expressive_config(
        self, api_key, test_output_dir, tts_config_default, maya_config_expressive
    ):
        """Test TTS with expressive generation config"""
        output_file = test_output_dir / "test_expressive.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This test uses expressive parameters for more varied and dynamic speech.",
            speaker_name="Energetic and expressive voice",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_expressive,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Expressive config TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_balanced_config(
        self, api_key, test_output_dir, tts_config_default, maya_config_balanced
    ):
        """Test TTS with balanced generation config"""
        output_file = test_output_dir / "test_balanced.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This test uses balanced parameters for natural sounding speech.",
            speaker_name="Natural conversational voice",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_balanced,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Balanced config TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_custom_temperature(self, api_key, test_output_dir, tts_config_default):
        """Test TTS with custom temperature setting"""
        output_file = test_output_dir / "test_custom_temp.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing custom temperature parameter.",
            speaker_name="Test voice",
            model=tts_config_default["model"],
            maya_generation_config={"temperature": 0.6},
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Custom temperature TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_custom_top_p(self, api_key, test_output_dir, tts_config_default):
        """Test TTS with custom top_p setting"""
        output_file = test_output_dir / "test_custom_top_p.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing custom top p parameter.",
            speaker_name="Test voice",
            model=tts_config_default["model"],
            maya_generation_config={"top_p": 0.88},
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Custom top_p TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_custom_repetition_penalty(
        self, api_key, test_output_dir, tts_config_default
    ):
        """Test TTS with custom repetition_penalty setting"""
        output_file = test_output_dir / "test_custom_rep_penalty.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing custom repetition penalty parameter.",
            speaker_name="Test voice",
            model=tts_config_default["model"],
            maya_generation_config={"repetition_penalty": 1.3},
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Custom repetition_penalty TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_all_parameters_combined(
        self, api_key, test_output_dir, tts_config_default
    ):
        """Test TTS with all generation parameters specified"""
        output_file = test_output_dir / "test_all_params.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing all generation parameters together.",
            speaker_name="Comprehensive test voice",
            model=tts_config_default["model"],
            maya_generation_config={
                "temperature": 0.75,
                "top_p": 0.92,
                "top_k": 55,
                "repetition_penalty": 1.18,
            },
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "All parameters TTS should succeed"
        assert output_file.exists(), "Output file should be created"


@pytest.mark.integration
class TestSpeakerDescriptions:
    """Tests for different speaker descriptions"""

    def test_male_voice(
        self, api_key, test_output_dir, tts_config_default, maya_config_balanced
    ):
        """Test with male voice description"""
        output_file = test_output_dir / "test_male_voice.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a test with a male voice description.",
            speaker_name="Realistic male voice in 30s with American accent",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_balanced,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Male voice TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_female_voice(
        self, api_key, test_output_dir, tts_config_default, maya_config_balanced
    ):
        """Test with female voice description"""
        output_file = test_output_dir / "test_female_voice.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a test with a female voice description.",
            speaker_name="Warm female voice with British accent",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_balanced,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Female voice TTS should succeed"
        assert output_file.exists(), "Output file should be created"

    def test_narrator_voice(
        self, api_key, test_output_dir, tts_config_default, maya_config_balanced
    ):
        """Test with narrator voice description"""
        output_file = test_output_dir / "test_narrator_voice.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="This is a test with a professional narrator voice.",
            speaker_name="Professional narrator voice with clear diction",
            model=tts_config_default["model"],
            maya_generation_config=maya_config_balanced,
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "Narrator voice TTS should succeed"
        assert output_file.exists(), "Output file should be created"


@pytest.mark.integration
class TestAudioMetrics:
    """Tests for audio metrics and information"""

    def test_ttft_measurement(self, api_key, test_output_dir, tts_config_default):
        """Test that TTFT (Time To First Token) is measured correctly"""
        output_file = test_output_dir / "test_ttft.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing time to first token measurement.",
            speaker_name="Test voice",
            model=tts_config_default["model"],
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "TTS should succeed"

        ttft_metrics = client.get_ttft_metrics()
        assert ttft_metrics["ttft_seconds"] is not None, (
            "TTFT seconds should be measured"
        )
        assert ttft_metrics["ttft_ms"] is not None, "TTFT ms should be measured"
        assert ttft_metrics["ttft_ms"] > 0, "TTFT should be positive"
        assert ttft_metrics["ttft_ms"] < 10000, "TTFT should be reasonable (< 10s)"

    def test_audio_info_accuracy(self, api_key, test_output_dir, tts_config_default):
        """Test that audio info is accurate"""
        output_file = test_output_dir / "test_audio_info.wav"

        client = TalkScriberTTSClient(
            api_key=api_key,
            text="Testing audio information accuracy.",
            speaker_name="Test voice",
            model=tts_config_default["model"],
            enable_playback=tts_config_default["enable_playback"],
            save_audio_path=str(output_file),
        )

        success = client.run_simple_test()

        assert success, "TTS should succeed"

        audio_info = client.get_audio_info()
        assert audio_info["chunks_count"] > 0, "Should have chunks"
        assert audio_info["total_bytes"] > 0, "Should have bytes"
        assert audio_info["duration_seconds"] > 0, "Should have duration"
        assert audio_info["sample_rate"] == 24000, "Sample rate should be 24kHz"
        assert audio_info["channels"] == 1, "Should be mono"
        assert audio_info["bits_per_sample"] == 16, "Should be 16-bit"

        # Check file size matches reported bytes (with WAV header)
        file_size = output_file.stat().st_size
        # WAV header is 44 bytes
        assert file_size == audio_info["total_bytes"] + 44, (
            "File size should match audio data + WAV header"
        )
