from datetime import datetime
from src.db.db_connection import get_db
from src.model.users import Users
from bson import ObjectId

class UserProfile:
    def __init__(self):
        """Initialize UserProfile with the database connection"""
        self.db = get_db()
    
    def _get_collection(self,db):
        return {
            'users': db['users']
        }
    
    def save_user(self, user_data) -> str:
        """Save user data to the database"""
        collections = self._get_collection(self.db)

        # Use attribute access for Pydantic or dataclass models
        email = getattr(user_data, 'email', None)
        if not email:
            raise ValueError("Email is required")
        user = collections['users'].find_one({"email": email})
        if user:
            raise ValueError("User with this email already exists")

        user_obj = Users(
            _id=ObjectId(),
            first_name=getattr(user_data, 'first_name', None),
            last_name=getattr(user_data, 'last_name', None),
            email=email,
            password=getattr(user_data, 'password', None),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # Convert dataclass to dict for MongoDB
        user_dict = user_obj.__dict__
        result = collections['users'].insert_one(user_dict)
        return "User created successfully with ID: {}".format(result.inserted_id)