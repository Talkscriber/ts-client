import os
import wave
import threading
import textwrap
import json
import uuid
import time

try:
    import numpy as np
    import scipy
    import ffmpeg
    import pyaudio
    import websocket
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    # Create mock classes for when dependencies are not available
    class MockWebSocket:
        def __init__(self, *args, **kwargs): pass
        def send(self, *args, **kwargs): pass
        def close(self, *args, **kwargs): pass
    websocket = type('MockWebSocketModule', (), {'WebSocketApp': MockWebSocket})()
    class MockPyAudio:
        def __init__(self, *args, **kwargs): pass
        def open(self, *args, **kwargs): return type('MockStream', (), {'start_stream': lambda: None, 'stop_stream': lambda: None, 'close': lambda: None})()
        def terminate(self, *args, **kwargs): pass
        paInt16 = 8
    pyaudio = type('MockPyAudioModule', (), {'PyAudio': MockPyAudio, 'paInt16': 8})()

def resample_audio(input_file: str, new_sample_rate: int = 16000):
    """
    Open an audio file, read it as mono waveform, resample if needed,
    and save the modified audio file.
    """
    try:
        # Use ffmpeg to decode audio with resampling
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

class Client:
    """
    Manages audio recording, streaming, and WebSocket communication with server.
    """
    SESSIONS = {}

    def __init__(self, server_host=None, server_port=None, api_key=None, multilingual=False, language=None, translate=False, enable_turn_detection=False, turn_detection_timeout=0.6):
        """
        Initialize an AudioClient instance for recording and streaming audio.
        """
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required dependencies (numpy, scipy, ffmpeg-python, pyaudio, websocket-client) are not installed. Please install them with: pip install numpy scipy ffmpeg-python pyaudio websocket-client")
        self.audio_chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_channels = 1
        self.audio_rate = 16000
        self.max_record_time = 60000
        self.is_recording = False
        self.api_key = api_key
        self.multilingual = multilingual
        self.language = language
        self.task = "translate" if translate else "transcribe"
        self.enable_turn_detection = enable_turn_detection
        self.turn_detection_timeout = turn_detection_timeout
        self.session_id = str(uuid.uuid4())
        self.is_waiting = False
        self.last_server_response_time = None
        self.timeout_duration = 30
        self.time_offset = 0.0
        self.audio_data = None
        self.record_seconds = 60000
        self.pyaudio_instance = pyaudio.PyAudio()
        self.audio_stream = self.pyaudio_instance.open(
            format=self.audio_format,
            channels=self.audio_channels,
            rate=self.audio_rate,
            input=True,
            frames_per_buffer=self.audio_chunk_size,
        )

        if server_host is not None and server_port is not None:
            websocket_url = f"{server_host}:{server_port}"
            self.websocket_client = websocket.WebSocketApp(
                websocket_url,
                on_open=lambda ws: self.on_open(ws),
                on_message=lambda ws, message: self.on_message(ws, message),
                on_error=lambda ws, error: self.on_error(ws, error),
                on_close=lambda ws, status_code, msg: self.on_close(ws, status_code, msg),
            )
        else:
            print("[ERROR]: Server host or port not specified.")
            return

        Client.SESSIONS[self.session_id] = self

        # Start WebSocket thread
        self.websocket_thread = threading.Thread(target=self.websocket_client.run_forever)
        self.websocket_thread.setDaemon(True)
        self.websocket_thread.start()

        self.recorded_frames = b""
        print("[INFO]: * Starting recording")

    def write_audio_frames_to_file(self, frames, file_name):
        """
        Write audio frames to a WAV file.

        The WAV file is created or overwritten with the specified name. The audio frames should be
        in the correct format and match the specified channel, sample width, and sample rate.

        Args:
            frames (bytes): The audio frames to be written to the file.
            file_name (str): The name of the WAV file to which the frames will be written.

        """
        with wave.open(file_name, "wb") as wavfile:
            wavfile: wave.Wave_write
            wavfile.setnchannels(self.audio_channels)
            wavfile.setsampwidth(2)
            wavfile.setframerate(self.audio_rate)
            wavfile.writeframes(frames)

    def multicast_packet(self, packet, unconditional=False):
        """
        Sends an identical packet via all clients.

        Args:
            packet (bytes): The audio data packet in bytes to be sent.
            unconditional (bool, optional): If true, send regardless of whether clients are recording.  Default is False.
        """
        # for client in self.clients:
        # if (unconditional or self.recording):
        self.stream_audio_packet(packet)

    def write_output_recording(self, n_audio_file, out_file):
        """
        Combine and save recorded audio chunks into a single WAV file.

        The individual audio chunk files are expected to be located in the "chunks" directory. Reads each chunk
        file, appends its audio data to the final recording, and then deletes the chunk file. After combining
        and saving, the final recording is stored in the specified `out_file`.


        Args:
            n_audio_file (int): The number of audio chunk files to combine.
            out_file (str): The name of the output WAV file to save the final recording.

        """
        input_files = [
            f"chunks/{i}.wav"
            for i in range(n_audio_file)
            if os.path.exists(f"chunks/{i}.wav")
        ]
        with wave.open(out_file, "wb") as wavfile:
            wavfile: wave.Wave_write
            wavfile.setnchannels(self.audio_channels)
            wavfile.setsampwidth(2)
            wavfile.setframerate(self.audio_rate)
            for in_file in input_files:
                with wave.open(in_file, "rb") as wav_in:
                    while True:
                        data = wav_in.readframes(self.audio_chunk_size)
                        if data == b"":
                            break
                        wavfile.writeframes(data)
                # remove this file
                os.remove(in_file)
        wavfile.close()

    def record(self, out_file="output_recording.wav"):
        """
        Record audio data from the input stream and save it to a WAV file.

        Continuously records audio data from the input stream, sends it to the server via a WebSocket
        connection, and simultaneously saves it to multiple WAV files in chunks. It stops recording when
        the `RECORD_SECONDS` duration is reached or when the `RECORDING` flag is set to `False`.

        Audio data is saved in chunks to the "chunks" directory. Each chunk is saved as a separate WAV file.
        The recording will continue until the specified duration is reached or until the `RECORDING` flag is set to `False`.
        The recording process can be interrupted by sending a KeyboardInterrupt (e.g., pressing Ctrl+C). After recording,
        the method combines all the saved audio chunks into the specified `out_file`.

        Args:
            out_file (str, optional): The name of the output WAV file to save the entire recording.
                                      Default is "output_recording.wav".

        """
        n_audio_file = 0
        if not os.path.exists("chunks"):
            os.makedirs("chunks", exist_ok=True)
        try:
            for _ in range(0, int(self.audio_rate / self.audio_chunk_size * self.record_seconds)):
                # if not any(client.recording for client in self.clients):
                #     break
                data = self.audio_stream.read(self.audio_chunk_size, exception_on_overflow=False)
                self.recorded_frames += data

                audio_array = self.convert_bytes_to_float(data)

                self.multicast_packet(audio_array.tobytes())

                # save recorded_frames if more than a minute
                if len(self.recorded_frames) > 60 * self.audio_rate:
                    t = threading.Thread(
                        target=self.write_audio_frames_to_file,
                        args=(
                            self.recorded_frames[:],
                            f"chunks/{n_audio_file}.wav",
                        ),
                    )
                    t.start()
                    n_audio_file += 1
                    self.recorded_frames = b""
            # self.write_all_clients_srt()

        except KeyboardInterrupt:
            if len(self.recorded_frames):
                self.write_audio_frames_to_file(
                    self.recorded_frames[:], f"chunks/{n_audio_file}.wav"
                )
                n_audio_file += 1
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.pyaudio_instance.terminate()
            self.close_websocket_connection()

            self.write_output_recording(n_audio_file, out_file)
            # self.write_all_clients_srt()

    def on_message(self, ws, message):
        """
        Processes messages received from the server.
        """
        self.last_server_response_time = time.time()
        server_message = json.loads(message)

        if self.session_id != server_message.get("session_id"):
            # print("[ERROR]: Mismatched session ID")
            self.session_id = server_message.get("session_id")

        if "status" in server_message and server_message["status"] == "WAIT":
            self.is_waiting = True
            print(f"[INFO]: Server busy. Estimated wait: {round(server_message['info'])} minutes.")

        if "message" in server_message and server_message["message"] == "DISCONNECT":
            print("[INFO]: Server initiated disconnect.")
            self.is_recording = False

        if "message" in server_message and server_message["message"] == "SERVER_READY":
            self.is_recording = True
            return

        if "language" in server_message:
            self.selected_language = server_message.get("detected_language")
            language_confidence = server_message.get("language_confidence")
            print(f"[INFO]: Detected language {self.selected_language} with confidence {language_confidence}")
            return

        if "segments" not in server_message:
            return

        transcript_segments = server_message["segments"]
        transcript = []
        if len(transcript_segments):
            for segment in transcript_segments:
                if transcript and transcript[-1] == segment["text"]:
                    continue
                transcript.append(segment["text"])
        if len(transcript) > 3:
            transcript = transcript[-3:]
        text_wrapper = textwrap.TextWrapper(width=60)
        wrapped_text = text_wrapper.wrap(text="".join(transcript))
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        for line in wrapped_text:
            print(line)
        if 'segments' in message:
            segments = server_message['segments']
            last_segment = segments[-1] if segments else None
            if last_segment and last_segment['EOS']:
                print("[INFO]: --------End of speech detected----------")


    def on_error(self, ws, error):
        print(f"[ERROR]: WebSocket error: {error}")

    def on_close(self, ws, status_code, msg):
        print(f"[INFO]: WebSocket closed with status {status_code}: {msg}")

    def on_open(self, ws):
        """
        Handles the WebSocket connection opening.
        """
        print("[INFO]: Connection established")
        ws.send(
            json.dumps(
                {
                    "uid": self.session_id,
                    "multilingual": self.multilingual,
                    "language": self.language,
                    "task": self.task,
                    "auth": self.api_key,
                    "enable_turn_detection": self.enable_turn_detection,
                    "turn_detection_timeout": self.turn_detection_timeout
                }
            )
        )

    @staticmethod
    def convert_bytes_to_float(audio_bytes):
        """
        Converts byte audio data to a float array.
        """
        raw_audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        return raw_audio_data.astype(np.float32) / 32768.0

    def stream_audio_packet(self, audio_packet):
        """
        Streams an audio packet to the server.
        """
        try:
            self.websocket_client.send(audio_packet, websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            print(f"[ERROR]: Streaming error: {e}")

    def play_and_stream_audio(self, audio_file_path):
        """
        Plays and streams an audio file.
        """
        with wave.open(audio_file_path, "rb") as audio_file:
            self.audio_stream = self.pyaudio_instance.open(
                format=self.pyaudio_instance.get_format_from_width(audio_file.getsampwidth()),
                channels=audio_file.getnchannels(),
                rate=audio_file.getframerate(),
                input=True,
                output=True,
                frames_per_buffer=self.audio_chunk_size,
            )
            try:
                while self.is_recording:
                    data = audio_file.readframes(self.audio_chunk_size)
                    if data == b"":
                        break

                    float_audio_data = self.convert_bytes_to_float(data)
                    self.stream_audio_packet(float_audio_data.tobytes())
                    self.audio_stream.write(data)

                audio_file.close()
                assert self.last_server_response_time
                while time.time() - self.last_server_response_time < self.timeout_duration:
                    continue
                self.audio_stream.close()
                self.close_websocket_connection()

            except KeyboardInterrupt:
                audio_file.close()
                self.audio_stream.stop_stream()
                self.audio_stream.close()
                self.pyaudio_instance.terminate()
                self.close_websocket_connection()
                print("[INFO]: Recording stopped.")

    def close_websocket_connection(self):
        """
        Closes the WebSocket connection.
        """
        try:
            self.websocket_client.close()
        except Exception as e:
            print("[ERROR]: Closing WebSocket error:", e)

        try:
            self.websocket_thread.join()
        except Exception as e:
            print("[ERROR]: WebSocket thread join error:", e)


class TranscriptionClient:
    """
    Client for handling audio transcription tasks via a WebSocket connection.

    Acts as a high-level client for audio transcription tasks using a WebSocket connection. It can be used
    to send audio data for transcription to a server and receive transcribed text segments.

    Args:
        host (str): The hostname or IP address of the server.
        port (int): The port number to connect to on the server.
        multilingual (bool, optional): Indicates whether the transcription should support multiple languages (default is False).
        lang (str, optional): The primary language for transcription (used if `multilingual` is False). Default is None, which defaults to English ('en').
        translate (bool, optional): Indicates whether translation tasks are required (default is False).
        enable_turn_detection (bool, optional): Enables smart turn detection using ML model (default is False).
        turn_detection_timeout (float, optional): Timeout threshold for end-of-speech detection in seconds (default is 0.6).

    Attributes:
        client (Client): An instance of the underlying Client class responsible for handling the WebSocket connection.

    Example:
        To create a TranscriptionClient and start transcription on microphone audio:
        ```python
        transcription_client = TranscriptionClient(
            host="localhost", 
            port=9090, 
            multilingual=True, 
            translate=False,
            enable_turn_detection=True,
            turn_detection_timeout=0.6
        )
        transcription_client()
        ```
    """
    def __init__(self, host, port, api_key, multilingual=False, language=None, translate=False, enable_turn_detection=False, turn_detection_timeout=0.6):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required dependencies (numpy, scipy, ffmpeg-python, pyaudio, websocket-client) are not installed. Please install them with: pip install numpy scipy ffmpeg-python pyaudio websocket-client")
        self.client = Client(host, port, api_key, multilingual=multilingual, language=language, translate=translate, enable_turn_detection=enable_turn_detection, turn_detection_timeout=turn_detection_timeout)

    def __call__(self, audio=None):
        """
        Start the transcription process.

        Initiates the transcription process by connecting to the server via a WebSocket. It waits for the server
        to be ready to receive audio data and then sends audio for transcription. If an audio file is provided, it
        will be played and streamed to the server; otherwise, it will perform live recording.

        Args:
            audio (str, optional): Path to an audio file for transcription. Default is None, which triggers live recording.

        """
        print("[INFO]: Waiting for server ready ...")
        while not self.client.is_recording:
            if self.client.is_waiting:
                self.client.close_websocket()
                return
            pass
        print("[INFO]: Server Ready!")
        if audio is not None:
            resampled_file = resample_audio(audio)
            self.client.play_and_stream_audio(resampled_file)
        else:
            self.client.record()
