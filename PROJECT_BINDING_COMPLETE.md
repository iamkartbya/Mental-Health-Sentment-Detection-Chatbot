# Milo AI - Complete File Binding Summary

## Project Overview
Milo AI is a mental health support chatbot with sentiment analysis capabilities, created for Sathyabama Institute of Science and Technology.

**Created by:** Kartbya Kumar  
**Institution:** Sathyabama Institute of Science and Technology, Chennai

---

## Architecture & Module Bindings

### 1. Configuration Layer
**Files:** `config.py`, `.env`

- **config.py**: Central configuration management
  - MongoConfig: MongoDB connection settings
  - GeminiConfig: Google Gemini API settings
  - AppConfig: Main application configuration
  - load_config(): Loads environment variables into AppConfig singleton

**Bindings:**
- All modules import `CONFIG` from config.py
- Environment variables are loaded via python-dotenv

---

### 2. Database Layer
**Files:** `database.py`, `mongo_db.py` (deprecated)

**Primary Module: `database.py`**
- Database: Singleton class for MongoDB connection
- Collections available: users, chats, messages
- Functions:
  - get_database(): Get Database instance
  - get_users_collection(): Get users collection
  - get_chats_collection(): Get chats collection
  - get_messages_collection(): Get messages collection

**Deprecated Module: `mongo_db.py`**
- Replaced by database.py with better error handling and proper configuration
- Still referenced in auth_mongo.py (updated to use database.py)

**Bindings:**
- All modules that need database access import from database.py:
  - auth_service.py → get_users_collection()
  - chat_service.py → get_chats_collection(), get_messages_collection()
  - chat_db.py → Uses database module functions

---

### 3. Authentication Layer
**Files:** `auth_service.py`, `auth_mongo.py`, `login.py`, `signup.py`, `ui_login.py`, `ui_signup.py`

**Primary Module: `auth_service.py`**
- AuthService class with methods:
  - signup(email, password): Create new user
  - login(email, password): Authenticate user
  - change_password(email, old_password, new_password): Change password
- Convenience functions:
  - signup_user(email, password)
  - login_user(email, password)
  - change_user_password(email, old_password, new_password)

**Supporting Module: `auth_mongo.py`**
- Legacy authentication functions (now wrapper-like)
- Uses database.py instead of direct mongo_db imports
- signup(email, password): User registration
- login(email, password): User authentication

**UI Modules:**
- `login.py`: Shows login interface, calls AuthService.login()
- `signup.py`: Shows signup interface, calls AuthService.signup()
- `ui_login.py`: Enhanced login UI with captcha
- `ui_signup.py`: Enhanced signup UI with password strength

**Bindings:**
```
login.py → AuthService.login() → database.get_users_collection()
signup.py → AuthService.signup() → database.get_users_collection()
ui_login.py → auth_service.login_user()
ui_signup.py → auth_service.signup_user()
```

---

### 4. Chat & Message Management
**Files:** `chat_service.py`, `chat_db.py`

**Primary Module: `chat_service.py`**
- ChatService class with methods:
  - create_chat(): Create new chat
  - save_message(): Save message to database
  - load_chat(): Load chat history
  - get_user_chats(): Get all user chats
  - delete_chat(): Delete a chat
  - rename_chat(): Rename a chat
- Convenience functions:
  - create_new_chat()
  - save_chat_message()
  - load_chat_history()
  - get_all_user_chats()
  - delete_user_chat()
  - rename_user_chat()

**Supporting Module: `chat_db.py`**
- Legacy chat functions (now uses database.py)
- Functions: create_chat(), save_message(), load_chat(), get_user_chats(), delete_chat(), rename_chat()

**Bindings:**
```
chat_db.py → database.get_chats_collection(), database.get_messages_collection()
chat_service.py → database.get_chats_collection(), database.get_messages_collection()
app.py → chat_db.py functions
```

---

### 5. AI Services
**Files:** `ai_service.py`

- AIService class with methods:
  - initialize(): Initialize Gemini client
  - get_client(): Get Gemini client (singleton)
  - get_system_prompt(): Get system prompt for Milo AI
  - get_response(): Get AI response (async)
- Convenience function:
  - get_ai_response(): Synchronous AI response wrapper

**Bindings:**
```
ai_service.py → CONFIG (for API key)
app.py → AIService.initialize() → AIService.get_client()
```

