# Arc 1 - "Brain in Jar" Demo
# It can help you to order but it cannot order directly

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\yende\Projects\Food Agent\.env")

llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = llm.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Please order a chicken biryani for me"}
    ]
)

print(f"AI: {response.choices[0].message.content}")
    