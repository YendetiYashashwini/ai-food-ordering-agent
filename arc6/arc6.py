# Arc 6 - MCP (Model Context Protocol)
# We expose our food agent tools via MCP
# Now any AI client (Claude Desktop, Cursor) can use our tools directly

import sys
sys.path.append(r"c:\Users\yende\Projects\AI Food Ordering Agent\arc3")

from fastmcp import FastMCP
from tools import search_meals, place_order

# Create MCP server
mcp = FastMCP("Food Agent")

# Expose search_meals as MCP tool
@mcp.tool()
def search_meals_tool(
    max_price: int = None,
    min_protein: int = None,
    cuisine: str = None,
    diet: str = None
) -> str:
    """Search for meals based on price, protein, cuisine or diet preferences"""
    return search_meals(
        max_price=max_price,
        min_protein=min_protein,
        cuisine=cuisine,
        diet=diet
    )

# Expose place_order as MCP tool
@mcp.tool()
def place_order_tool(dish: str, quantity: int = 1) -> str:
    """Place an order for a specific dish"""
    return place_order(dish=dish, quantity=quantity)

# Run the MCP server
if __name__ == "__main__":
    mcp.run()