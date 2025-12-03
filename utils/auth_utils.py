import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import streamlit as st

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Try Streamlit secrets first, then fall back to environment variables
try:
    JWT_SECRET_KEY = st.secrets.get("JWT_SECRET_KEY", os.getenv("JWT_SECRET_KEY", "default-secret-key-change-in-production"))
    JWT_ALGORITHM = st.secrets.get("JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))
    JWT_EXPIRATION_HOURS = int(st.secrets.get("JWT_EXPIRATION_HOURS", os.getenv("JWT_EXPIRATION_HOURS", "24")))
except:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

class AuthUtils:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError:
            return None