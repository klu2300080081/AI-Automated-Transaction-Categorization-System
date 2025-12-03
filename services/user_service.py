from datetime import datetime
from config.db_config import db_config
from utils.auth_utils import AuthUtils
import uuid

class UserService:
    
    def __init__(self):
        self.db = db_config.get_database()
        self.users_collection = self.db["users"]
        self._create_indexes()
    
    def _create_indexes(self):
        # Create unique index on email and username
        self.users_collection.create_index("email", unique=True)
        self.users_collection.create_index("username", unique=True)
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        try:
            # Check if user already exists
            if self.users_collection.find_one({"email": email}):
                return {"success": False, "message": "Email already registered"}
            
            if self.users_collection.find_one({"username": username}):
                return {"success": False, "message": "Username already taken"}
            
            # Create user
            user_id = str(uuid.uuid4())
            hashed_password = AuthUtils.hash_password(password)
            
            user_data = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "password": hashed_password,
                "user_created_on": datetime.utcnow()
            }
            
            self.users_collection.insert_one(user_data)
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id
            }
        
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}
    
    def login_user(self, email: str, password: str) -> dict:
        try:
            user = self.users_collection.find_one({"email": email})
            
            if not user:
                return {"success": False, "message": "Invalid email or password"}
            
            if not AuthUtils.verify_password(password, user["password"]):
                return {"success": False, "message": "Invalid email or password"}
            
            # Create JWT token
            token = AuthUtils.create_access_token({
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"]
            })
            
            return {
                "success": True,
                "message": "Login successful",
                "token": token,
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}
    
    def get_user_by_id(self, user_id: str) -> dict:
        try:
            user = self.users_collection.find_one(
                {"user_id": user_id},
                {"password": 0, "_id": 0}
            )
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None