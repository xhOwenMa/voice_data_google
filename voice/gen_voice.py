from pathlib import Path
from openai import OpenAI

client = OpenAI()


def generate_voice(text, path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(path)


def process_text_file(file_path):
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            line = line.strip()  # Remove any leading/trailing whitespace
            if line:  # Check if the line is not empty
                # Generate a unique file name for each entry
                voice_file_path = Path(__file__).parent / f"speech_{index}.mp3"
                generate_voice(line, voice_file_path)
                print(f"Generated speech for line {index}")


# Path to the text file containing the text entries
text_file_path = Path(__file__).parent / "voice_prompts.txt"
process_text_file(text_file_path)
