# This file allows the 'src' directory to be treated as a package root.

from fastapi import APIRouter
from .profile import router as profile_router
from .agents import router as agents_router

router = APIRouter()

router.include_router(profile_router)
router.include_router(agents_router)