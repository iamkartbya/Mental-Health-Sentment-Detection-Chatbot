# Milo AI - Mental Health & Sentiment Detection System

**Your compassionate AI companion for mental health support and sentiment analysis.**

---

## 📋 Overview

Milo AI is an advanced mental health support chatbot that combines:
- **Sentiment Analysis**: Detects depression and mental health concerns using machine learning
- **AI-Powered Conversations**: Uses Google Gemini API for empathetic, supportive responses
- **User Authentication**: Secure sign-up and login with bcrypt password hashing
- **Chat Management**: Persistent chat history with MongoDB
- **Contextual Support**: Remembers conversations and provides personalized support

---

## 🏗️ Project Architecture

### Project Structure

```
mhsd/
├── Core Application
│   ├── app_enhanced.py          # Main Streamlit app (refactored)
│   ├── config.py                # Configuration management
│   ├── logger.py                # Logging setup
│   └── exceptions.py            # Custom exceptions
│
├── Services (Business Logic)
│   ├── auth_service.py          # Authentication service
│   ├── chat_service.py          # Chat management
│   ├── ai_service.py            # Gemini API integration
│   ├── sentiment_model.py       # ML model inference
│   └── database.py              # MongoDB manager
│
├── UI Modules
│   ├── ui_login.py              # Login interface
│   ├── ui_signup.py             # Signup interface
│   └── ui_styles.py             # CSS styling
│
├── Utilities
│   ├── validators.py            # Input validation
│   ├── utils.py                 # Helper functions
│   └── utils/text_processor.py  # NLP preprocessing
│
├── Data & Models
│   ├── train_model.py           # Model training script
│   ├── model.pkl                # Trained model
│   ├── vectorizer.pkl           # TF-IDF vectorizer
│   └── data/
│       └── depression_dataset_reddit_cleaned.csv
│
└── Configuration
    └── requirements.txt         # Python dependencies
```

### Design Patterns

1. **Service Layer Pattern**: Separation of business logic from UI
2. **Singleton Pattern**: For database, AI service, and model management
3. **Dependency Injection**: Services are initialized and passed where needed
4. **Error Handling**: Custom exceptions with proper logging

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Streamlit

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mhsd
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```env
   # MongoDB Configuration
   MONGO_USER=your_mongodb_username
   MONGO_PASS=your_mongodb_password
   MONGO_CLUSTER=your_cluster.mongodb.net


   # Application Settings
   DEBUG=false
   LOG_LEVEL=INFO
   ```

5. **Run the application**
   ```bash
   streamlit run app_enhanced.py
   ```

---

## 📚 Core Modules

### 1. **config.py** - Configuration Management
Centralized configuration using dataclasses and environment variables.

```python
from config import CONFIG

# Access configuration
mongo_uri = CONFIG.mongo.connection_uri
```

### 2. **database.py** - Database Management
Singleton MongoDB manager with connection pooling.

```python
from database import get_database, get_users_collection

db = get_database()
users = get_users_collection()
```

### 3. **auth_service.py** - Authentication
Handles user signup, login, and password management.

```python
from auth_service import signup_user, login_user

# Signup
user = signup_user(\"user@example.com\", \"password123\")

# Login
user = login_user(\"user@example.com\", \"password123\")
```

### 4. **chat_service.py** - Chat Management
Manages chat creation, message storage, and retrieval.

```python
from chat_service import create_new_chat, save_chat_message, load_chat_history

# Create chat
chat = create_new_chat(user_id, chat_id, \"First message\")

# Save message
msg = save_chat_message(user_id, chat_id, \"user\", \"Hello\")

# Load history
messages = load_chat_history(user_id, chat_id)
```

### 5. **sentiment_model.py** - Mental Health Detection
ML-based depression and mental health risk detection.

```python
from sentiment_model import load_models, predict_sentiment

models = load_models()
risk_level, confidence, scores = predict_sentiment(\"I feel depressed\")
```

### 6. **ai_service.py** - Gemini Integration
Google Gemini API integration for empathetic responses.

```python
from ai_service import init_ai, get_ai_response

ai = init_ai()
response = get_ai_response(messages, temperature=0.7)
```

### 7. **validators.py** - Input Validation
Comprehensive input validation utilities.

```python
from validators import validate_email, validate_password, calculate_password_strength

validate_email(\"user@example.com\")
score, label, color = calculate_password_strength(\"MyP@ss123\")
```

### 8. **utils.py** - Utilities
Text processing, formatting, and helper functions.

```python
from utils import get_text_processor, generate_chat_title

processor = get_text_processor()
processed = processor.preprocess(\"Raw text here\")
title = generate_chat_title(\"My first message...\")
```

---

## 🔐 Security Features

1. **Password Security**
   - bcrypt hashing with salt
   - Minimum 8 characters enforced
   - Strength meter with visual feedback

