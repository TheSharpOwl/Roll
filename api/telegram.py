import json
import os
from http.server import BaseHTTPRequestHandler

import requests

HF_TOKEN = os.environ.get("HF_TOKEN", "")
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
MODEL = os.environ.get("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

HF_URL = "https://router.huggingface.co/v1/chat/completions"
GREETING = (
    "Hello, I am Roll, Ziad's AI Assistant. You can ask me about his "
    "experience and I will try to answer."
)
FALLBACK = "I cannot answer that, sorry."

# Loaded once per cold start.
_kb_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "about.md")
with open(_kb_path, encoding="utf-8") as f:
    KNOWLEDGE = f.read()

SYSTEM_PROMPT = (
    "You are Roll, Ziad's AI assistant. Answer questions about Ziad's experience "
    "using only the information below. Keep answers short. If the information "
    "does not cover the question, you can answer from your mind.\n\n" + KNOWLEDGE
)


def ask(question: str) -> str:
    resp = requests.post(
        HF_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={
            "model": MODEL,
            "max_tokens": 300,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        },
        timeout=8,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def send(chat_id: int, text: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=5,
    )


class handler(BaseHTTPRequestHandler):
    def _reply(self, status: int, body: bytes = b"ok") -> None:
        self.send_response(status)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._reply(200)

    def do_POST(self):
        if not WEBHOOK_SECRET or (
            self.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET
        ):
            return self._reply(403, b"forbidden")

        length = int(self.headers.get("Content-Length", 0))
        update = json.loads(self.rfile.read(length) or b"{}")
        message = update.get("message") or {}
        text = message.get("text")
        chat_id = (message.get("chat") or {}).get("id")

        if text and chat_id:
            if text.strip().startswith("/start"):
                answer = GREETING
            else:
                try:
                    answer = ask(text)
                except Exception as error:
                    print(f"HF request failed: {error}")
                    answer = FALLBACK
            send(chat_id, answer)

        # Always 200 so Telegram doesn't keep retrying the update.
        self._reply(200)
