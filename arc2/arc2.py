# Arc 2 - Amnesia Problem Demo
# LLM has no memory so, every msg is a new msg

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\yende\Projects\Food Agent\.env")

llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
while True:
    human_input = input("Human: ")
    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": human_input}
        ]
    )
    print(f"AI: {response.choices[0].message.content}")
    print()