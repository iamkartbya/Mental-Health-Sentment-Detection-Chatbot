"""
AI service for Milo AI application.
Handles interaction with Groq API.
"""

from typing import Optional, List, Dict
from groq import Groq
from config import CONFIG
from exceptions import AIServiceError
from logger import setup_logger
import os

logger = setup_logger(__name__)


class AIService:
    """Service for AI interactions with Groq"""

    _instance: Optional['AIService'] = None
    _client: Optional[Groq] = None

    def __new__(cls) -> 'AIService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls) -> 'AIService':
        instance = cls()

        if cls._client is not None:
            logger.info("Using existing Groq client")
            return instance

        try:
            logger.info("Initializing Groq client")

            cls._client = Groq(
                api_key=os.getenv("GROQ_API_KEY") or CONFIG.get("groq_api_key")
            )

            logger.info("✅ Groq client initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Groq: {str(e)}")
            raise AIServiceError(f"Failed to initialize Groq: {str(e)}")

        return instance

    @classmethod
    def get_client(cls) -> Groq:
        if cls._client is None:
            cls.initialize()
        return cls._client

    @staticmethod
    def get_system_prompt() -> str:
        return """You are Milo AI, an empathetic and supportive mental health chatbot created by Kartbya Kumar from Sathyabama Institute of Science and Technology, Chennai.

Your purpose is to:
- Provide emotional support and a listening ear
- Help users explore their feelings and thoughts
- Offer coping strategies and wellness tips
- Never replace professional mental health treatment
- Always encourage seeking professional help for serious concerns
- Maintain confidentiality and respect user privacy

Important:
- If user mentions self-harm, suggest professional help immediately
- Be empathetic, calm, and supportive
"""

    @staticmethod
    def get_response_sync(
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        try:
            client = AIService.get_client()

            # Add system prompt
            system_prompt = AIService.get_system_prompt()

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content

            if not content:
                return "I'm here to listen and support you. What's on your mind?"

            return content

        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise AIServiceError(f"Failed to get AI response: {str(e)}")


def init_ai() -> AIService:
    return AIService.initialize()


def get_ai_response(
    messages: List[Dict[str, str]],
    temperature: float = 0.7
) -> str:
    return AIService.get_response_sync(messages, temperature=temperature)


def get_system_message() -> str:
    return AIService.get_system_prompt()