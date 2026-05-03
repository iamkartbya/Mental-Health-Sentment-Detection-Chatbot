"""
Custom exceptions for Milo AI application.
Provides domain-specific exception classes.
"""


class MiloException(Exception):
    """Base exception for all Milo AI errors"""
    pass


class AuthenticationError(MiloException):
    """Raised when authentication fails"""
    pass


class UserNotFoundError(MiloException):
    """Raised when user is not found"""
    pass


class UserAlreadyExistsError(MiloException):
    """Raised when trying to create user that already exists"""
    pass


class DatabaseError(MiloException):
    """Raised when database operation fails"""
    pass


class ModelError(MiloException):
    """Raised when model loading or inference fails"""
    pass


class AIServiceError(MiloException):
    """Raised when AI service call fails"""
    pass


class ValidationError(MiloException):
    """Raised when input validation fails"""
    pass


class ChatNotFoundError(MiloException):
    """Raised when chat is not found"""
    pass
