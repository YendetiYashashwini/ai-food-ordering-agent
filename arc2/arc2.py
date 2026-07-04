# Arc 2 - Amnesia Problem Demo
# LLM has no memory - every message is treated as a fresh conversation

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(r"c:\Users\yende\Projects\Food Agent\.env")

# Connect to Groq
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

while True:
    human_input = input("Human: ")

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # No history - only current message is sent
            # LLM has no idea what was said before
            {"role": "user", "content": human_input}
        ]
    )

    print(f"AI: {response.choices[0].message.content}")
    print()