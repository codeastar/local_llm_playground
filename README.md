# LLM Chat Bot - Getting Started

This is a local LLM chat bot program that runs on your machine using Ollama and Python.

This README is separated into 2 parts:

1. Run with native Ollama setup (recommended)
2. Run with Docker Compose

## Prerequisites

Before you can run the chat bot, you need to install two tools:

### 1. Install Ollama

Ollama allows you to run large language models locally.

- Download and install from: https://ollama.com
- Follow the installation instructions for your operating system

### 2. Install UV

UV is a fast Python package installer and runner.

- Install via pip:
  ```bash
  pip install uv
  ```
- Or follow the installation guide at: https://docs.astral.sh/uv/

## Part 1: Run with native Ollama setup (Recommended)

Native Ollama is recommended in this project because:

- The architecture is simpler (no container networking layer)
- It provides faster response time in this setup

### Step 1: Pull an Ollama Model

Start by pulling a language model. We use Qwen 3.5 4B model as our example:

```bash
ollama pull qwen3.5:4b
```

You can use model you prefer, just replace the model name after the command "pull". You can find available models from https://ollama.com/search.

### Step 2: Start Ollama

Run the Ollama server in the background:

```bash
ollama serve
```

This will start Ollama on `localhost:11434` by default.

### Step 3: Install Python Dependencies

Install the project's related Python libraries from `pyproject.toml`:

```bash
uv sync
```

### Step 4: Run the Chat Bot

In a new terminal window, run the program:

```bash
uv run main.py
```

Optional: pass a model explicitly (remember to pull the model from Ollama first):

```bash
uv run main.py qwen3.5:0.8b
```

## Part 2: Run with Docker Compose

This mode runs Ollama in Docker while keeping the Python app local.

Important note:

- This Docker Compose path has only been tested in a Windows environment
- In testing, there is a significant performance drawback compared with the native method due to OS restrictions

### Step 1: Create your environment file

```bash
cp .env.example .env
```

Edit `.env` and set:

- `OLLAMA_MODELS`: comma-separated models to download at startup (for example `qwen3.5:4b,granite4.1:3b`)
- `OLLAMA_MODEL`: default model for local Python app
- `OLLAMA_PORT`: host port to publish Ollama (default `11434`)
- `OLLAMA_KEEP_ALIVE`: how long a model stays loaded in the memory (default `5m`, 5 minutes)

### Step 2: Start Ollama + model preload in background

```bash
docker compose up -d
```

On the first run, model downloads can take a while depending on model size and network speed.

### Step 3: Run the chatbot locally (Python)

```bash
uv run main.py
```

This uses your local Python process and talks to Dockerized Ollama on `http://127.0.0.1:${OLLAMA_PORT}`.

### Step 4: Stop background services

```bash
docker compose down
```


## Notes

- Keep the Ollama server running in the background while using the chat bot
- You can switch between models by pulling different ones with `ollama pull <model name>` and either pass the model as an ar 