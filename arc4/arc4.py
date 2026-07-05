# Arc 4 - FastAPI Backend
# We are turning our Arc 3 terminal agent into an HTTP server
# Now anyone can send a message to /chat endpoint and get a response

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import sys

# This tells Python where to find our arc3 tools
sys.path.append(r"c:\Users\yende\Projects\AI Food Ordering Agent\arc3")

# Import tools and definitions from arc3
from tools import search_meals, place_order, TOOL_DEFINITIONS

# Load API key from .env file
load_dotenv(r"c:\Users\yende\Projects\AI Food Ordering Agent\.env")

# Connect to Groq
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Create the FastAPI app - this is our server
app = FastAPI()

# System prompt - tells LLM how to behave
# This is sent at the start of every new conversation
SYSTEM_PROMPT = """You are a smart food assistant — like Zomato, but powered by AI.
Help users find and order meals that match their nutritional and budget goals.
You have two tools:
  - search_meals : find meals that match protein/price/cuisine/diet constraints
  - place_order  : place an order once the user has chosen a meal
When listing meal options, use this format:
  🍽️ **Dish Name** — Restaurant Name
     Protein: Xg | Price: ₹X | ETA: X min | ⭐ rating
     Short description
IMPORTANT RULES — never break these:
  - After calling place_order, relay the EXACT restaurant name, dish name, ETA, and price
    from the tool result. Never invent or guess these values.
  - The ETA and restaurant name in your confirmation MUST match what the tool returned.
  - Never make up order details that differ from the tool response.
  - When calling search_meals, always use valid JSON format for arguments.
  - When calling place_order, quantity must always be an integer like 1, 2, 3 — never a string.
Always use ₹ for prices. Be friendly and concise."""

# This defines what the user must send in their request
# message - the new message from user
# messages - the full conversation history (empty by default)
class ChatRequest(BaseModel):
    message: str
    messages: list = []

# This is our main API route
# When anyone sends POST request to /chat, this function runs
@app.post("/chat")
def chat(request: ChatRequest):
    messages = []
    
    # Start with system prompt always
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    # Add only user/assistant messages from history (skip system/tool messages)
    for msg in request.messages:
        if isinstance(msg, dict) and msg.get("role") in ["user", "assistant"]:
            if isinstance(msg.get("content"), str):
                messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add new user message
    messages.append({"role": "user", "content": request.message})

    # Keep looping until LLM gives a final answer (no more tool calls)
    while True:
        response = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        ai_message = response.choices[0].message

        if ai_message.tool_calls:
            # LLM wants to call a tool
            messages.append(ai_message)

            for tool_call in ai_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Run the correct tool based on LLM's request
                if tool_name == "search_meals":
                    result = search_meals(**tool_args)
                elif tool_name == "place_order":
                    result = place_order(**tool_args)
                else:
                    result = "Unknown tool"

                # Send tool result back to LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            # LLM gave final answer - return it to the user
            return {
                "reply": ai_message.content,
                "messages": messages
            }