from bson import ObjectId
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Users:
    _id: ObjectId
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime