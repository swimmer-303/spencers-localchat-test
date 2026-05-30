import os

from openai import OpenAI

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:30b")


def build_client(host=None):
    host = (host or HOST).rstrip("/")
    return OpenAI(base_url=host + "/v1", api_key="ollama")
