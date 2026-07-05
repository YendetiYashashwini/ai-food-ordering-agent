# Arc 3 - tools
# All functions that the LLM can call as tools

from data import RESTAURANTS

def search_meals(
    max_price: int = None,
    min_protein: int = None,
    cuisine: str = None,
    diet: str = None
):
    if max_price: max_price = int(max_price)
    if min_protein: min_protein = int(min_protein)

    results = RESTAURANTS

    if max_price:
        results = [r for r in results if r["price"] <= max_price]
    if min_protein:
        results = [r for r in results if r["protein_g"] >= min_protein]
    if cuisine:
        results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
    if diet:
        results = [r for r in results if diet.lower() in [t.lower() for t in r["tags"]]]

    if not results:
        return "No meals found. Try relaxing your filters."

    output = ""
    for r in results:
        output += (
            f"\n🍽️ **{r['dish']}** — {r['name']}\n"
            f"   Protein: {r['protein_g']}g | Price: ₹{r['price']} | "
            f"ETA: {r['eta_min']} min | ⭐ {r['rating']}\n"
            f"   {r['description']}\n"
        )
    return output

def place_order(dish: str, quantity: int):
    for r in RESTAURANTS:
        if r["dish"].lower() == dish.lower():
            total = r["price"] * quantity
            return (
                f"\n🍽️  Order Confirmed!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 {quantity}x {r['dish']}\n"
                f"🏪 Restaurant: {r['name']}\n"
                f"💰 Total: ₹{total}\n"
                f"⏱️  ETA: {r['eta_min']} mins\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
            )
    return f"❌ {dish} is not available in the menu"


# Tool definitions - tells LLM which tools exist and how to use them
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_meals",
            "description": "Search meals based on protein, price, cuisine or diet preferences",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {"type": "integer", "description": "Maximum price in rupees"},
                    "min_protein": {"type": "integer", "description": "Minimum protein in grams"},
                    "cuisine": {"type": "string", "description": "Cuisine type e.g. Indian, Healthy, Continental"},
                    "diet": {"type": "string", "description": "Diet type e.g. vegetarian, vegan, high-protein, gluten-free"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Place an order for a specific dish",
            "parameters": {
                "type": "object",
                "properties": {
                    "dish": {"type": "string", "description": "Exact dish name"},
                    "quantity": {"type": "integer", "description": "Number of items"}
                },
                "required": ["dish", "quantity"]
            }
        }
    }
]