---

### 6. Sentiment Analysis & ML
**Files:** `sentiment_model.py`, `train_model.py`, `test_gemini.py`

**Primary Module: `sentiment_model.py`**
- SentimentModel class (singleton) with methods:
  - load(): Load ML models from disk
  - predict_risk(text): Predict depression risk (HIGH/LOW)
  - get_sentiment_insights(text): Get detailed sentiment analysis
- Convenience function:
  - predict_sentiment(text): Wrapper for predict_risk()

**Supporting Modules:**
- `train_model.py`: Trains and saves ML models (model.pkl, vectorizer.pkl)
- `test_gemini.py`: Tests Gemini API integration

**Bindings:**
```
sentiment_model.py → utils.get_text_processor() (for text preprocessing)
sentiment_model.py → CONFIG (for model paths)
app.py → SentimentModel.load() → SentimentModel.predict_risk()
```

---

### 7. Utilities & Helpers
**Files:** `utils.py`, `validators.py`, `logger.py`, `exceptions.py`

**utils.py:**
- TextProcessor: Singleton class for NLP preprocessing
- Functions:
  - get_text_processor(): Get TextProcessor instance
  - generate_chat_title(text): Generate title from first message
  - format_timestamp(timestamp): Format MongoDB timestamps
  - truncate_text(text, max_length): Truncate text for display

**validators.py:**
- Functions:
  - validate_email(email): Validate email format
  - validate_password(password): Validate password strength
  - calculate_password_strength(password): Get password strength score
  - validate_text_input(text, min_length, max_length): Validate general text input

**logger.py:**
- setup_logger(name): Create configured logger instance
- Module-level logger instance

**exceptions.py:**
- MiloException: Base exception class
- Specific exceptions:
  - AuthenticationError
  - UserNotFoundError
  - UserAlreadyExistsError
  - DatabaseError
  - ModelError
  - AIServiceError
  - ValidationError
  - ChatNotFoundError

**Bindings:**
```
All modules → logger.setup_logger(__name__)
All validation → validators module
auth_service.py, chat_service.py → exceptions module
```

---

### 8. UI & Styling
**Files:** `css.py`, `ui_styles.py`

- **css.py**: 
  - load_auth_css(): Load authentication page CSS
  - load_chat_css(): Load chat page CSS

- **ui_styles.py**: Additional UI styling utilities

**Bindings:**
```
app.py → css.load_auth_css(), css.load_chat_css()
login.py, signup.py → CSS loaded via app.py context
```

---

### 9. Main Application
**Files:** `app.py`, `app_enhanced.py`

**app.py (Primary entry point):**
- Imports all modules and binds them together
- Streamlit app configuration
- Session state management
- Page routing (login, signup, chat)
- Model loading and caching
- Chat interface and AI interaction

**app_enhanced.py:**
- Alternative implementation with enhanced features
- Uses ChatService, AIService, SentimentModel
- Structured service layer approach

**Bindings:**
```
app.py →
  - login (login.py)
  - signup (signup.py)
  - chat_db (chat_db.py)
  - css (css.py)
  - database (database.py)
  - ai_service (ai_service.py)
  - sentiment_model (sentiment_model.py)
  - utils (utils.py)
  - config (config.py)
  - logger (logger.py)
```

---

## Module Dependency Graph

```
┌─────────────────────────────────────────┐
│         CONFIGURATION LAYER             │
│         config.py (CONFIG singleton)    │
└─────────────────────────────────────────┘
           ↑        ↑        ↑
           │        │        │
    ┌──────┴────────┴────────┴──────┐
    │                               │
┌───▼──────────┐      ┌────────────▼─┐
│ DATABASE     │      │ AI SERVICES  │
│ database.py  │      │ ai_service   │
└────┬─────────┘      │ sentiment    │
     │                │ _model.py    │
     │                └──────────────┘
┌────▼──────────────┐
│ DOMAIN LAYERS    │
│                  │
├─ auth_service   │  → get_users_collection()
├─ chat_service   │  → get_chats_collection()
├─ chat_db.py     │  → get_messages_collection()
└────┬─────────────┘
     │
┌────▼──────────────────────┐
│ UI LAYER                  │
├─ login.py                 │ → AuthService
├─ signup.py                │ → AuthService
├─ ui_login.py              │ → auth_service
├─ ui_signup.py             │ → auth_service
├─ css.py                   │
└────┬──────────────────────┘
     │
┌────▼──────────────┐
│ MAIN APP          │
│ app.py            │
│ (Streamlit entry) │
└───────────────────┘
```

