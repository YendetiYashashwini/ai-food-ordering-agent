# Arc 1 - "Brain in a Jar" Demo
# LLM without tools - it can talk but cannot take actions

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(r"c:\Users\yende\Projects\Food Agent\.env")

# Connect to Groq (LLM provider)
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Ask LLM to order food - it will refuse because it has no tools
response = llm.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Please order a chicken biryani for me"}
    ]
)

print(f"AI: {response.choices[0].message.content}")
    