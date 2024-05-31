# Talkscriber Client Setup

This README provides clear, step-by-step instructions on how to set up and run the Talkscriber client using a Conda environment. It's structured to be user-friendly, guiding a user from installing the required software, setting up the environment, installing dependencies, and finally, running the live client.

Follow these instructions to set up the Talkscriber client in a Conda environment.

## Prerequisites

- Anaconda or Miniconda installed on your machine. Visit [Anaconda's website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) for installation instructions.

## Setup Environment

1. **Create and Activate the Conda Environment:**
   - Open your terminal.
   - Create a new Conda environment with Python 3.9:
     ```bash
     conda create --name talkscriber python=3.9
     ```
   - Activate the newly created environment:
     ```bash
     conda activate talkscriber
     ```

2. **Install Required Packages:**
   - Ensure you are in the project directory where `requirements.txt` is located.
   - Install the necessary Python packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Client

### Authentication
To authenticate with the Talkscriber API, generate an API key from the [Talkscriber dashboard](https://app.talkscriber.com):

```python
from ts_live.client import TranscriptionClient

TS_API_KEY = "YOUR_API_KEY"  # Replace with your API key

client = TranscriptionClient(
    host="wss://api.talkscriber.com",
    port=9090,
    api_key=TS_API_KEY,
    multilingual=False,
    language="en",
    translate=True
)
```

### Supported Languages
For a list of supported languages, refer to the section below.

### Running the Client
The client.py can be run in two modes: mic and file.

#### Mic Input
To use the microphone for live transcription:

```python
client()  # For Mic input
```

#### File Input
To transcribe an audio file (let's call it test.wav):

```python
client('test.wav')  # For file input
```

- Run the client.py:

```bash
python client.py
```

- See `client.py` for specific configuration details before running.

## Conclusion
That's it! You are now connected to the Talkscriber API and receiving live transcriptions. For more advanced features and detailed API references, check out the official documentation.


## Supported Languages

The client supports the following language codes:

```python
LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
    "yue": "cantonese",
}
```