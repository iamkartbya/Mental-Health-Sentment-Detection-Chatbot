"""
Authentication module for Milo AI.
Provides user authentication and management operations.
"""

import bcrypt
from datetime import datetime
from database import get_users_collection
from exceptions import AuthenticationError, UserNotFoundError
from logger import setup_logger

logger = setup_logger(__name__)

def signup(email, password):
    """Sign up a new user"""
    try:
        users_collection = get_users_collection()
        email = email.strip().lower()

        if users_collection.find_one({"username": email}):
            logger.warning(f"Signup attempt with existing email: {email}")
            return False

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        users_collection.insert_one({
            "username": email,
            "email": email,
            "password": hashed,
            "created_at": datetime.utcnow()
        })
        
        logger.info(f"User signed up: {email}")
        return True
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return False


def login(email, password):
    """Authenticate user with email and password"""
    try:
        users_collection = get_users_collection()
        email = email.strip().lower()

        user = users_collection.find_one({"username": email})

        if user and bcrypt.checkpw(password.encode(), user["password"]):
            logger.info(f"User logged in: {email}")
            return user

        logger.warning(f"Failed login attempt for: {email}")
        return None
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return None