import os
import wave
from typing import Optional, List
from pydantic import BaseModel, Field

import numpy as np
import scipy
import ffmpeg
import pyaudio
import threading
import textwrap
import json
import websocket
import uuid
import time

class AudioConfig(BaseModel):
    """Audio configuration settings."""
    chunk_size: int = Field(default=1024, description="Size of audio chunks to process")
    format: int = Field(default=pyaudio.paInt16, description="Audio format")
    channels: int = Field(default=1, description="Number of audio channels")
    rate: int = Field(default=16000, description="Sample rate in Hz")
    max_record_time: int = Field(default=60000, description="Maximum recording time in ms")

class ServerConfig(BaseModel):
    """Server connection configuration."""
    host: str = Field(..., description="WebSocket server host")
    port: int = Field(..., description="WebSocket server port")
    api_key: str = Field(..., description="API key for authentication")
    multilingual: bool = Field(default=False, description="Enable multilingual support")
    language: Optional[str] = Field(default="en", description="Target language code")
    translate: bool = Field(default=False, description="Enable translation")

class TranscriptionSegment(BaseModel):
    """Model for transcription segments."""
    text: str = Field(..., description="Transcribed text")
    start: float = Field(..., description="Start time of segment")
    end: float = Field(..., description="End time of segment")

class ServerMessage(BaseModel):
    """Model for server messages."""
    session_id: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    segments: Optional[List[TranscriptionSegment]] = None
    language: Optional[str] = None
    language_confidence: Optional[float] = None

