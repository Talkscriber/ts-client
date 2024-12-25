import unittest
from ts_live.client import TranscriptionClient

class TestTranscriptionClient(unittest.TestCase):
    def setUp(self):
        self.client = TranscriptionClient(api_key="test_key")

    def test_initialization(self):
        self.assertEqual(self.client.host, "wss://api.talkscriber.com")
        self.assertEqual(self.client.port, 9090)
        self.assertEqual(self.client.api_key, "test_key")
        self.assertEqual(self.client.language, "en")
        self.assertEqual(self.client.multilingual, False)
        self.assertEqual(self.client.translate, True)

if __name__ == '__main__':
    unittest.main() 