2. **Input Validation**
   - Email format validation
   - Text length limits
   - Special character sanitization

3. **Authentication**
   - Email/password authentication
   - CAPTCHA verification for signup/login
   - Secure session management

4. **Database Security**
   - MongoDB URI encryption
   - TLS connections
   - Connection timeout protection


---

## 📊 Machine Learning Model

### Training Pipeline (`train_model.py`)

The sentiment detection model is trained using:
- **Dataset**: Depression Reddit dataset (cleaned)
- **Features**: TF-IDF vectorization
- **Algorithm**: Multinomial Naive Bayes
- **Preprocessing**: Lemmatization, stopword removal

### Model Performance

- Accuracy: ~87% (on test set)
- Features: 5000 most important terms
- Classes: LOW risk, HIGH risk

### Using the Model

```python
from sentiment_model import predict_sentiment

# Get prediction
risk_level, confidence, scores = predict_sentiment(user_text)

# Example output
# risk_level: \"HIGH\" or \"LOW\"
# confidence: 0.85
# scores: {\"LOW\": 0.15, \"HIGH\": 0.85}
```

---

## 🎨 UI/UX Design

### Components

1. **Authentication Pages**
   - Login with email, password, and CAPTCHA
   - Signup with password strength meter
   - Real-time validation feedback

2. **Chat Interface**
   - Sidebar with chat history
   - Message display with sentiments
   - Real-time AI responses
   - Typing indicator

3. **Styling**
   - Custom CSS with gradients
   - Responsive design
   - Accessible color schemes
   - Smooth animations

---

## 🧪 Error Handling & Logging

### Custom Exceptions

```python
from exceptions import (
    AuthenticationError,
    DatabaseError,
    ModelError,
    AIServiceError,
    ValidationError
)
```

### Logging

```python
from logger import setup_logger

logger = setup_logger(__name__)
logger.info(\"User logged in\")
logger.error(\"Database connection failed\")
```

---

## 📈 System Architecture Diagram

```
┌─────────────────────────────────────────────┐
│        Streamlit UI Frontend                 │
│  ├── ui_login.py                            │
│  ├── ui_signup.py                           │
│  └── ui_styles.py                           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│      Application Logic (app_enhanced.py)     │
└────────────────┬────────────────────────────┘
                 │
     ┌───────────┼───────────────┐
     │           │               │
┌────▼──┐ ┌─────▼────┐ ┌───────▼──────┐
│ Auth  │ │   Chat   │ │     AI &     │
│Service│ │ Service  │ │    Models    │
└────┬──┘ └─────┬────┘ └───────┬──────┘
     │          │              │
┌────▼──────────▼──────────────▼───┐
│      Database Service             │
│  ├── Users Collection             │
│  ├── Chats Collection             │
│  └── Messages Collection          │
└────┬───────────────────────────────┘
     │
┌────▼─────────────┐  ┌─────────────────┐
│   MongoDB        │  │  Gemini API     │
│   (Cloud)        │  │  (Google Cloud) │
└──────────────────┘  └─────────────────┘
```

---

## 🔄 Data Flow

### User Message Flow

```
1. User Input
   ↓
2. Sentiment Analysis (ML Model)
   ↓
3. Message Storage (DB)
   ↓
4. AI Response Generation (Gemini)
   ↓
5. Response Storage (DB)
   ↓
6. Display to User
```

---

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Set environment variables
4. Deploy

### Docker

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app_enhanced.py"]
```

---

## 📝 Environment Variables

```env
# Required
MONGO_USER=username
MONGO_PASS=password
MONGO_CLUSTER=cluster.mongodb.net
GEMINI_API_KEY=your_api_key

# Optional
DEBUG=false
LOG_LEVEL=INFO
MODEL_PATH=model.pkl
VECTORIZER_PATH=vectorizer.pkl
```

---

## 🛠️ Development

### Code Quality

- **Linting**: `flake8 .`
- **Formatting**: `black .`
- **Type Checking**: `mypy .`
- **Testing**: `pytest`

### Project Standards

- Type hints on all functions
- Comprehensive docstrings
- Custom exception handling
- Structured logging
- Configuration management
- Service layer separation

---

## 📝 License

This project is created for educational purposes at Sathyabama Institute of Science and Technology.

---

## 👤 Author

**Kartbya Kumar**
- Institution: Sathyabama Institute of Science and Technology, Chennai
- Email: [your-email]
- GitHub: [your-github]

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [your-email]
- Create a discussion

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Crisis resource integration
- [ ] Mental health resource library
- [ ] Daily wellness check-ins
- [ ] Mood tracking visualization
- [ ] Therapist referral system
- [ ] Anonymous support groups
- [ ] Mobile app
- [ ] Advanced analytics

---

**Last Updated**: May 2024
**Version**: 2.0 (Refactored)
