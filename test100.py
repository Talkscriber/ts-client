from tsclient import TranscriptionClient

# Create the client instance
client = TranscriptionClient(
    api_key="your-api-key",
    host="wss://api.talkscriber.com",
    port=9090,
    multilingual=False,
    language="en",
    translate=False
)

# Start microphone
client.start_microphone()

try:
    # Read audio in a loop
    while True:
        audio_chunk = client.read_audio()
        # Process audio_chunk as needed
except KeyboardInterrupt:
    # Stop when Ctrl+C is pressed
    client.stop_microphone()