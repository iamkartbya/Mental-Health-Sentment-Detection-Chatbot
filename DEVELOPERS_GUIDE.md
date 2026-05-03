# Milo AI - Developer's Quick Reference Guide

## 🚀 Quick Start

### Import Essentials
```python
# Configuration
from config import CONFIG

# Database
from database import get_users_collection, get_chats_collection, get_messages_collection

# Authentication
from auth_service import AuthService, signup_user, login_user

# Chat Management
from chat_service import ChatService, create_new_chat, save_chat_message

# AI & Sentiment
from ai_service import AIService
from sentiment_model import SentimentModel

# Utilities
from logger import setup_logger
from exceptions import AuthenticationError, DatabaseError
from utils import get_text_processor
from validators import validate_email, validate_password
```

---

## 📋 Common Tasks

### 1. User Authentication

**Sign Up:**
```python
from auth_service import AuthService
from exceptions import UserAlreadyExistsError, ValidationError

try:
    user = AuthService.signup("user@example.com", "secure_password")
    print(f"User created: {user['id']}")
except UserAlreadyExistsError:
    print("User already exists")
except ValidationError as e:
    print(f"Validation error: {e}")
```

**Login:**
```python
from auth_service import AuthService
from exceptions import AuthenticationError

try:
    user = AuthService.login("user@example.com", "password")
    print(f"Logged in: {user['email']}")
except AuthenticationError:
    print("Invalid credentials")
```

### 2. Create and Manage Chats

**Create Chat:**
```python
from chat_service import ChatService
import uuid

chat_id = str(uuid.uuid4())
chat = ChatService.create_chat(
    user_id="user@example.com",
    chat_id=chat_id,
    first_message="Hello, how are you?"
)
```

**Save Message:**
```python
message = ChatService.save_message(
    user_id="user@example.com",
    chat_id=chat_id,
    role="user",  # "user", "assistant", or "system"
    content="Hello!",
    metadata={"sentiment": "HIGH", "confidence": 0.95}
)
```

**Load Chat:**
```python
messages = ChatService.load_chat(
    user_id="user@example.com",
    chat_id=chat_id
)
# Returns: [{"role": "user", "content": "..."}, ...]
```

**Get User's Chats:**
```python
chats = ChatService.get_user_chats("user@example.com", limit=50)
```

### 3. AI Responses

**Initialize Gemini:**
```python
from ai_service import AIService

AIService.initialize()  # Do once at app startup
```

**Get AI Response:**
```python
from ai_service import AIService

messages = [
    {"role": "system", "content": AIService.get_system_prompt()},
    {"role": "user", "content": "I'm feeling anxious"}
]

response = AIService.get_ai_response(
    messages=messages,
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1000
)
```

### 4. Sentiment Analysis

**Predict Risk:**
```python
from sentiment_model import SentimentModel

SentimentModel.load()  # Do once at app startup

risk_level, confidence, scores = SentimentModel.predict_risk(
    "I've been feeling really down lately..."
)
# Returns: ("HIGH"/"LOW", 0.0-1.0, {"LOW": ..., "HIGH": ...})
```

**Get Detailed Insights:**
```python
insights = SentimentModel.get_sentiment_insights(
    "I'm having a bad day"
)
# Returns detailed analysis with risk level, confidence, word count, etc.
```

### 5. Text Processing

**Preprocess Text:**
```python
from utils import get_text_processor

processor = get_text_processor()
cleaned_text = processor.preprocess("Hello! How are you?")
# Returns: "hello how are"
```

**Generate Chat Title:**
```python
from utils import generate_chat_title

title = generate_chat_title("I'm feeling anxious about my presentation")
# Returns: "I'm feeling anxious about my pres..." (truncated to 50 chars)
```

### 6. Input Validation

**Validate Email:**
```python
from validators import validate_email
from exceptions import ValidationError

try:
    validate_email("user@example.com")
except ValidationError as e:
    print(f"Invalid email: {e}")
```

**Validate Password:**
```python
from validators import validate_password, calculate_password_strength

try:
    validate_password("MySecure123!")
    score, label, color = calculate_password_strength("MySecure123!")
    print(f"Password strength: {label}")
except ValidationError as e:
    print(f"Invalid password: {e}")
```

**Validate Text Input:**
```python
from validators import validate_text_input

try:
    validate_text_input("Hello world", min_length=1, max_length=100)
except ValidationError as e:
    print(f"Invalid text: {e}")
```

### 7. Logging

**Setup Logger:**
```python
from logger import setup_logger

logger = setup_logger(__name__)

logger.info("Application started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
```

### 8. Error Handling

**Common Exceptions:**
```python
from exceptions import (
    AuthenticationError,      # Authentication failed
    UserNotFoundError,        # User doesn't exist
    UserAlreadyExistsError,   # User already registered
    DatabaseError,            # DB operation failed
    ModelError,               # ML model error
    AIServiceError,           # Gemini API error
    ValidationError,          # Input validation failed
    ChatNotFoundError         # Chat doesn't exist
)

try:
    # Some operation
    pass
except ValidationError as e:
    print(f"Input validation failed: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
except (AuthenticationError, AIServiceError, ModelError) as e:
    print(f"Operation failed: {e}")
```

