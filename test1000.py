from ts_live.client import TranscriptionClient

TS_API_KEY = 'M4nEMzJoHHBeGumXRInIhR1u9P87NeCqzbS2fK3dijs'
client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=TS_API_KEY,
    multilingual=False,
    language="en",
    translate=False
)

f_name = '/Users/aramfaghfouri/Downloads/output.wav'
f_name = '/Users/aramfaghfouri/Downloads/audio.wav'
f_name = '/Users/aramfaghfouri/Downloads/tts_result/jenny.wav'
u = client(f_name)