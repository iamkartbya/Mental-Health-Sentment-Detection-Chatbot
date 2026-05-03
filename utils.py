"""
Utility functions for Milo AI application.
Provides common helper functions.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Tuple, Optional
from logger import setup_logger


logger = setup_logger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


class TextProcessor:
    """Text preprocessing utilities for NLP"""
    
    _instance: Optional['TextProcessor'] = None
    
    def __new__(cls) -> 'TextProcessor':
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize text processor"""
        if self._initialized:
            return
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._initialized = True
        logger.info("TextProcessor initialized")
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess text for NLP analysis.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        if not text:
            return ""
        
        # Lowercase
        text = text.lower()
        
        # Remove special characters, keep only letters and spaces
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Tokenize
        words = nltk.word_tokenize(text)
        
        # Lemmatize and remove stopwords
        processed_words = [
            self.lemmatizer.lemmatize(w)
            for w in words
            if w not in self.stop_words and len(w) > 1
        ]
        
        return " ".join(processed_words)


def get_text_processor() -> TextProcessor:
    """
    Get singleton instance of TextProcessor.
    
    Returns:
        TextProcessor: Singleton instance
    """
    return TextProcessor()


def generate_chat_title(text: str, max_length: int = 50) -> str:
    """
    Generate a chat title from first message.
    
    Args:
        text: First message text
        max_length: Maximum length of title
        
    Returns:
        str: Generated title
    """
    # Remove special characters and extra whitespace
    title = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Truncate
    if len(title) > max_length:
        title = title[:max_length-3] + "..."
    
    # Return or provide default
    return title if title else "New Chat"


def format_timestamp(timestamp) -> str:
    """
    Format MongoDB timestamp for display.
    
    Args:
        timestamp: MongoDB datetime object
        
    Returns:
        str: Formatted timestamp
    """
    try:
        return timestamp.strftime("%b %d, %Y %I:%M %p")
    except (AttributeError, ValueError):
        return "Unknown"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