class Client:
    """Manages audio recording, streaming, and WebSocket communication with server."""
    
    def __init__(self, config: ServerConfig):
        """Initialize client with configuration."""
        self.config = config
        self.audio_config = AudioConfig()
        self.session_id = str(uuid.uuid4())
        
        # State
        self.is_recording = False
        self.is_waiting = False
        self.last_server_response_time = None
        self.timeout_duration = 30
        self.recorded_frames = b""
        
        # Audio setup
        self.pyaudio_instance = pyaudio.PyAudio()
        self.audio_stream = self.pyaudio_instance.open(
            format=self.audio_config.format,
            channels=self.audio_config.channels,
            rate=self.audio_config.rate,
            input=True,
            frames_per_buffer=self.audio_config.chunk_size,
        )
        
        # WebSocket setup
        websocket_url = f"{config.host}:{config.port}"
        self.websocket_client = websocket.WebSocketApp(
            websocket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        
        # Start WebSocket thread
        self.websocket_thread = threading.Thread(target=self.websocket_client.run_forever)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()
        
        print("[INFO]: * Starting recording")

    def write_audio_frames_to_file(self, frames: bytes, file_name: str) -> None:
        """Write audio frames to a WAV file."""
        with wave.open(file_name, "wb") as wavfile:
            wavfile.setnchannels(self.audio_config.channels)
            wavfile.setsampwidth(2)
            wavfile.setframerate(self.audio_config.rate)
            wavfile.writeframes(frames)

    def stream_audio_packet(self, audio_packet: bytes) -> None:
        """Stream an audio packet to the server."""
        try:
            self.websocket_client.send(audio_packet, websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            print(f"[ERROR]: Streaming error: {e}")

    @staticmethod
    def convert_bytes_to_float(audio_bytes: bytes) -> np.ndarray:
        """Convert byte audio data to float array."""
        raw_audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        return raw_audio_data.astype(np.float32) / 32768.0

    def record(self, out_file: str = "output_recording.wav") -> None:
        """Record audio from microphone and stream to server."""
        n_audio_file = 0
        os.makedirs("chunks", exist_ok=True)
        
        try:
            while self.is_recording:
                data = self.audio_stream.read(self.audio_config.chunk_size, 
                                            exception_on_overflow=False)
                self.recorded_frames += data
                audio_array = self.convert_bytes_to_float(data)
                self.stream_audio_packet(audio_array.tobytes())
                
                if len(self.recorded_frames) > 60 * self.audio_config.rate:
                    threading.Thread(
                        target=self.write_audio_frames_to_file,
                        args=(self.recorded_frames[:], f"chunks/{n_audio_file}.wav")
                    ).start()
                    n_audio_file += 1
                    self.recorded_frames = b""
                    
        except KeyboardInterrupt:
            self._cleanup(n_audio_file, out_file)

    def _cleanup(self, n_audio_file: int, out_file: str) -> None:
        """Clean up resources and save recording."""
        if self.recorded_frames:
            self.write_audio_frames_to_file(
                self.recorded_frames[:], 
                f"chunks/{n_audio_file}.wav"
            )
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.pyaudio_instance.terminate()
        self.close_websocket_connection()
        self.write_output_recording(n_audio_file, out_file)

    def on_message(self, ws, message: str) -> None:
        """Handle incoming server messages."""
        self.last_server_response_time = time.time()
        try:
            server_message = ServerMessage.parse_raw(message)
            
            if server_message.session_id and server_message.session_id != self.session_id:
                self.session_id = server_message.session_id
                
            if server_message.status == "WAIT":
                self.is_waiting = True
                print(f"[INFO]: Server busy. Please wait...")
                
            if server_message.message == "DISCONNECT":
                print("[INFO]: Server initiated disconnect.")
                self.is_recording = False
                
            if server_message.message == "SERVER_READY":
                self.is_recording = True
                
            if server_message.segments:
                self._handle_transcription(server_message.segments)
                
        except Exception as e:
            print(f"[ERROR]: Message parsing error: {e}")

    def _handle_transcription(self, segments: List[TranscriptionSegment]) -> None:
        """Process and display transcription segments."""
        transcript = []
        for segment in segments:
            if not transcript or transcript[-1] != segment.text:
                transcript.append(segment.text)
                
        if len(transcript) > 3:
            transcript = transcript[-3:]
            
        text = "".join(transcript)
        wrapped_text = textwrap.wrap(text, width=60)
        
        os.system("cls" if os.name == "nt" else "clear")
        for line in wrapped_text:
            print(line)

    def on_error(self, ws, error) -> None:
        """Handle WebSocket errors."""
        print(f"[ERROR]: WebSocket error: {error}")

    def on_close(self, ws, status_code: int, msg: str) -> None:
        """Handle WebSocket connection close."""
        print(f"[INFO]: WebSocket closed with status {status_code}: {msg}")

    def on_open(self, ws) -> None:
        """Handle WebSocket connection open."""
        print("[INFO]: Connection established")
        auth_message = {
            "uid": self.session_id,
            "multilingual": self.config.multilingual,
            "language": self.config.language,
            "task": "translate" if self.config.translate else "transcribe",
            "auth": self.config.api_key
        }
        ws.send(json.dumps(auth_message))

class TranscriptionClient:
    """High-level client for audio transcription."""
    
    def __init__(self, host: str, port: int, api_key: str, 
                 multilingual: bool = False, language: str = "en", 
                 translate: bool = False):
        """Initialize transcription client."""
        config = ServerConfig(
            host=host,
            port=port,
            api_key=api_key,
            multilingual=multilingual,
            language=language,
            translate=translate
        )
        self.client = Client(config)

    def __call__(self, audio: Optional[str] = None) -> None:
        """Start transcription process."""
        print("[INFO]: Waiting for server ready ...")
        
        while not self.client.is_recording:
            if self.client.is_waiting:
                self.client.close_websocket_connection()
                return
                
        print("[INFO]: Server Ready!")
        
        if audio:
            resampled_file = resample_audio(audio)
            self.client.play_and_stream_audio(resampled_file)
        else:
            self.client.record()

def resample_audio(input_file: str, new_sample_rate: int = 16000) -> str:
    """Resample audio file to specified sample rate."""
    try:
        output, _ = (
            ffmpeg.input(input_file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=new_sample_rate)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Error loading audio: {e.stderr.decode()}") from e
        
    np_audio_buffer = np.frombuffer(output, dtype=np.int16)
    modified_audio_file = f"{input_file.split('.')[0]}_modified.wav"
    scipy.io.wavfile.write(modified_audio_file, new_sample_rate, np_audio_buffer.astype(np.int16))
    
    return modified_audio_file
