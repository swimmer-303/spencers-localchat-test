# localchat

terminal chat with a local LLM, running offline through ollama. no api key, no network.

defaults to llama3.1:8b which is fine on 16gb. swap with `--model` or `OLLAMA_MODEL`.

## setup

```bash
brew install ollama
ollama serve &
ollama pull llama3.1:8b

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## use

```bash
python chat.py
python ask.py "explain mixture of experts in a paragraph"
```

`/reset` clears history, `/exit` quits. `python chat.py --model llama3.2` for a smaller/faster one.
