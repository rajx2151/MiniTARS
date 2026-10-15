
from ollama import chat


MODEL = "qwen3:4b"


def ask_ollama(user_text):
    """Send a general conversation request to Ollama."""

    response = chat(
        model=MODEL,
        think=False,
        messages=[
            {
                "role": "system",
                "content": """
You are MiniTARS, a helpful AI assistant.

The physical MiniTARS commands are handled separately
by the Python tool system.

You are responsible only for general conversation,
questions, explanations, and casual interaction.

Do not pretend that you physically performed an action.
Keep responses concise because you are running on
limited hardware.
"""
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response["message"]["content"].strip()