---

## 🔧 Configuration

**Access Configuration:**
```python
from config import CONFIG

print(CONFIG.mongo.cluster)       # MongoDB cluster
print(CONFIG.gemini.api_key)      # Gemini API key
print(CONFIG.debug)               # Debug mode
print(CONFIG.log_level)           # Log level
print(CONFIG.db_connection_timeout)  # DB timeout (ms)
print(CONFIG.model_path)          # ML model path
print(CONFIG.vectorizer_path)     # Vectorizer path
```

---

## 📊 Database Direct Access

**Get Collections:**
```python
from database import (
    get_users_collection,
    get_chats_collection,
    get_messages_collection
)

# Collections are PyMongo Collection objects
users = get_users_collection()
chats = get_chats_collection()
messages = get_messages_collection()

# Use standard MongoDB operations
user = users.find_one({"email": "user@example.com"})
chats.insert_one({"user_id": "123", "title": "Chat"})
messages.update_one({"_id": "..."}, {"$set": {"content": "..."}})
```

---

## ⚙️ Session State (Streamlit)

**Login Flow:**
```python
# After successful login
st.session_state.user = user_email
st.session_state.page = "chat"
st.session_state.chat_id = str(uuid.uuid4())

# Check authentication
if st.session_state.user is None:
    show_auth_page()
else:
    show_chat_page()
```

---

## 🎨 UI Styling

**Load CSS:**
```python
from css import load_auth_css, load_chat_css

# Load authentication CSS
load_auth_css()

# OR load chat CSS
load_chat_css()
```

---

## 📁 Module Overview

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| config.py | Configuration management | CONFIG, MongoConfig, GeminiConfig |
| database.py | Database connection | Database, get_*_collection() |
| auth_service.py | User authentication | AuthService, login_user(), signup_user() |
| chat_service.py | Chat management | ChatService, save_chat_message() |
| ai_service.py | Gemini AI integration | AIService, get_ai_response() |
| sentiment_model.py | Sentiment analysis | SentimentModel, predict_sentiment() |
| utils.py | Utilities | TextProcessor, generate_chat_title() |
| validators.py | Input validation | validate_email(), validate_password() |
| logger.py | Logging setup | setup_logger() |
| exceptions.py | Custom exceptions | All MiloException subclasses |
| css.py | UI styling | load_auth_css(), load_chat_css() |

---

## 🔍 Debugging Tips

**Enable Debug Logging:**
```bash
export LOG_LEVEL=DEBUG
export DEBUG=true
```

**Check Database Connection:**
```python
from database import Database
try:
    db = Database.connect()
    print("✅ Database connected")
except Exception as e:
    print(f"❌ Database error: {e}")
```

**Test Gemini Connection:**
```python
from ai_service import AIService
try:
    AIService.initialize()
    print("✅ Gemini initialized")
except Exception as e:
    print(f"❌ Gemini error: {e}")
```

**Test Model Loading:**
```python
from sentiment_model import SentimentModel
try:
    SentimentModel.load()
    print("✅ Models loaded")
except Exception as e:
    print(f"❌ Model error: {e}")
```

---

## 📝 Best Practices

1. **Always use logger:**
   ```python
   logger = setup_logger(__name__)
   logger.info("Starting operation...")
   ```

2. **Use service classes, not direct DB access:**
   ```python
   # ✅ Good
   from auth_service import AuthService
   user = AuthService.login(email, password)
   
   # ❌ Avoid
   from database import get_users_collection
   users = get_users_collection()
   # Direct collection access
   ```

3. **Handle exceptions properly:**
   ```python
   try:
       result = AuthService.signup(email, password)
   except ValidationError as e:
       logger.warning(f"Validation error: {e}")
   except DatabaseError as e:
       logger.error(f"Database error: {e}")
   ```

4. **Use type hints:**
   ```python
   def process_message(user_id: str, content: str) -> Dict[str, Any]:
       """Process and save a message"""
       pass
   ```

5. **Validate user input:**
   ```python
   from validators import validate_text_input
   try:
       validate_text_input(user_input, max_length=5000)
   except ValidationError as e:
       show_error(str(e))
   ```

---

## 🚨 Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| ValidationError | Invalid input format | Check validate_email(), validate_password() |
| DatabaseError | DB connection failed | Check .env configuration and MongoDB |
| AuthenticationError | Wrong credentials | Verify email/password |
| ModelError | Models not loaded | Call SentimentModel.load() |
| AIServiceError | Gemini API issue | Check API key and initialize |
| UserNotFoundError | User doesn't exist | Check user email |
| UserAlreadyExistsError | User exists | User already registered |
| ChatNotFoundError | Chat doesn't exist | Verify chat_id |

---

## 📞 Support

For issues or questions, refer to:
- `PROJECT_BINDING_COMPLETE.md` - Complete architecture documentation
- `MIGRATION_GUIDE.md` - Migration documentation
- `ENHANCEMENT_SUMMARY.md` - Enhancement details
- `README.md` - Project overview
