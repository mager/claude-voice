# claude-voice

A small voice agent: Claude thinks, ElevenLabs speaks it aloud in **Joe's**
voice. Single-shot or a full multi-turn conversation, streamed to your terminal
as it plays.

## Setup

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
cp .env.example .env
# fill in your API keys
```

## Usage

One-shot:

```bash
./venv/bin/python main.py "What's the weather like on Mars?"
```

Conversation (remembers the thread until you quit):

```bash
./venv/bin/python main.py
You: > What should I make for dinner tonight?
Joe: > ...
You: > something vegetarian
```

Type `exit`, `quit`, or Ctrl-C to leave.

## How it works

1. Your prompt goes to Claude (`claude-opus-4-8`) via the Anthropic SDK, with a
   system prompt that keeps answers short and natural for *speech* (no markdown,
   no bullet lists).
2. The response streams to your terminal, then goes to ElevenLabs TTS
   (voice: **Joe**, `sB7vwSCyX0tQmU24cW2C`).
3. Audio plays through your speakers via macOS `afplay` — no ffmpeg required.

## Keys

- `ANTHROPIC_API_KEY` — [console.anthropic.com](https://console.anthropic.com)
- `ELEVENLABS_API_KEY` — [elevenlabs.io](https://elevenlabs.io)

`.env` is gitignored — keep your keys out of version control.
