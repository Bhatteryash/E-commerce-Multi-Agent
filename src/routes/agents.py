from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from src.utils.logging import setup_logger

from src.crew import ECommerce

router = APIRouter(prefix="/agents")
logger = setup_logger(__name__)

crew_instance = None

def get_crew():
    """Get or create crew instance"""
    global crew_instance
    if crew_instance is None:
        crew_instance = ECommerce()
    return crew_instance

# Pydantic models for request/response
class ProductSearchRequest(BaseModel):
    query: str = Field(..., description="Product search query", example="wireless bluetooth headphones")
    budget: Optional[str] = Field("flexible", description="Budget constraint", example="under $200")
    category: Optional[str] = Field("general", description="Product category", example="electronics")
    preferences: Optional[str] = Field("", description="User preferences", example="good sound quality, noise cancellation")

class CustomerSupportRequest(BaseModel):
    query: str = Field(..., description="Customer support query", example="What's the return policy?")
    context: Optional[str] = Field("", description="Additional context", example="I bought headphones last week")

class ProductSearchResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]
    timestamp: str

class CustomerSupportResponse(BaseModel):
    success: bool
    message: str
    response: str
    timestamp: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_type: str
    timestamp: str

@router.post("/api/v1/search", response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest, background_tasks: BackgroundTasks):
    """
    Search for products using the e-commerce multi-agent crew
    """
    try:
        logger.info(f"🔍 Product search request: {request.query}")
        
        # Get crew instance
        crew = get_crew()
        
        # Run product search
        result = crew.run_product_search(
            query=request.query,
            budget=request.budget,
            category=request.category,
            preferences=request.preferences
        )
        
        if result.get("success"):
            logger.info("✅ Product search completed successfully")
            return ProductSearchResponse(
                success=True,
                message="Product search completed successfully",
                data=result,
                timestamp=datetime.now().isoformat()
            )
        else:
            logger.error(f"❌ Product search failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail="Product search failed")
            
    except Exception as e:
        logger.error(f"❌ Error in product search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                message="Internal server error during product search",
                error_type=type(e).__name__,
                timestamp=datetime.now().isoformat()
            ).dict()
        )

@router.post("/api/v1/support", response_model=CustomerSupportResponse)
async def customer_support(request: CustomerSupportRequest):
    """
    Handle customer support queries using the customer service agent
    """
    try:
        logger.info(f"💬 Customer support request: {request.query[:100]}...")
        
        # Get crew instance
        crew = get_crew()
        
        # Handle customer query
        result = crew.handle_customer_query(
            follow_up_query=request.query,
            context=request.context
        )
        
        if result.get("success"):
            logger.info("✅ Customer support query handled successfully")
            return CustomerSupportResponse(
                success=True,
                message="Customer support query handled successfully",
                response=result.get("response", ""),
                timestamp=datetime.now().isoformat()
            )
        else:
            logger.error(f"❌ Customer support failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail="Customer support query failed")
            
    except Exception as e:
        logger.error(f"❌ Error in customer support: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                message="Internal server error during customer support",
                error_type=type(e).__name__,
                timestamp=datetime.now().isoformat()
            ).dict()
        )