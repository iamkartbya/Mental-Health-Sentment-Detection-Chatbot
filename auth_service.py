"""
Authentication service for Milo AI application.
Handles user signup, login, and password verification.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import bcrypt
from database import get_users_collection
from exceptions import (
    AuthenticationError,
    UserNotFoundError,
    UserAlreadyExistsError,
    DatabaseError,
    ValidationError
)
from validators import validate_email, validate_password
from logger import setup_logger


logger = setup_logger(__name__)


class AuthService:
    """Authentication service for user management"""
    
    @staticmethod
    def signup(email: str, password: str) -> Dict[str, Any]:
        """
        Create a new user account.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Dict with user data
            
        Raises:
            ValidationError: If email or password is invalid
            UserAlreadyExistsError: If user already exists
            DatabaseError: If database operation fails
        """
        try:
            # Validate inputs
            validate_email(email)
            validate_password(password)
            
            email = email.strip().lower()
            
            # Check if user exists
            users_collection = get_users_collection()
            existing_user = users_collection.find_one({"username": email})
            
            if existing_user:
                logger.warning(f"Signup attempt with existing email: {email}")
                raise UserAlreadyExistsError(f"User with email {email} already exists")
            
            # Hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create user document
            user_doc = {
                "username": email,
                "email": email,
                "password": hashed_password,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": None,
                "is_active": True
            }
            
            result = users_collection.insert_one(user_doc)
            
            logger.info(f"User created successfully: {email}")
            
            return {
                "id": str(result.inserted_id),
                "email": email,
                "created_at": user_doc["created_at"]
            }
            
        except (ValidationError, UserAlreadyExistsError):
            raise
        except Exception as e:
            logger.error(f"Signup error for {email}: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    @staticmethod
    def login(email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Dict with user data (without password)
            
        Raises:
            ValidationError: If email or password is invalid
            AuthenticationError: If authentication fails
            DatabaseError: If database operation fails
        """
        try:
            # Validate inputs
            validate_email(email)
            if not password:
                raise ValidationError("Password cannot be empty")
            
            email = email.strip().lower()
            
            # Find user
            users_collection = get_users_collection()
            user = users_collection.find_one({"username": email})
            
            if not user:
                logger.warning(f"Login attempt with non-existent user: {email}")
                raise AuthenticationError("Invalid email or password")
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                logger.warning(f"Failed login attempt for: {email}")
                raise AuthenticationError("Invalid email or password")
            
            # Update last login
            users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            logger.info(f"User logged in successfully: {email}")
            
            # Return user data without password
            return {
               "id": str(user["_id"]),
               "email": user.get("email", user.get("username")),
               "username": user.get("username"),
               "created_at": user.get("created_at"),
               "last_login": datetime.utcnow()
            }
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            raise DatabaseError(f"Login failed: {str(e)}")
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            bool: True if password matches
        """
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
    
    @staticmethod
    def change_password(email: str, old_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            email: User email
            old_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password changed successfully
            
        Raises:
            AuthenticationError: If old password is incorrect
            ValidationError: If new password is invalid
            DatabaseError: If database operation fails
        """
        try:
            validate_email(email)
            validate_password(new_password)
            
            email = email.strip().lower()
            
            # Verify old password
            users_collection = get_users_collection()
            user = users_collection.find_one({"username": email})
            
            if not user:
                raise UserNotFoundError(f"User {email} not found")
            
            if not AuthService.verify_password(old_password, user["password"]):
                raise AuthenticationError("Current password is incorrect")
            
            # Hash new password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # Update password
            users_collection.update_one(
                {"username": email},
                {
                    "$set": {
                        "password": hashed_password,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"Password changed for user: {email}")
            return True
            
        except (ValidationError, AuthenticationError, UserNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Password change error for {email}: {str(e)}")
            raise DatabaseError(f"Failed to change password: {str(e)}")


# Convenience functions
def signup_user(email: str, password: str) -> Dict[str, Any]:
    """Signup a new user"""
    return AuthService.signup(email, password)


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Login a user"""
    return AuthService.login(email, password)


def change_user_password(email: str, old_password: str, new_password: str) -> bool:
    """Change user password"""
    return AuthService.change_password(email, old_password, new_password)
