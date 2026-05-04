"""
Chat service for Milo AI application.
Handles chat and message management.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
from database import get_chats_collection, get_messages_collection
from utils import generate_chat_title, get_text_processor
from exceptions import ChatNotFoundError, DatabaseError, ValidationError
from validators import validate_text_input
from logger import setup_logger


logger = setup_logger(__name__)


class ChatService:
    """Service for managing chats and messages"""
    
    @staticmethod
    def create_chat(user_id: str, chat_id: str, first_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new chat.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            first_message: Optional first message to generate title from
            
        Returns:
            Dict with chat data
            
        Raises:
            DatabaseError: If creation fails
        """
        try:
            # Generate title from first message or use default
            title = "New Chat"
            if first_message:
                title = generate_chat_title(first_message)
            
            chat_doc = {
                "user_id": user_id,
                "chat_id": chat_id,
                "title": title,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "message_count": 0,
                "is_archived": False
            }
            
            chats_collection = get_chats_collection()
            result = chats_collection.insert_one(chat_doc)
            
            logger.info(f"Chat created: {chat_id} for user: {user_id}")
            
            return {
                "id": str(result.inserted_id),
                "chat_id": chat_id,
                "title": title,
                "created_at": chat_doc["created_at"]
            }
            
        except Exception as e:
            logger.error(f"Failed to create chat: {str(e)}")
            raise DatabaseError(f"Failed to create chat: {str(e)}")
    
    @staticmethod
    def save_message(
        user_id: str,
        chat_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save a message to database.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            role: Message role (user/assistant/system)
            content: Message content
            metadata: Optional metadata (sentiment, risk, etc.)
            
        Returns:
            Dict with message data
            
        Raises:
            ValidationError: If content is invalid
            DatabaseError: If save fails
        """
        try:
            # Validate input
            validate_text_input(content, max_length=50000)
            
            if role not in ["user", "assistant", "system"]:
                raise ValidationError(f"Invalid role: {role}")
            
            message_doc = {
                "user_id": user_id,
                "chat_id": chat_id,
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow(),
                "metadata": metadata or {}
            }
            
            messages_collection = get_messages_collection()
            result = messages_collection.insert_one(message_doc)
            
            # Update chat's updated_at and message count
            chats_collection = get_chats_collection()
            chats_collection.update_one(
                {"chat_id": chat_id, "user_id": user_id},
                {
                    "$set": {"updated_at": datetime.utcnow()},
                    "$inc": {"message_count": 1}
                }
            )
            
            logger.debug(f"Message saved: {str(result.inserted_id)} in chat: {chat_id}")
            
            return {
                "id": str(result.inserted_id),
                "role": role,
                "content": content,
                "timestamp": message_doc["timestamp"]
            }
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to save message in chat {chat_id}: {str(e)}")
            raise DatabaseError(f"Failed to save message: {str(e)}")
    
    @staticmethod
    def load_chat(user_id: str, chat_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Load messages for a chat with pagination (optimized).
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            limit: Number of messages to load (default 50)
            offset: Offset for pagination (default 0)
            
        Returns:
            List of message dictionaries
            
        Raises:
            ChatNotFoundError: If chat not found
            DatabaseError: If load fails
        """
        try:
            # Verify chat exists and belongs to user
            chats_collection = get_chats_collection()
            chat = chats_collection.find_one({
                "user_id": user_id,
                "chat_id": chat_id
            })
            
            if not chat:
                raise ChatNotFoundError(f"Chat {chat_id} not found")
            
            # Load messages with pagination (optimized with skip and limit)
            messages_collection = get_messages_collection()
            messages = list(messages_collection.find({
                "user_id": user_id,
                "chat_id": chat_id
            }).sort("timestamp", 1).skip(offset).limit(limit))
            
            # Format for LLM
            chat_list = []
            for msg in messages:
                chat_list.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            logger.debug(f"Loaded {len(chat_list)} messages for chat: {chat_id} (offset: {offset}, limit: {limit})")
            return chat_list
            
        except ChatNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to load chat {chat_id}: {str(e)}")
            raise DatabaseError(f"Failed to load chat: {str(e)}")
    
    @staticmethod
    def get_user_chats(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get all chats for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of chats to return
            
        Returns:
            List of chat dictionaries
            
        Raises:
            DatabaseError: If retrieval fails
        """
        try:
            chats_collection = get_chats_collection()
            chats = list(chats_collection.find(
                {"user_id": user_id, "is_archived": False}
            ).sort("updated_at", -1).limit(limit))
            
            # Format response
            result = []
            for chat in chats:
                result.append({
                    "id": str(chat["_id"]),
                    "chat_id": chat["chat_id"],
                    "title": chat["title"],
                    "created_at": chat["created_at"],
                    "updated_at": chat["updated_at"],
                    "message_count": chat.get("message_count", 0)
                })
            
            logger.debug(f"Retrieved {len(result)} chats for user: {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to get chats for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve chats: {str(e)}")
    
    @staticmethod
    def delete_chat(user_id: str, chat_id: str) -> bool:
        """
        Delete a chat and its messages.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            ChatNotFoundError: If chat not found
            DatabaseError: If deletion fails
        """
        try:
            chats_collection = get_chats_collection()
            messages_collection = get_messages_collection()
            
            # Verify chat exists
            chat = chats_collection.find_one({
                "user_id": user_id,
                "chat_id": chat_id
            })
            
            if not chat:
                raise ChatNotFoundError(f"Chat {chat_id} not found")
            
            # Delete messages
            messages_collection.delete_many({
                "user_id": user_id,
                "chat_id": chat_id
            })
            
            # Delete chat
            chats_collection.delete_one({
                "_id": chat["_id"]
            })
            
            logger.info(f"Chat deleted: {chat_id}")
            return True
            
        except ChatNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete chat {chat_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete chat: {str(e)}")
    
    @staticmethod
    def rename_chat(user_id: str, chat_id: str, new_title: str) -> bool:
        """
        Rename a chat.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            new_title: New title
            
        Returns:
            bool: True if renamed successfully
            
        Raises:
            ValidationError: If title is invalid
            ChatNotFoundError: If chat not found
            DatabaseError: If update fails
        """
        try:
            validate_text_input(new_title, min_length=1, max_length=200)
            
            chats_collection = get_chats_collection()
            
            # Update
            result = chats_collection.update_one(
                {"user_id": user_id, "chat_id": chat_id},
                {
                    "$set": {
                        "title": new_title,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                raise ChatNotFoundError(f"Chat {chat_id} not found")
            
            logger.info(f"Chat renamed: {chat_id}")
            return True
            
        except (ValidationError, ChatNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Failed to rename chat {chat_id}: {str(e)}")
            raise DatabaseError(f"Failed to rename chat: {str(e)}")


# Convenience functions
def create_new_chat(user_id: str, chat_id: str, first_message: Optional[str] = None) -> Dict[str, Any]:
    """Create a new chat"""
    return ChatService.create_chat(user_id, chat_id, first_message)


def save_chat_message(
    user_id: str,
    chat_id: str,
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Save a message"""
    return ChatService.save_message(user_id, chat_id, role, content, metadata)


def load_chat_history(user_id: str, chat_id: str) -> List[Dict[str, Any]]:
    """Load chat history"""
    return ChatService.load_chat(user_id, chat_id)


def get_all_user_chats(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all user chats"""
    return ChatService.get_user_chats(user_id, limit)


def delete_user_chat(user_id: str, chat_id: str) -> bool:
    """Delete a chat"""
    return ChatService.delete_chat(user_id, chat_id)


def rename_user_chat(user_id: str, chat_id: str, new_title: str) -> bool:
    """Rename a chat"""
    return ChatService.rename_chat(user_id, chat_id, new_title)
