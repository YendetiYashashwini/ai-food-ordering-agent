# Arc 2 - Amnesia Fix
# We store previous messages and send full history on every API call
# This way LLM remembers the entire conversation

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(r"c:\Users\yende\Projects\AI Food Ordering Agent\.env")

# Connect to Groq
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# This list stores the full conversation history
# Every user message and AI reply is saved here
messages = []

while True:
    human_input = input("Human: ")

    # Add user message to history
    messages.append({"role": "user", "content": human_input})

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        # Sending full history every time - this is the amnesia fix
        messages=messages
    )

    ai_response = response.choices[0].message.content

    # Add AI reply to history so it remembers what it said too
    messages.append({"role": "assistant", "content": ai_response})

    print(f"AI: {ai_response}")
    print()