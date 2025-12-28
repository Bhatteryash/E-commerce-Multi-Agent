# Minimal MCP stdio server exposing ecommerce tools
# Requires: pip install mcp

import asyncio
import json
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ToolRequest, ToolResponse

# Import your existing tools
from src.tools.ecommerce_tools import ProductSearchTool, PriceComparisonTool, ProductSearchInput, PriceComparisonInput

server = Server("ecommerce-tools")

# Register tools with simple JSON input schemas
@server.tool(
    name="product_search",
    description="Search for products by query/category and return mock results",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "category": {"type": "string"},
            "max_results": {"type": "integer"}
        },
        "required": ["query"],
        "additionalProperties": False
    }
)
async def product_search(req: ToolRequest) -> ToolResponse:
    # Validate and map inputs, then call your tool
    payload: Dict[str, Any] = req.arguments or {}
    query = payload.get("query")
    category = payload.get("category", "general")
    max_results = int(payload.get("max_results", 10))

    tool = ProductSearchTool()
    result = tool._run(query=query, category=category, max_results=max_results)
    return ToolResponse(content=[TextContent(type="text", text=result)])

@server.tool(
    name="price_comparison",
    description="Compare prices across platforms for a product name",
    input_schema={
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "platforms": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["product_name"],
        "additionalProperties": False
    }
)
async def price_comparison(req: ToolRequest) -> ToolResponse:
    payload: Dict[str, Any] = req.arguments or {}
    product_name = payload.get("product_name")
    platforms = payload.get("platforms")

    tool = PriceComparisonTool()
    result = tool._run(product_name=product_name, platforms=platforms)
    return ToolResponse(content=[TextContent(type="text", text=result)])

async def main() -> None:
    # Start stdio transport
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
