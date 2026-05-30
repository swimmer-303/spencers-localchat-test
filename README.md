# localchat

terminal chat with a local LLM, running offline through ollama. no api key, no network.

defaults to gpt-oss:20b (20b MoE, ~14gb). runs on 16gb and it's smarter than the 8b, but
slow-ish: ~3 tok/s and a slow cold start. want speed instead? `--model llama3.1:8b`.

(tried qwen3:30b first. 19gb on 16gb ram = computer basically froze. then dropped to gpt-oss
which actually fits. lesson learned.)

## setup

```bash
brew install ollama
ollama serve &
ollama pull gpt-oss:20b

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## use

```bash
python chat.py
python ask.py "explain mixture of experts in a paragraph"
```

`/reset` clears history, `/exit` quits. `python chat.py --model llama3.2` for a smaller/faster one.

## web ui

```bash
python web.py
```

then open http://localhost:8000. renders the bot's answers as markdown. markdown lib is vendored in static/ so it works offline too.
