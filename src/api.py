from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uvicorn
import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from src.crew import ECommerce
from src.routes import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-commerce Multi-Agent API",
    description="REST API for e-commerce product search and recommendations using CrewAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the application on startup"""
    logger.info("🚀 Starting E-commerce Multi-Agent API...")
    try:
        # Initialize crew
        # get_crew()
        logger.info("✅ Crew initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize crew: {e}")



@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "e-commerce-multi-agent-api"
    }



# Include the profile router
app.include_router(router)

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
