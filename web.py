#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from dotenv import load_dotenv

from localchat.client import build_client, DEFAULT_MODEL
from localchat.session import SYSTEM_PROMPT

load_dotenv()
STATIC = Path(__file__).parent / "static"
client = build_client()

TYPES = {".html": "text/html", ".js": "application/javascript", ".css": "text/css"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        name = "index.html" if self.path in ("/", "") else self.path.lstrip("/")
        path = (STATIC / name).resolve()
        if STATIC not in path.parents or not path.is_file():
            self.send_error(404)
            return
        body = path.read_bytes()
        self._send(200, TYPES.get(path.suffix, "text/plain"), body)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        history = json.loads(self.rfile.read(length) or "{}").get("messages", [])
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        try:
            resp = client.chat.completions.create(
                model=DEFAULT_MODEL, messages=messages, temperature=0.6
            )
            payload = {"reply": resp.choices[0].message.content}
        except Exception as e:
            payload = {"error": str(e)}
        self._send(200, "application/json", json.dumps(payload).encode())

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("chat UI at http://localhost:8000  (ctrl-c to stop)")
    ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()
