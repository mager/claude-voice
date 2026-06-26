"""Claude voice agent — Claude thinks, ElevenLabs (Joe) speaks.

Run interactively for a multi-turn conversation, or pass a prompt as args for
a single-shot answer:

    python main.py                      # conversation loop
    python main.py "Why is the sky blue?"   # one-shot
"""

import os
import sys
import tempfile
import subprocess

import anthropic
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

MODEL = "claude-opus-4-8"
# Joe — warm, nature-documentary narrator. He's a Voice Library voice, so the
# ElevenLabs API only allows him on a paid plan. Override VOICE_ID in .env to a
# premade voice (e.g. George, JBFqnCBsd6RMkjVDRZzb) to run on the free plan.
VOICE_ID = os.environ.get("VOICE_ID", "sB7vwSCyX0tQmU24cW2C")
TTS_MODEL = "eleven_multilingual_v2"

SYSTEM_PROMPT = (
    "You are a voice assistant. Your replies are spoken aloud, not read on a "
    "screen, so keep them concise and conversational — usually one to three "
    "sentences. Never use markdown, bullet points, code blocks, or symbols that "
    "don't read naturally when spoken aloud. If a question genuinely needs depth, "
    "give the short answer first, then offer to go deeper."
)

for _key in ("ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY"):
    if not os.environ.get(_key):
        sys.exit(f"Missing {_key}. Copy .env.example to .env and fill it in.")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
voice = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])


def speak(text: str) -> None:
    """Synthesize `text` as Joe and play it through the speakers via afplay."""
    audio = voice.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=TTS_MODEL,
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)
        path = f.name
    try:
        subprocess.run(["afplay", path], check=True)
    finally:
        os.unlink(path)


def reply(history: list) -> str:
    """Stream Claude's response to the terminal and return the full text."""
    print("Joe: ", end="", flush=True)
    text = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    ) as stream:
        for delta in stream.text_stream:
            print(delta, end="", flush=True)
            text += delta
    print("\n")
    return text


def main() -> None:
    history: list = []

    one_shot = " ".join(sys.argv[1:]).strip()
    if one_shot:
        history.append({"role": "user", "content": one_shot})
        speak(reply(history))
        return

    print("Claude voice agent — narrated by Joe. Type 'exit' or Ctrl-C to quit.\n")
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit", "bye"}:
            print("Goodbye.")
            break
        history.append({"role": "user", "content": prompt})
        answer = reply(history)
        history.append({"role": "assistant", "content": answer})
        speak(answer)


if __name__ == "__main__":
    main()
