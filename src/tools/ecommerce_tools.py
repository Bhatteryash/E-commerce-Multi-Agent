from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
import json
import random
from datetime import datetime


class ProductSearchInput(BaseModel):
    """Input schema for ProductSearchTool."""
    query: str = Field(..., description="Product search query")
    category: str = Field(default="general", description="Product category")
    max_results: int = Field(default=10, description="Maximum number of results to return")


class ProductSearchTool(BaseTool):
    name: str = "Product Search Tool"
    description: str = (
        "Search for products across multiple e-commerce platforms. "
        "This tool helps find products based on search queries and categories."
    )
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, query: str, category: str = "general", max_results: int = 10) -> str:
        """
        Search for products. In a real implementation, this would connect to actual APIs.
        For demo purposes, we'll return mock data.
        """
        # Mock product data - in real implementation, this would call actual APIs
        mock_products = [
            {
                "name": f"Premium {query} - Model A",
                "price": round(random.uniform(50, 500), 2),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "reviews": random.randint(10, 1000),
                "description": f"High-quality {query} with advanced features",
                "availability": "In Stock",
                "seller": "TechStore Plus",
                "category": category
            },
            {
                "name": f"Budget {query} - Model B",
                "price": round(random.uniform(20, 150), 2),
                "rating": round(random.uniform(3.0, 4.5), 1),
                "reviews": random.randint(5, 500),
                "description": f"Affordable {query} with good value for money",
                "availability": "In Stock",
                "seller": "ValueMart",
                "category": category
            },
            {
                "name": f"Professional {query} - Model C",
                "price": round(random.uniform(200, 800), 2),
                "rating": round(random.uniform(4.0, 5.0), 1),
                "reviews": random.randint(50, 800),
                "description": f"Professional-grade {query} for serious users",
                "availability": "Limited Stock",
                "seller": "ProEquipment",
                "category": category
            }
        ]
        
        # Limit results
        results = mock_products[:min(max_results, len(mock_products))]
        
        return json.dumps({
            "search_query": query,
            "category": category,
            "total_results": len(results),
            "products": results,
            "search_timestamp": datetime.now().isoformat()
        }, indent=2)


class PriceComparisonInput(BaseModel):
    """Input schema for PriceComparisonTool."""
    product_name: str = Field(..., description="Product name to compare prices")
    platforms: List[str] = Field(default=["amazon", "ebay", "walmart"], description="Platforms to compare")


class PriceComparisonTool(BaseTool):
    name: str = "Price Comparison Tool"
    description: str = (
        "Compare prices of products across different e-commerce platforms. "
        "Helps find the best deals and pricing information."
    )
    args_schema: Type[BaseModel] = PriceComparisonInput

    def _run(self, product_name: str, platforms: List[str] = None) -> str:
        """
        Compare prices across platforms. In a real implementation, this would connect to actual APIs.
        For demo purposes, we'll return mock price comparison data.
        """
        if platforms is None:
            platforms = ["amazon", "ebay", "walmart", "bestbuy"]
        
        # Mock price comparison data
        base_price = random.uniform(50, 300)
        price_comparisons = []
        
        for platform in platforms:
            # Vary prices by platform with some randomness
            price_variation = random.uniform(0.8, 1.3)
            price = round(base_price * price_variation, 2)
            shipping = round(random.uniform(0, 25), 2) if random.choice([True, False]) else 0
            
            price_comparisons.append({
                "platform": platform.title(),
                "price": price,
                "shipping": shipping,
                "total_cost": price + shipping,
                "availability": random.choice(["In Stock", "Limited Stock", "Pre-order"]),
                "seller_rating": round(random.uniform(3.5, 5.0), 1),
                "return_policy": f"{random.choice([30, 60, 90])} days",
                "prime_eligible": platform == "amazon" and random.choice([True, False])
            })
        
        # Sort by total cost
        price_comparisons.sort(key=lambda x: x["total_cost"])
        
        best_deal = price_comparisons[0]
        savings = price_comparisons[-1]["total_cost"] - best_deal["total_cost"]
        
        return json.dumps({
            "product": product_name,
            "comparison_timestamp": datetime.now().isoformat(),
            "price_comparisons": price_comparisons,
            "best_deal": {
                "platform": best_deal["platform"],
                "total_cost": best_deal["total_cost"],
                "savings_vs_highest": round(savings, 2)
            },
            "summary": f"Best price found on {best_deal['platform']} at ${best_deal['total_cost']:.2f} (saves ${savings:.2f})"
        }, indent=2)


class UserPreferencesTool(BaseTool):
    name: str = "User Preferences Tool"
    description: str = (
        "Analyze and store user preferences for personalized recommendations. "
        "Helps understand customer shopping behavior and preferences."
    )
    args_schema: Type[BaseModel] = BaseModel

    def _run(self) -> str:
        """
        Get user preferences. This would typically connect to a user database.
        """
        # Mock user preferences
        preferences = {
            "preferred_brands": ["Apple", "Samsung", "Sony"],
            "price_range": "mid-range",
            "shopping_frequency": "monthly",
            "preferred_categories": ["electronics", "home", "books"],
            "delivery_preference": "fast",
            "review_threshold": 4.0,
            "warranty_preference": "extended"
        }
        
        return json.dumps({
            "user_preferences": preferences,
            "last_updated": datetime.now().isoformat()
        }, indent=2)
