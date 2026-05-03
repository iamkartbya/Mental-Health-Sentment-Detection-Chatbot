"""
Database module for Milo AI application.
Handles MongoDB connection and collections initialization.
"""

import certifi
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from config import CONFIG
from logger import setup_logger
from exceptions import DatabaseError


logger = setup_logger(__name__)


class Database:
    """MongoDB database manager"""
    
    _instance: Optional['Database'] = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls) -> 'Database':
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def connect(cls) -> 'Database':
        """
        Establish MongoDB connection.
        
        Returns:
            Database: Database instance
            
        Raises:
            DatabaseError: If connection fails
        """
        instance = cls()
        
        if cls._client is not None:
            logger.info("Using existing database connection")
            return instance
        
        try:
            logger.info(f"Connecting to MongoDB at {CONFIG.mongo.cluster}")
            
            cls._client = MongoClient(
                CONFIG.mongo.connection_uri,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=CONFIG.db_connection_timeout,
                connectTimeoutMS=CONFIG.db_connection_timeout,
                socketTimeoutMS=CONFIG.db_socket_timeout,
            )
            
            # Test connection
            cls._client.admin.command("ping")
            logger.info("✅ MongoDB connection successful")
            
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.error(f"❌ MongoDB connection failed: {str(e)}")
            raise DatabaseError(f"Failed to connect to MongoDB: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Unexpected error during MongoDB connection: {str(e)}")
            raise DatabaseError(f"Unexpected error: {str(e)}")
        
        return instance
    
    @classmethod
    def get_database(cls) -> 'Database':
        """
        Get database instance. Connects if not already connected.
        
        Returns:
            Database: Database instance
        """
        instance = cls()
        if cls._client is None:
            cls.connect()
        return instance
    
    @property
    def db(self):
        """Get database object"""
        if self._client is None:
            raise DatabaseError("Database not connected")
        return self._client[CONFIG.mongo.database]
    
    @property
    def users_collection(self) -> Collection:
        """Get users collection"""
        return self.db["users"]
    
    @property
    def chats_collection(self) -> Collection:
        """Get chats collection"""
        return self.db["chats"]
    
    @property
    def messages_collection(self) -> Collection:
        """Get messages collection"""
        return self.db["messages"]
    
    def close(self) -> None:
        """Close database connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
            logger.info("Database connection closed")


# Convenience functions
def get_database() -> Database:
    """
    Get database instance.
    
    Returns:
        Database: Database instance
    """
    return Database.get_database()


def get_users_collection() -> Collection:
    """Get users collection"""
    return get_database().users_collection


def get_chats_collection() -> Collection:
    """Get chats collection"""
    return get_database().chats_collection


def get_messages_collection() -> Collection:
    """Get messages collection"""
    return get_database().messages_collection
