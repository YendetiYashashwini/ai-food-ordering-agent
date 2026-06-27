# Arc 2 - Amnesia Fix
# We store previous messages and send history for each new call

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\yende\Projects\Food Agent\.env")

llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

messages = []  

while True:
    human_input = input("Human: ")
    messages.append({"role": "user", "content": human_input})  
    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages  
    )
    ai_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_response})  
    print(f"AI: {ai_response}")
    print()