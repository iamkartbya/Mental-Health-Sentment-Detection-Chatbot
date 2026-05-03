"""
Input validation utilities for Milo AI application.
Provides validation functions for user inputs.
"""

import re
from typing import Tuple
from exceptions import ValidationError


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid email format
        
    Raises:
        ValidationError: If email is invalid
    """
    email = email.strip().lower()
    
    if not email:
        raise ValidationError("Email cannot be empty")
    
    if len(email) > 254:
        raise ValidationError("Email is too long")
    
    pattern = r'^[\w\.\+\-]+@[\w\-]+\.\w{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    
    return True


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        bool: True if password meets minimum requirements
        
    Raises:
        ValidationError: If password doesn't meet requirements
    """
    if not password:
        raise ValidationError("Password cannot be empty")
    
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    
    return True


def calculate_password_strength(password: str) -> Tuple[int, str, str]:
    """
    Calculate password strength score.
    
    Args:
        password: Password to evaluate
        
    Returns:
        Tuple of (score: int, label: str, color: str)
    """
    if len(password) == 0:
        return 0, "", "#243328"
    
    if len(password) < 8:
        return 1, "Too short", "#e07070"
    
    score = 0
    
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
    if len(password) >= 12:
        score += 1
    
    score = max(1, min(score, 4))
    
    labels = {1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}
    colors = {1: "#e07070", 2: "#c9a84c", 3: "#7aab8a", 4: "#5db87a"}
    
    return score, labels[score], colors[score]


def validate_text_input(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """
    Validate text input.
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If text is invalid
    """
    if not text or not text.strip():
        raise ValidationError("Input cannot be empty")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValidationError(f"Input must be at least {min_length} characters")
    
    if len(text) > max_length:
        raise ValidationError(f"Input cannot exceed {max_length} characters")
    
    return True


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing/escaping harmful characters.
    
    Args:
        text: Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    # Strip whitespace
    text = text.strip()
    
    # Remove potentially harmful characters but keep normal text
    # This is basic sanitization - adjust based on your needs
    text = re.sub(r'[<>\"\'\\]', '', text)
    
    return text
