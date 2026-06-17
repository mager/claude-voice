# claude-voice

A minimal demo: Claude answers your question, then ElevenLabs speaks the response aloud.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in your API keys
```

## Usage

```bash
python main.py "What's the weather like on Mars?"
```

Or run interactively:

```bash
python main.py
Ask: > What should I make for dinner tonight?
```

## How it works

1. Your prompt goes to Claude (`claude-opus-4-8`) via the Anthropic SDK
2. The text response is passed to ElevenLabs TTS (voice: George)
3. Audio plays directly through your speakers

## Keys

- `ANTHROPIC_API_KEY` — [console.anthropic.com](https://console.anthropic.com)
- `ELEVENLABS_API_KEY` — [elevenlabs.io](https://elevenlabs.io)
