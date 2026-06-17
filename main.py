import sys
import anthropic
from elevenlabs import ElevenLabs, play

client = anthropic.Anthropic()
voice = ElevenLabs()

def ask(prompt: str) -> str:
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    audio = voice.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
        text=text,
        model_id="eleven_multilingual_v2",
    )
    play(audio)
    return text

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Ask: ")
    response = ask(prompt)
    print(f"\n{response}")
