#!/usr/bin/env python3
import sys

from dotenv import load_dotenv

from localchat.client import build_client, DEFAULT_MODEL

if len(sys.argv) < 2:
    sys.exit('usage: python ask.py "your prompt"')

load_dotenv()
client = build_client()
resp = client.chat.completions.create(
    model=DEFAULT_MODEL,
    messages=[{"role": "user", "content": " ".join(sys.argv[1:])}],
)
print(resp.choices[0].message.content)
