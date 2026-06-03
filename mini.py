from ollama import chat

model_name = "qwen3.5:2b"

messages = [
    {
        "role": "system",
        "content": "You are the Joker in Gotham City."
    }
]

print(f"Local LLM Chatbot [model={model_name}]")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    stream = chat(
        model=model_name,
        messages=messages,
        stream=True,
    )

    assistant_text = ""

    print("Bot: ", end="", flush=True)

    for chunk in stream:
        piece = chunk.get("message", {}).get("content", "")
        if piece:
            assistant_text += piece
            print(piece, end="", flush=True)

    print("\n")

    messages.append({
        "role": "assistant",
        "content": assistant_text
    })