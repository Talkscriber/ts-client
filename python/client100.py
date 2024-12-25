from ts_live.client import TranscriptionClient

# Initialize the TranscriptionClient with specific configuration:

# host: URL of the transcription service.
# port: Port number for the socket connection to the service.
# multilingual: Enables or disables support for AUTO language detection (based on the first 5 seconds of active audio).
# language: Language code for transcription (e.g., "en" for English, "zh" for Chinese, etc.).
# translate: Enable translation of transcribed text to another language.

# Configure the TranscriptionClient with your API key.

TS_API_KEY = "YOUR_API_KEY"  # Replace with your API key

client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=TS_API_KEY,
    multilingual=False,
    language="en",
    translate=True
)

# client('test.wav') # For file input
# OR
client() # For Mic input


