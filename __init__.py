"""
Milo AI - Mental Health Support Chatbot
A sentiment-focused LLM chatbot for mental health support

Created by: Kartbya Kumar
Institution: Sathyabama Institute of Science and Technology, Chennai
"""

__version__ = "1.0.0"
__author__ = "Kartbya Kumar"

# Core imports for easy access
from database import Database, get_database, get_users_collection, get_chats_collection, get_messages_collection
from auth_service import AuthService
from ai_service import AIService
from sentiment_model import SentimentModel
from chat_service import ChatService
from config import CONFIG
from logger import setup_logger
from exceptions import (
    MiloException,
    AuthenticationError,
    UserNotFoundError,
    UserAlreadyExistsError,
    DatabaseError,
    ModelError,
    AIServiceError,
    ValidationError,
    ChatNotFoundError
)

__all__ = [
    "Database",
    "get_database",
    "get_users_collection",
    "get_chats_collection", 
    "get_messages_collection",
    "AuthService",
    "AIService",
    "SentimentModel",
    "ChatService",
    "CONFIG",
    "setup_logger",
    "MiloException",
    "AuthenticationError",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "DatabaseError",
    "ModelError",
    "AIServiceError",
    "ValidationError",
    "ChatNotFoundError"
]
