from pathlib import Path
from openai import OpenAI

client = OpenAI()

speech_file_path = Path(__file__).parent / "voice/speech.mp3"


def generate_voice(path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!"
    )

    response.stream_to_file(path)


generate_voice(speech_file_path)
