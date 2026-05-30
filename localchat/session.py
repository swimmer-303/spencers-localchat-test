from openai import APIConnectionError

from .client import build_client, DEFAULT_MODEL

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer only what the user actually asked, "
    "and keep it short. Don't volunteer extra facts, tangents, or counts they "
    "didn't ask for. If you're unsure, say so instead of making something up."
)


def stream_reply(client, model, messages, temperature):
    out = []
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    for event in stream:
        delta = event.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            out.append(delta)
    print()
    return "".join(out)


def run(model=DEFAULT_MODEL, temperature=0.6):
    client = build_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"connected to {model}. /reset to clear, /exit to quit.\n")

    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user:
            continue
        if user == "/exit":
            break
        if user == "/reset":
            messages = messages[:1]
            print("(cleared)\n")
            continue

        messages.append({"role": "user", "content": user})
        print("bot> ", end="", flush=True)
        try:
            reply = stream_reply(client, model, messages, temperature)
        except APIConnectionError:
            messages.pop()
            print(f"\ncan't reach ollama. is it running? (ollama serve / ollama pull {model})\n")
            continue
        messages.append({"role": "assistant", "content": reply})
        print()
