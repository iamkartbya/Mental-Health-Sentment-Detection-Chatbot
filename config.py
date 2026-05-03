"""
Configuration management for Milo AI application.
Handles environment variables and application settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class MongoConfig:
    """MongoDB configuration"""
    user: str
    password: str
    cluster: str
    database: str = "mental_health"
    
    @property
    def connection_uri(self) -> str:
        """Build MongoDB connection URI"""
        from urllib.parse import quote_plus
        username = quote_plus(self.user)
        password = quote_plus(self.password)
        return f"mongodb+srv://{username}:{password}@{self.cluster}/{self.database}?retryWrites=true&w=majority"


@dataclass
class GroqConfig:
    """Groq API configuration"""
    api_key: str


@dataclass
class AppConfig:
    """Main application configuration"""
    mongo: MongoConfig
    groq: GroqConfig
    debug: bool
    log_level: str
    
    # Timeouts (in milliseconds)
    db_connection_timeout: int = 5000
    db_socket_timeout: int = 5000
    
    # Model paths
    model_path: str = "model.pkl"
    vectorizer_path: str = "vectorizer.pkl"


def load_config() -> AppConfig:
    """
    Load configuration from environment variables.
    
    Returns:
        AppConfig: Application configuration object
        
    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()
    
    # Required environment variables
    required_vars = [
        "MONGO_USER",
        "MONGO_PASS",
        "MONGO_CLUSTER",
        "GROQ_API_KEY",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    mongo_config = MongoConfig(
        user=os.getenv("MONGO_USER", ""),
        password=os.getenv("MONGO_PASS", ""),
        cluster=os.getenv("MONGO_CLUSTER", ""),
    )
    
    groq_config = GroqConfig(
        api_key=os.getenv("GROQ_API_KEY", "")
    )
    
    app_config = AppConfig(
        mongo=mongo_config,
        groq=groq_config,
        debug=os.getenv("DEBUG", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
    
    return app_config


# Global configuration instance
try:
    CONFIG = load_config()
except ValueError as e:
    import sys
    print(f"Configuration Error: {e}")
    sys.exit(1)
