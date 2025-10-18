#!/usr/bin/env python3
"""
Simple Python WebSocket Client for TTS Server
Connects to the WebSocket server and receives audio tokens
Plays audio in real-time with buffering (optional)
Saves audio to file (optional)
"""

import json
import os
import threading
import time
import uuid
from collections import deque

try:
    import pyaudio
    import websocket
    from loguru import logger
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    # Create a mock logger for when dependencies are not available
    class MockLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    logger = MockLogger()

# Audio Configuration
BUFFER_SIZE_CHUNKS = 5  # Number of chunks to buffer before starting playback
SAMPLE_RATE = 24000    # 24kHz sample rate (must match server)
CHANNELS = 1           # Mono audio
BITS_PER_SAMPLE = 16   # 16-bit audio
BYTES_PER_SAMPLE = BITS_PER_SAMPLE // 8

class TalkScriberTTSClient:
    def __init__(self, host="api.talkscriber.com", port=9099, text="Hello, this is a test of the text-to-speech system.", speaker_name="tara", api_key=None, enable_playback=True, save_audio_path=None):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required dependencies (pyaudio, websocket-client, loguru) are not installed. Please install them with: pip install pyaudio websocket-client loguru")
        
        self.server_host = host
        self.server_port = port
        self.websocket_url = f"wss://{host}:{port}"
        self.websocket_client = None
        self.is_connected = False
        self.chunks_received = 0
        self.total_bytes = 0
        self.api_key = api_key
        self.speaker_name = speaker_name
        self.text = text
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        # Audio playback settings
        self.enable_playback = enable_playback
        self.save_audio_path = save_audio_path
        
        # Audio playback components (only initialized if playback is enabled)
        self.audio = None
        self.audio_stream = None
        self.audio_buffer = deque()
        self.is_playing = False
        self.playback_thread = None
        self.stop_playback = False
        self.buffer_lock = threading.Lock()
        self.generation_complete = False
        self.session_id = str(uuid.uuid4())
        
        # Audio storage components
        self.audio_chunks_for_storage = []
        self.storage_lock = threading.Lock()
        
        # Connection event callbacks
        self.on_open_callback = None
        self.on_message_callback = None
        self.on_error_callback = None
        self.on_close_callback = None
        
        # Log configuration
        if self.enable_playback:
            logger.info("Audio playback enabled")
        else:
            logger.info("Audio playback disabled")
            
        logger.info("Audio will be stored in memory")
        if self.save_audio_path:
            logger.info(f"Audio will also be saved to: {self.save_audio_path}")
    
    def set_callbacks(self, on_open=None, on_message=None, on_error=None, on_close=None):
        """Set connection event callbacks"""
        self.on_open_callback = on_open
        self.on_message_callback = on_message
        self.on_error_callback = on_error
        self.on_close_callback = on_close
    
    def connect(self):
        """Connect to the WebSocket server"""
        try:
            logger.info(f"Connecting to TTS server at {self.websocket_url}")
            
            self.websocket_client = websocket.WebSocketApp(
                self.websocket_url,
                on_open=lambda ws: self.on_open(ws),
                on_message=lambda ws, message: self.on_message(ws, message),
                on_error=lambda ws, error: self.on_error(ws, error),
                on_close=lambda ws, status_code, msg: self.on_close(ws, status_code, msg),
            )
            
            # Start WebSocket connection in a separate thread
            self.websocket_thread = threading.Thread(target=self.websocket_client.run_forever, daemon=True)
            self.websocket_thread.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the WebSocket server"""
        # Stop audio playback first
        if self.enable_playback:
            self.stop_audio_playback()
        
        if self.websocket_client:
            self.websocket_client.close()
            self.is_connected = False
            logger.info("Disconnected from TTS server")
    
    def send_json(self, data):
        """Send JSON message to server"""
        if not self.websocket_client or not self.is_connected:
            logger.error("Not connected to server")
            return False
        
        try:
            message = json.dumps(data)
            self.websocket_client.send(message)
            logger.debug(f"Sent JSON: {message}")
            return True
        except Exception as e:
            logger.error(f"Error sending JSON: {e}")
            return False
    
    def send_speak_request(self, text, speaker_name="tara"):
        """Send a speak request to generate TTS audio"""
        if not self.is_connected:
            logger.error("Not connected to server")
            return False
        
        speak_message = {
            "type": "speak",
            "text": text,
            "speaker": self.speaker_name
        }
        
        logger.info(f"Sending speak request for text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        return self.send_json(speak_message)
    
    def on_open(self, ws):
        """WebSocket on_open callback"""
        logger.info("WebSocket connection opened")
        self.is_connected = True
        
        # Send authentication message
        auth_message = {
            "uid": self.session_id,
            "auth": self.api_key,
            "type": "tts",
            "speaker_name": self.speaker_name,
            "text": self.text
        }
        self.send_json(auth_message)
        logger.info("Authentication message sent")
        
        # Call user callback if set
        if self.on_open_callback:
            try:
                self.on_open_callback(ws)
            except Exception as e:
                logger.error(f"Error in on_open callback: {e}")
    
    def on_message(self, ws, message):
        """WebSocket on_message callback"""
        try:
            # Call user callback if set
            if self.on_message_callback:
                try:
                    self.on_message_callback(ws, message)
                except Exception as e:
                    logger.error(f"Error in on_message callback: {e}")
            
            # Handle the message
            self.handle_message(message)
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def on_error(self, ws, error):
        """WebSocket on_error callback"""
        logger.error(f"WebSocket error: {error}")
        self.is_connected = False
        
        # Call user callback if set
        if self.on_error_callback:
            try:
                self.on_error_callback(ws, error)
            except Exception as e:
                logger.error(f"Error in on_error callback: {e}")
    
    def on_close(self, ws, status_code, msg):
        """WebSocket on_close callback"""
        logger.info(f"WebSocket connection closed: {status_code} - {msg}")
        self.is_connected = False
        
        # Call user callback if set
        if self.on_close_callback:
            try:
                self.on_close_callback(ws, status_code, msg)
            except Exception as e:
                logger.error(f"Error in on_close callback: {e}")
    
    def init_audio(self):
        """Initialize PyAudio for real-time playback"""
        if not self.enable_playback:
            logger.info("Audio playback disabled, skipping audio initialization")
            return True
            
        try:
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                format=pyaudio.paInt16,  # 16-bit
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                output=True,
                frames_per_buffer=1024  # Small buffer for low latency
            )
            logger.info(f"Audio initialized: {SAMPLE_RATE}Hz, {CHANNELS} channel(s), {BITS_PER_SAMPLE}-bit")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize audio: {e}")
            return False
    
    def stop_audio_playback(self):
        """Stop audio playback and cleanup"""
        if not self.enable_playback:
            return
            
        self.stop_playback = True
        
        # Wait for playback thread to finish
        if self.playback_thread and self.playback_thread.is_alive():
            logger.info("Stopping audio playback thread...")
            self.playback_thread.join(timeout=2.0)
        
        # Close audio stream
        if self.audio_stream:
            try:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            except Exception as e:
                logger.warning(f"Error closing audio stream: {e}")
            self.audio_stream = None
        
        # Close PyAudio
        if self.audio:
            try:
                self.audio.terminate()
            except Exception as e:
                logger.warning(f"Error terminating PyAudio: {e}")
            self.audio = None
        
        self.is_playing = False
        logger.info("Audio playback stopped and cleaned up")
    
    def start_audio_playback(self):
        """Start the audio playback thread"""
        if not self.enable_playback:
            return
            
        if not self.is_playing and self.audio_stream:
            self.stop_playback = False
            self.is_playing = True
            self.playback_thread = threading.Thread(target=self._audio_playback_worker, daemon=True)
            self.playback_thread.start()
            logger.info("Audio playback thread started")
    
    def _audio_playback_worker(self):
        """Audio playback worker thread"""
        logger.info("Audio playback worker started")
        
        try:
            while not self.stop_playback:
                chunk_data = None
                
                # Get chunk from buffer (thread-safe)
                with self.buffer_lock:
                    if self.audio_buffer:
                        chunk_data = self.audio_buffer.popleft()
                
                if chunk_data:
                    try:
                        # Play the audio chunk
                        self.audio_stream.write(chunk_data)
                    except Exception as e:
                        logger.error(f"Error playing audio chunk: {e}")
                        break
                else:
                    # No data available, sleep briefly to avoid busy waiting
                    time.sleep(0.01)
                    
        except Exception as e:
            logger.error(f"Audio playback worker error: {e}")
        finally:
            self.is_playing = False
            logger.info("Audio playback worker finished")
    
    def save_audio_to_file(self):
        """Save collected audio chunks to file as WAV format"""
        if not self.save_audio_path or not self.audio_chunks_for_storage:
            return False
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.save_audio_path), exist_ok=True)
            
            # Combine all audio chunks
            with self.storage_lock:
                combined_audio = b''.join(self.audio_chunks_for_storage)
            
            # Create WAV file with proper headers
            with open(self.save_audio_path, 'wb') as f:
                # WAV file header
                # RIFF header
                f.write(b'RIFF')
                file_size = len(combined_audio) + 36  # 36 bytes for WAV header
                f.write(file_size.to_bytes(4, 'little'))
                f.write(b'WAVE')
                
                # fmt chunk
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))  # fmt chunk size
                f.write((1).to_bytes(2, 'little'))   # PCM format
                f.write(CHANNELS.to_bytes(2, 'little'))  # number of channels
                f.write(SAMPLE_RATE.to_bytes(4, 'little'))  # sample rate
                byte_rate = SAMPLE_RATE * CHANNELS * BITS_PER_SAMPLE // 8
                f.write(byte_rate.to_bytes(4, 'little'))  # byte rate
                block_align = CHANNELS * BITS_PER_SAMPLE // 8
                f.write(block_align.to_bytes(2, 'little'))  # block align
                f.write(BITS_PER_SAMPLE.to_bytes(2, 'little'))  # bits per sample
                
                # data chunk
                f.write(b'data')
                f.write(len(combined_audio).to_bytes(4, 'little'))  # data size
                f.write(combined_audio)  # audio data
            
            logger.info(f"Audio saved to: {self.save_audio_path} ({len(combined_audio):,} bytes, WAV format)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save audio to file: {e}")
            return False
    
    def handle_message(self, message):
        """Handle incoming messages from server"""
        try:
            # Check if message is binary (audio data) or text (JSON)
            if isinstance(message, bytes):
                # Handle binary audio chunk
                self.handle_audio_chunk(message)
            else:
                # Handle JSON message
                try:
                    data = json.loads(message)
                    self.handle_json_message(data)
                except json.JSONDecodeError:
                    logger.warning(f"Received non-JSON text message: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def handle_audio_chunk(self, chunk):
        """Handle incoming audio chunk"""
        self.chunks_received += 1
        self.total_bytes += len(chunk)
        
        logger.info(f"Received audio chunk #{self.chunks_received}: {len(chunk)} bytes (total: {self.total_bytes:,} bytes)")
        
        # Always store audio chunk in memory
        with self.storage_lock:
            self.audio_chunks_for_storage.append(chunk)
        
        # Add chunk to audio buffer for playback (if enabled)
        if self.enable_playback:
            with self.buffer_lock:
                self.audio_buffer.append(chunk)
                buffer_size = len(self.audio_buffer)
            
            # Start playback if we have enough buffered chunks and aren't playing yet
            if buffer_size >= BUFFER_SIZE_CHUNKS and not self.is_playing:
                logger.info(f"Buffer filled ({buffer_size} chunks), starting audio playback...")
                self.start_audio_playback()
            elif buffer_size == 1 and not self.is_playing:
                logger.info(f"First chunk buffered, waiting for {BUFFER_SIZE_CHUNKS} chunks before starting playback...")
            
            # Log buffer status periodically
            if self.chunks_received % 10 == 0:
                logger.debug(f"Audio buffer status: {buffer_size} chunks buffered, playing: {self.is_playing}")
    
    def handle_json_message(self, data):
        """Handle incoming JSON messages"""
        message_type = data.get("type", "unknown")
        logger.debug(f"Received JSON message: {message_type}")
        
        if message_type == "server_ready":
            logger.info("Server confirmed ready for TTS")
        
        elif message_type == "audio_complete":
            logger.info(f"Audio generation completed! Received {self.chunks_received} chunks, {self.total_bytes:,} total bytes")
            
            # Save audio to file if path is provided
            if self.save_audio_path:
                self.save_audio_to_file()
            
            if self.enable_playback:
                logger.info("Audio generation finished - letting buffered audio finish playing...")
                self.generation_complete = True
                
                # Wait for buffer to drain while playing
                if self.is_playing:
                    buffer_size = len(self.audio_buffer)
                    if buffer_size > 0:
                        logger.info(f"Waiting for {buffer_size} remaining chunks to play...")
                        # Note: We don't stop playback here - let it drain naturally
            else:
                self.generation_complete = True
                logger.info("Audio generation completed (no playback)")
        
        elif message_type == "error":
            error_msg = data.get("message", "Unknown error")
            logger.error(f"Server error: {error_msg}")
        
        elif message_type == "stop_confirmed":
            logger.info(f"Stop confirmed: {data.get('message', 'Generation stopped')}")
        
        else:
            logger.debug(f"Received message type '{message_type}': {data}")
    
    def run_simple_test(self):
        """Run a simple test - connect, send text, receive and play audio"""
        # Reset counters and audio state
        self.chunks_received = 0
        self.total_bytes = 0
        self.generation_complete = False
        
        # Clear audio storage
        with self.storage_lock:
            self.audio_chunks_for_storage.clear()
        
        if self.enable_playback:
            self.stop_audio_playback()  # Clean up any previous audio session
            
            # Clear audio buffer
            with self.buffer_lock:
                self.audio_buffer.clear()
            
            # Initialize audio
            if not self.init_audio():
                logger.error("Failed to initialize audio - cannot play audio")
                return False
        
        # Connect to server
        if not self.connect():
            return False
        
        try:
            # Wait for connection to establish
            timeout_count = 0
            while not self.is_connected and timeout_count < 50:  # 5 seconds timeout
                time.sleep(0.1)
                timeout_count += 1
            
            if not self.is_connected:
                logger.error("Failed to connect within timeout")
                return False
            
            # Wait a moment for connection to stabilize
            time.sleep(0.5)
            
            # Send speak request
            if self.send_speak_request(self.text):
                logger.info("Speak request sent, waiting for audio chunks...")
                
                # Wait for audio generation to complete
                timeout_count = 0
                max_timeout = 300  # 30 seconds max
                
                while not self.generation_complete and timeout_count < max_timeout:
                    time.sleep(0.1)
                    timeout_count += 1
                
                if timeout_count >= max_timeout:
                    logger.warning("Timeout waiting for audio completion")
                else:
                    logger.info("Audio generation completed")
                
                # Wait for audio buffer to drain (let remaining audio play)
                if self.enable_playback and self.is_playing:
                    logger.info("Waiting for remaining audio to finish playing...")
                    max_wait = 100  # 10 seconds max
                    wait_count = 0
                    while len(self.audio_buffer) > 0 and wait_count < max_wait:
                        time.sleep(0.1)
                        wait_count += 1
                    
                    if len(self.audio_buffer) > 0:
                        logger.warning(f"Audio buffer still has {len(self.audio_buffer)} chunks after waiting")
                    else:
                        logger.info("All audio chunks played successfully")
            else:
                logger.error("Failed to send speak request")
        
        finally:
            self.disconnect()
        
        return True
    
    def get_stored_audio_data(self):
        """Get the raw audio data that was received during generation"""
        with self.storage_lock:
            return b''.join(self.audio_chunks_for_storage)
    
    def get_audio_chunks(self):
        """Get the list of audio chunks that were received"""
        with self.storage_lock:
            return self.audio_chunks_for_storage.copy()
    
    def get_audio_info(self):
        """Get information about the received audio"""
        with self.storage_lock:
            total_bytes = sum(len(chunk) for chunk in self.audio_chunks_for_storage)
            return {
                'chunks_count': len(self.audio_chunks_for_storage),
                'total_bytes': total_bytes,
                'duration_seconds': total_bytes / (SAMPLE_RATE * CHANNELS * BITS_PER_SAMPLE // 8),
                'sample_rate': SAMPLE_RATE,
                'channels': CHANNELS,
                'bits_per_sample': BITS_PER_SAMPLE
            }