---

## Import Patterns Used

### Pattern 1: Singleton Configuration
```python
from config import CONFIG
# Access: CONFIG.mongo.connection_uri, CONFIG.gemini.api_key
```

### Pattern 2: Database Access
```python
from database import get_users_collection, get_chats_collection, get_messages_collection
collection = get_users_collection()
```

### Pattern 3: Service Classes
```python
from auth_service import AuthService
user = AuthService.login(email, password)
```

### Pattern 4: Logging
```python
from logger import setup_logger
logger = setup_logger(__name__)
logger.info("Message")
```

### Pattern 5: Exceptions
```python
from exceptions import AuthenticationError, ValidationError
try:
    AuthService.login(email, password)
except AuthenticationError as e:
    logger.error(f"Auth failed: {e}")
```

---

## File Binding Changes Made

### 1. **app.py**
- ✅ Added proper imports for database, ai_service, sentiment_model
- ✅ Added logger initialization
- ✅ Unified all service imports

### 2. **login.py**
- ✅ Changed `import auth_mongo as auth` → `from auth_service import AuthService`
- ✅ Updated auth.login() calls → `AuthService.login()`
- ✅ Added error handling with proper exceptions

### 3. **signup.py**
- ✅ Changed `import auth_mongo as auth` → `from auth_service import AuthService`
- ✅ Updated auth.signup() calls → `AuthService.signup()`
- ✅ Added error handling with proper exceptions

### 4. **chat_db.py**
- ✅ Changed `from mongo_db import ...` → `from database import get_chats_collection, get_messages_collection`
- ✅ Updated all functions to call get_collections() dynamically

### 5. **auth_mongo.py**
- ✅ Changed `from mongo_db import users_collection` → `from database import get_users_collection`
- ✅ Updated functions to call get_users_collection() dynamically
- ✅ Added logging and error handling

### 6. **sentiment_model.py**
- ✅ Added missing `Dict, Any` imports from typing

### 7. **__init__.py (NEW)**
- ✅ Created package initialization file
- ✅ Exports all public APIs
- ✅ Provides clean module interface

---

## Testing Checklist

- [ ] Environment variables (.env) configured
- [ ] MongoDB connection with CONFIG
- [ ] Authentication flow (signup → login)
- [ ] Chat creation and message storage
- [ ] AI response generation
- [ ] Sentiment analysis predictions
- [ ] Error handling for all exception cases
- [ ] Logger output correctly formatted

---

## Database Schema

### Collections Structure:

**users collection:**
```json
{
  "username": "email@example.com",
  "email": "email@example.com",
  "password": "hashed_password",
  "created_at": "datetime",
  "updated_at": "datetime",
  "last_login": "datetime",
  "is_active": true
}
```

**chats collection:**
```json
{
  "user_id": "email@example.com",
  "chat_id": "uuid",
  "title": "Chat Title",
  "created_at": "datetime",
  "updated_at": "datetime",
  "message_count": 0,
  "is_archived": false
}
```

**messages collection:**
```json
{
  "user_id": "email@example.com",
  "chat_id": "uuid",
  "role": "user|assistant|system",
  "content": "message text",
  "timestamp": "datetime",
  "metadata": {
    "sentiment": "HIGH|LOW",
    "confidence": 0.95
  }
}
```

---

## Environment Variables Required

```env
MONGO_USER=<username>
MONGO_PASS=<password>
MONGO_CLUSTER=<cluster_name>
GEMINI_API_KEY=<api_key>
DEBUG=false
LOG_LEVEL=INFO
```

---

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Alternative enhanced version
streamlit run app_enhanced.py
```

---

## Conclusion

All files in the Milo AI project have been successfully bound together with:
- ✅ Unified configuration management
- ✅ Centralized database access
- ✅ Consistent error handling
- ✅ Proper logging throughout
- ✅ Clear module dependencies
- ✅ Type hints for better IDE support
- ✅ Service layer architecture

The project is now properly organized with clear separation of concerns and minimal code duplication.
