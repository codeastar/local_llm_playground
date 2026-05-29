from ollama import chat
from dotenv import load_dotenv
import argparse
import os
import threading
import time
from urllib.error import URLError
from urllib.request import urlopen

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful, concise chatbot. "
    "Answer clearly and ask follow-up questions when useful."
)


def get_ollama_base_url():
    host = os.getenv("OLLAMA_HOST")
    if host:
        return host.rstrip("/")

    port = os.getenv("OLLAMA_PORT", "11434")
    host = f"http://127.0.0.1:{port}"
    return host.rstrip("/")


def is_ollama_running(timeout=1.5):
    tags_url = f"{get_ollama_base_url()}/api/tags"
    try:
        with urlopen(tags_url, timeout=timeout) as response:
            return response.status == 200
    except URLError:
        return False


def show_thinking_timer(stop_event):
    start = time.perf_counter()
    while not stop_event.is_set():
        elapsed = time.perf_counter() - start
        print(f"\rBot is thinking... {elapsed:0.1f}s", end="", flush=True)
        stop_event.wait(0.1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "model",
        nargs="?",
        default=os.getenv("OLLAMA_MODEL", "qwen3.5:4b"),
        help="Ollama model name to use, defaults to OLLAMA_MODEL from .env",
    )
    return parser.parse_args()


def run_chatbot(model_name):
    keep_alive = os.getenv("OLLAMA_KEEP_ALIVE", "24h")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print(f"Local LLM Chatbot [model={model_name}]")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        stop_event = threading.Event()
        timer_thread = threading.Thread(
            target=show_thinking_timer,
            args=(stop_event,),
            daemon=True,
        )
        timer_thread.start()
        thinking_start = time.perf_counter()
        thinking_time = None

        assistant_text = ""
        started_output = False

        stream = chat(
            model=model_name,
            messages=messages,
            stream=True,
            keep_alive=keep_alive,
        )

        for chunk in stream:
            piece = chunk.get("message", {}).get("content", "")
            if piece and not started_output:
                thinking_time = time.perf_counter() - thinking_start
                stop_event.set()
                timer_thread.join()
                print("\r" + " " * 40 + "\rBot: ", end="", flush=True)
                started_output = True
            if piece:
                assistant_text += piece
                print(piece, end="", flush=True)

        if not started_output:
            thinking_time = time.perf_counter() - thinking_start
            stop_event.set()
            timer_thread.join()
            print("\r" + " " * 40 + "\rBot: ", end="", flush=True)

        print(f"\nThinking time: {thinking_time:0.2f}s\n")
        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    args = parse_args()

    if not is_ollama_running():
        print(f"Ollama is not running on {get_ollama_base_url()}.")
        print("Start it with: ollama serve")
    else:
        run_chatbot(args.model)