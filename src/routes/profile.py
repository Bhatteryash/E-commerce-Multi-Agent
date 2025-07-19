from fastapi import APIRouter, HTTPException
from src.service.user_service import UserProfile
from pydantic import BaseModel


router = APIRouter(prefix="/profile")

profile = UserProfile()

class Users(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

@router.post("/api/v1/users")
def create_user(user: Users):
    try:
        user_id = profile.save_user(user)
        return {"user_id": user_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))