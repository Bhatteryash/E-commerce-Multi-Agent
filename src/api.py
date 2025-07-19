from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uvicorn
import asyncio
import logging
from datetime import datetime
import json

from src.crew import ECommerce

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(
    title="E-commerce Multi-Agent API",
    description="REST API for e-commerce product search and recommendations using CrewAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Global crew instance (in production, consider using dependency injection)
crew_instance = None

def get_crew():
    """Get or create crew instance"""
    global crew_instance
    if crew_instance is None:
        crew_instance = ECommerce()
    return crew_instance

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("🚀 Starting E-commerce Multi-Agent API...")
    try:
        # Initialize crew
        get_crew()
        logger.info("✅ Crew initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize crew: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "E-commerce Multi-Agent API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "product_search": "/api/v1/search",
            "customer_support": "/api/v1/support",
            "health_check": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "e-commerce-multi-agent-api"
    }

@app.post("/api/v1/search", response_model=ProductSearchResponse)
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

@app.post("/api/v1/support", response_model=CustomerSupportResponse)
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

@app.get("/api/v1/search/example")
async def get_search_example():
    """
    Get example search requests for testing
    """
    examples = [
        {
            "query": "wireless bluetooth headphones",
            "budget": "under $200",
            "category": "electronics",
            "preferences": "good sound quality, noise cancellation, long battery life"
        },
        {
            "query": "laptop for programming",
            "budget": "under $1500",
            "category": "computers",
            "preferences": "fast processor, good keyboard, lightweight"
        },
        {
            "query": "running shoes",
            "budget": "flexible",
            "category": "sports",
            "preferences": "comfortable, good support, durable"
        }
    ]
    
    return {
        "examples": examples,
        "usage": "POST these examples to /api/v1/search to test the API"
    }

@app.get("/api/v1/support/example")
async def get_support_example():
    """
    Get example support queries for testing
    """
    examples = [
        {
            "query": "What's the return policy for electronics?",
            "context": "I'm considering buying headphones"
        },
        {
            "query": "Do you offer international shipping?",
            "context": "I want to order a laptop to Canada"
        },
        {
            "query": "How long does delivery usually take?",
            "context": "I need running shoes for next week"
        }
    ]
    
    return {
        "examples": examples,
        "usage": "POST these examples to /api/v1/support to test the API"
    }

# Async background task for long-running operations
@app.post("/api/v1/search/async")
async def search_products_async(request: ProductSearchRequest, background_tasks: BackgroundTasks):
    """
    Asynchronous product search (for long-running searches)
    """
    task_id = f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def run_search_task():
        try:
            crew = get_crew()
            result = crew.run_product_search(
                query=request.query,
                budget=request.budget,
                category=request.category,
                preferences=request.preferences
            )
            # In production, store result in database or cache
            logger.info(f"✅ Async search task {task_id} completed")
        except Exception as e:
            logger.error(f"❌ Async search task {task_id} failed: {e}")
    
    background_tasks.add_task(run_search_task)
    
    return {
        "message": "Search task started",
        "task_id": task_id,
        "status": "processing",
        "timestamp": datetime.now().isoformat()
    }

def start_server():
    """Start the FastAPI server"""
    uvicorn.run(
        "src.e_commerce.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
