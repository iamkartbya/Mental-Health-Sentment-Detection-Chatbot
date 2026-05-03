"""
Sentiment and mental health model service for Milo AI.
Handles model loading and inference for depression detection.
"""

import joblib
from typing import Tuple, Optional, Dict, Any
from exceptions import ModelError
from utils import get_text_processor
from logger import setup_logger
from config import CONFIG


logger = setup_logger(__name__)


class SentimentModel:
    """Mental health sentiment analysis model"""
    
    _instance: Optional['SentimentModel'] = None
    _model = None
    _vectorizer = None
    
    def __new__(cls) -> 'SentimentModel':
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def load(cls) -> 'SentimentModel':
        """
        Load models from disk.
        
        Returns:
            SentimentModel: Loaded model instance
            
        Raises:
            ModelError: If model loading fails
        """
        instance = cls()
        
        if cls._model is not None and cls._vectorizer is not None:
            logger.info("Using cached models")
            return instance
        
        try:
            logger.info(f"Loading model from {CONFIG.model_path}")
            cls._model = joblib.load(CONFIG.model_path)
            
            logger.info(f"Loading vectorizer from {CONFIG.vectorizer_path}")
            cls._vectorizer = joblib.load(CONFIG.vectorizer_path)
            
            logger.info("✅ Models loaded successfully")
            
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {str(e)}")
            raise ModelError(f"Model file not found: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            raise ModelError(f"Failed to load models: {str(e)}")
        
        return instance
    
    @staticmethod
    def predict_risk(text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict mental health risk level.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (risk_level, confidence, scores_dict)
            - risk_level: "HIGH" or "LOW"
            - confidence: Confidence score (0-1)
            - scores_dict: Detailed scores
            
        Raises:
            ModelError: If prediction fails
        """
        try:
            if SentimentModel._model is None or SentimentModel._vectorizer is None:
                raise ModelError("Models not loaded. Call load() first")
            
            if not text or not text.strip():
                raise ValueError("Text input cannot be empty")
            
            # Preprocess text
            text_processor = get_text_processor()
            processed_text = text_processor.preprocess(text)
            
            if not processed_text:
                # If text becomes empty after processing, classify as LOW risk
                logger.warning("Text became empty after preprocessing")
                return "LOW", 0.5, {"LOW": 0.5, "HIGH": 0.5}
            
            # Vectorize
            vec = SentimentModel._vectorizer.transform([processed_text])
            
            # Predict
            prediction = SentimentModel._model.predict(vec)[0]
            probabilities = SentimentModel._model.predict_proba(vec)[0]
            
            risk_level = "HIGH" if prediction == 1 else "LOW"
            confidence = float(max(probabilities))
            
            scores = {
                "LOW": float(probabilities[0]),
                "HIGH": float(probabilities[1]) if len(probabilities) > 1 else 0.0
            }
            
            logger.debug(f"Risk prediction: {risk_level} (confidence: {confidence:.2f})")
            
            return risk_level, confidence, scores
            
        except ValueError as e:
            logger.warning(f"Invalid input: {str(e)}")
            raise ModelError(f"Invalid input: {str(e)}")
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise ModelError(f"Prediction failed: {str(e)}")
    
    @staticmethod
    def get_sentiment_insights(text: str) -> Dict[str, Any]:
        """
        Get detailed sentiment insights about the text.
        
        Args:
            text: Input text
            
        Returns:
            Dict with insights including:
            - risk_level: HIGH/LOW
            - confidence: Confidence score
            - word_count: Number of words
            - processed_text: Preprocessed text
            - scores: Probability scores
        """
        try:
            risk_level, confidence, scores = SentimentModel.predict_risk(text)
            
            text_processor = get_text_processor()
            processed_text = text_processor.preprocess(text)
            word_count = len(processed_text.split())
            
            return {
                "risk_level": risk_level,
                "confidence": round(confidence, 4),
                "word_count": word_count,
                "text_length": len(text),
                "processed_text": processed_text,
                "scores": scores
            }
            
        except Exception as e:
            logger.error(f"Failed to get sentiment insights: {str(e)}")
            return {
                "risk_level": "LOW",
                "confidence": 0.5,
                "word_count": len(text.split()),
                "text_length": len(text),
                "processed_text": "",
                "scores": {"LOW": 0.5, "HIGH": 0.5},
                "error": str(e)
            }


def load_models() -> SentimentModel:
    """Load sentiment models"""
    return SentimentModel.load()


def predict_sentiment(text: str) -> Tuple[str, float, Dict[str, float]]:
    """Predict sentiment/risk from text"""
    return SentimentModel.predict_risk(text)


def get_sentiment_analysis(text: str) -> Dict[str, any]:
    """Get detailed sentiment analysis"""
    return SentimentModel.get_sentiment_insights(text)
