"""
E-commerce Multi-Agent System
Export all tools for discovery and publishing
"""

# Import tools only - don't import routes, db, or other modules
# This prevents side effects during tool discovery
try:
    from src.tools.ecommerce_tools import (
        ProductSearchTool,
        PriceComparisonTool,
        UserPreferencesTool
    )
    from src.tools.custom_tool import MyCustomTool
    
    # Define what should be exported when publishing tools
    __all__ = [
        "ProductSearchTool",
        "PriceComparisonTool",
        "UserPreferencesTool",
        "MyCustomTool"
    ]
except ImportError:
    # Fallback if imports fail during discovery
    __all__ = []
