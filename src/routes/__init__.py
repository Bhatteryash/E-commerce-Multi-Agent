# This file allows the 'src/routes' directory to be treated as a package.
# Routes are for API endpoints, not CrewAI tools

from fastapi import APIRouter
from .profile import router as profile_router
from .agents import router as agents_router

router = APIRouter()

router.include_router(profile_router)
router.include_router(agents_router)

# No tools to export from routes
__all__ = []