# Arc 3 - Food Ordering Agent
# We give tools to the LLM so it can take real actions
# Without tools - LLM can only talk. With tools - it can actually order food.

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(r"c:\Users\yende\Projects\AI Food Ordering Agent\.env")

# Connect to Groq
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---- DATA ----
# Restaurant menu with nutrition and pricing info

RESTAURANTS = [
    {
        "id": 1,
        "name": "FitBite",
        "dish": "Grilled Chicken Bowl",
        "description": "Tender grilled chicken with quinoa, broccoli and tahini sauce",
        "protein_g": 42,
        "calories": 480,
        "price": 249,
        "rating": 4.5,
        "eta_min": 25,
        "cuisine": "Healthy",
        "tags": ["high-protein", "gluten-free"],
    },
    {
        "id": 2,
        "name": "NutriBowl",
        "dish": "Paneer Tikka Wrap",
        "description": "Marinated paneer tikka in a whole-wheat wrap with mint chutney",
        "protein_g": 28,
        "calories": 420,
        "price": 199,
        "rating": 4.2,
        "eta_min": 20,
        "cuisine": "Indian",
        "tags": ["vegetarian", "high-protein"],
    },
    {
        "id": 3,
        "name": "HealthyGrill",
        "dish": "Egg White Scramble Plate",
        "description": "6-egg white scramble with sautéed mushrooms, spinach and multigrain toast",
        "protein_g": 35,
        "calories": 320,
        "price": 179,
        "rating": 4.0,
        "eta_min": 15,
        "cuisine": "Continental",
        "tags": ["high-protein", "low-fat"],
    },
    {
        "id": 4,
        "name": "SpiceBox",
        "dish": "Dal Makhani + Rice",
        "description": "Slow-cooked black lentils in a rich tomato base, served with steamed rice",
        "protein_g": 18,
        "calories": 550,
        "price": 149,
        "rating": 4.3,
        "eta_min": 30,
        "cuisine": "Indian",
        "tags": ["vegetarian", "comfort-food"],
    },
    {
        "id": 5,
        "name": "GreenLeaf",
        "dish": "Quinoa Protein Salad",
        "description": "Quinoa, chickpeas, cucumber, cherry tomatoes with lemon-herb dressing",
        "protein_g": 22,
        "calories": 380,
        "price": 279,
        "rating": 4.6,
        "eta_min": 35,
        "cuisine": "Healthy",
        "tags": ["vegan", "high-protein"],
    },
]

# ---- TOOLS ----
# These are the actual Python functions the LLM can call

def get_menu():
    # Returns all dishes with price, protein, calories, rating and ETA
    menu_text = ""
    for r in RESTAURANTS:
        menu_text += f"{r['dish']} by {r['name']} - ₹{r['price']} | {r['protein_g']}g protein | {r['calories']} cal | Rating: {r['rating']} | ETA: {r['eta_min']} mins\n"
    return menu_text

def get_best_value_meal():
    # Finds the dish with highest protein per rupee
    best = max(RESTAURANTS, key=lambda x: x["protein_g"] / x["price"])
    return f"Best value: {best['dish']} by {best['name']} - ₹{best['price']} | {best['protein_g']}g protein | ETA: {best['eta_min']} mins"

def place_order(dish: str, quantity: int):
    # Places order if dish exists in the menu
    for r in RESTAURANTS:
        if r["dish"].lower() == dish.lower():
            total = r["price"] * quantity
            return f"{quantity}x {r['dish']} from {r['name']} ordered! Total: ₹{total} | ETA: {r['eta_min']} mins"
    return f"{dish} is not available in the menu"

# ---- TOOL DEFINITIONS ----
# This tells the LLM which tools are available and how to use them
# LLM reads the "description" to decide which tool to call

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the food menu with items and prices",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_best_value_meal",
            "description": "Get the lowest price and highest protein meal recommendation",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Place an order for a food item",
            "parameters": {
                "type": "object",
                "properties": {
                    "dish": {"type": "string", "description": "Food dish name"},
                    "quantity": {"type": "integer", "description": "Number of items"}
                },
                "required": ["dish", "quantity"]
            }
        }
    }
]

# ---- AGENT LOOP ----
# Outer loop - keeps the conversation going
# Inner loop - keeps calling LLM until it stops using tools and gives a final answer

messages = []

while True:
    human_input = input("Human: ")
    messages.append({"role": "user", "content": human_input})

    # Inner loop - handles tool calls one by one
    while True:
        response = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )

        ai_message = response.choices[0].message

        if ai_message.tool_calls:
            # LLM wants to call a tool
            messages.append(ai_message)

            for tool_call in ai_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Run the correct function based on what LLM requested
                if tool_name == "get_menu":
                    result = get_menu()
                elif tool_name == "get_best_value_meal":
                    result = get_best_value_meal()
                elif tool_name == "place_order":
                    result = place_order(**tool_args)
                else:
                    result = "Unknown tool"

                # Send the tool result back to LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            # No more tool calls - LLM gave final answer
            print(f"AI: {ai_message.content}")
            print()
            break