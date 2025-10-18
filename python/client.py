from ts_live.client import TranscriptionClient

# Initialize the TranscriptionClient with specific configuration:

# host: URL of the transcription service.
# port: Port number for the socket connection to the service.
# multilingual: Enables or disables support for AUTO language detection (based on the first 5 seconds of active audio).
# language: Language code for transcription (e.g., "en" for English, "zh" for Chinese, etc.).
# translate: Enable translation of transcribed text to another language.
# enable_turn_detection: Enables smart turn detection using ML model for better endpoint detection.
# turn_detection_timeout: Timeout threshold for end-of-speech detection in seconds (fallback when ML model confidence is low).

# Configure the TranscriptionClient with your API key.

TS_API_KEY = "YOUR_API_KEY"  # Replace with your API key

client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=TS_API_KEY,
    multilingual=False,
    language="en",
    translate=False,
    enable_turn_detection=False,
    turn_detection_timeout=0.6
)

# client('test.wav') # For file input
# OR
client() # For Mic input


