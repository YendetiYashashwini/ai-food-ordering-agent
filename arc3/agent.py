# Arc 3 - main agent loop & system prompt
# Main agent loop - connects LLM with tools

from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from tools import search_meals, place_order, TOOL_DEFINITIONS

# Load API key
load_dotenv(r"c:\Users\yende\Projects\AI Food Ordering Agent\.env")

# Connect to Groq
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# System prompt - tells LLM how to behave
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
  - When calling place_order, quantity must always be an integer like 1, 2, 3 — never a string.
Always use ₹ for prices. Be friendly and concise."""

# Conversation history - starts with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("\n🍔 AI Food Ordering Agent — Type 'quit' to exit\n")

while True:
    human_input = input("You: ")

    if human_input.lower() == "quit":
        print("Goodbye! 👋")
        break

    messages.append({"role": "user", "content": human_input})

    # Inner loop - handles tool calls
    while True:
        response = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        ai_message = response.choices[0].message

        if ai_message.tool_calls:
            messages.append(ai_message)

            for tool_call in ai_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Run the correct tool
                if tool_name == "search_meals":
                    result = search_meals(**tool_args)
                elif tool_name == "place_order":
                    result = place_order(**tool_args)
                    print(result)  # Show formatted order confirmation
                else:
                    result = "Unknown tool"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            # Final answer
            print(f"\nAI: {ai_message.content}\n")
            break