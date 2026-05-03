# Milo AI - Module Architecture Diagram

## 🏗️ Complete System Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        MILO AI APPLICATION LAYER                            ║
║                          (Streamlit Web App)                                ║
║                                                                              ║
║                              app.py (main)                                  ║
║                                  │                                          ║
║                ┌─────────────────┼─────────────────┐                        ║
║                │                 │                 │                        ║
║            ┌───▼────┐    ┌──────▼──────┐   ┌─────▼─────┐                   ║
║            │ Login  │    │   Signup    │   │   Chat    │                   ║
║            │UI Flow │    │   UI Flow   │   │Interface  │                   ║
║            └───┬────┘    └──────┬──────┘   └─────┬─────┘                   ║
║                │                │               │                          ║
║                └────────┬────────┘───────────────┘                          ║
╚════════════════════════╪════════════════════════════════════════════════════╝
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼─────┐  ┌─────▼──────┐  ┌────▼─────────┐
    │   login  │  │   signup   │  │   chat_db    │
    │  .py     │  │    .py     │  │    .py       │
    └────┬─────┘  └─────┬──────┘  └────┬─────────┘
         │              │              │
         └──────────┬───┴──────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
│                                                                  │
│   ┌──────────────────┐  ┌──────────────────┐                   │
│   │ AuthService      │  │ ChatService      │                   │
│   ├──────────────────┤  ├──────────────────┤                   │
│   │ • signup()       │  │ • create_chat()  │                   │
│   │ • login()        │  │ • save_message() │                   │
│   │ • change_pwd()   │  │ • load_chat()    │                   │
│   │                  │  │ • get_chats()    │                   │
│   │ auth_mongo.py    │  │ • delete_chat()  │                   │
│   │ (legacy)         │  │ • rename_chat()  │                   │
│   └──────┬───────────┘  └────────┬─────────┘                   │
│          │                       │                              │
│          └───────────────┬───────┘                              │
│                          │                                      │
│        ┌─────────────────┼─────────────────┐                   │
│        │                 │                 │                   │
│   ┌────▼─────────┐  ┌───▼──────────┐  ┌──▼──────────────┐    │
│   │ AIService    │  │ SentimentModel│  │ TextProcessor  │    │
│   ├──────────────┤  ├──────────────┤  ├────────────────┤    │
│   │ • init()     │  │ • load()     │  │ • preprocess() │    │
│   │ • get_resp() │  │ • predict()  │  │ • generate_   │    │
│   │ • get_sys_   │  │ • insights() │  │   title()      │    │
│   │   prompt()   │  │              │  │                │    │
│   └──────┬───────┘  └────┬─────────┘  └────────────────┘    │
│          │                │                                   │
│          └────────┬───────┘                                   │
│                   │                                           │
└───────────────────▼───────────────────────────────────────────┘
                    │
┌───────────────────▼───────────────────────────────────────────┐
│            INFRASTRUCTURE / CORE LAYER                         │
│                                                                │
│   ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│   │ config.py    │  │ database.py  │  │ logger.py       │    │
│   ├──────────────┤  ├──────────────┤  ├─────────────────┤    │
│   │ CONFIG       │  │ Database     │  │ setup_logger()  │    │
│   │ singleton    │  │ singleton    │  │ module logger   │    │
│   │              │  │              │  │                 │    │
│   │ MongoConfig  │  │ get_users()  │  │ All modules     │    │
│   │ GeminiConfig │  │ get_chats()  │  │ use for logging │    │
│   │ AppConfig    │  │ get_msgs()   │  │                 │    │
│   └──────┬───────┘  └──────┬───────┘  └─────────────────┘    │
│          │                 │                                  │
│   ┌──────▼──────────────────▼──────┐  ┌─────────────────┐    │
│   │   validators.py               │  │ exceptions.py   │    │
│   ├───────────────────────────────┤  ├─────────────────┤    │
│   │ • validate_email()            │  │ BaseException   │    │
│   │ • validate_password()         │  │ ├─ Auth Error   │    │
│   │ • validate_text_input()       │  │ ├─ Database Er. │    │
│   │ • calculate_password_str()    │  │ ├─ Model Error  │    │
│   └───────────────────────────────┘  │ ├─ AI Service   │    │
│                                       │ ├─ Validation   │    │
│                                       │ └─ Chat Not    │    │
│                                       │    Found       │    │
│                                       └─────────────────┘    │
└───────────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    ┌───▼──────┐   ┌───▼──────┐   ┌──▼─────────┐
    │ MongoDB  │   │ Gemini   │   │ ML Models  │
    │Database  │   │API       │   │(*.pkl)     │
    └──────────┘   └──────────┘   └────────────┘
```

---

## 📦 Package Structure

```
milo_ai/
├── __init__.py                    ← Package entry point
├── config.py                      ← Configuration management
├── database.py                    ← Database connection & collections
├── logger.py                      ← Logging setup
├── exceptions.py                  ← Custom exception types
│
├── Services/
│   ├── auth_service.py           ← User authentication
│   ├── auth_mongo.py             ← Legacy auth (uses database.py)
│   ├── chat_service.py           ← Chat management
│   ├── chat_db.py                ← Legacy chat (uses database.py)
│   ├── ai_service.py             ← Gemini AI integration
│   └── sentiment_model.py        ← ML sentiment analysis
│
├── Utils/
│   ├── utils.py                  ← Utility functions (TextProcessor)
│   ├── validators.py             ← Input validation functions
│   └── css.py                    ← UI styling
│
├── UI/
│   ├── login.py                  ← Login interface (uses AuthService)
│   ├── signup.py                 ← Signup interface (uses AuthService)
│   ├── ui_login.py               ← Enhanced login UI
│   ├── ui_signup.py              ← Enhanced signup UI
│   └── ui_styles.py              ← UI styling utilities
│
├── Main Application/
│   ├── app.py                    ← Main Streamlit app
│   └── app_enhanced.py           ← Enhanced version
│
├── ML & Training/
│   ├── train_model.py            ← Model training script
│   ├── test_gemini.py            ← Gemini API testing
│   ├── model.pkl                 ← Trained ML model
│   └── vectorizer.pkl            ← Text vectorizer
│
├── Configuration/
│   ├── .env                      ← Environment variables
│   └── requirements.txt          ← Python dependencies
│
├── Data/
│   └── depression_dataset_reddit_cleaned.csv
│
└── Documentation/
    ├── README.md
    ├── PROJECT_BINDING_COMPLETE.md
    ├── DEVELOPERS_GUIDE.md
    ├── BINDING_CHANGES_LOG.md
    ├── COMPLETE_FILE_BINDING_SUMMARY.md
    ├── MIGRATION_GUIDE.md
    ├── ENHANCEMENT_SUMMARY.md
    └── MODULE_ARCHITECTURE_DIAGRAM.md (this file)
```

---

## 🔄 Data Flow Diagrams

### Authentication Flow
```
┌────────┐
│  User  │
└────┬───┘
     │ (email, password)
     ▼
┌──────────────────┐
│    signup.py     │
│  (user interface)│
└────┬─────────────┘
     │
     ▼
┌──────────────────────────┐
│    AuthService.signup()  │
│  (business logic)        │
└────┬─────────────────────┘
     │ (validate, hash)
     ▼
┌──────────────────────────┐
│ database.py              │
│ get_users_collection()   │
└────┬─────────────────────┘
     │ (insert user)
     ▼
┌──────────────────────────┐
│    MongoDB - users       │
│    collection            │
└──────────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  User created response   │
│  Success message shown   │
└──────────────────────────┘
```

### Chat Message Flow
```
┌────────────────┐
│  User Message  │
└────────┬───────┘
         │
         ▼
    ┌────────────────────────┐
    │   app.py               │
    │  (receives message)    │
    └────────┬───────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────────┐  ┌────────────────────┐
│SentimentModel│  │  ChatService       │
│.predict()   │  │.save_message()     │
└────┬─────────┘  └────┬───────────────┘
     │                 │
     │ (HIGH/LOW)      ▼
     │            ┌─────────────────────┐
     │            │database.get_messages│
     │            │_collection()        │
     │            └────┬────────────────┘
     │                 │
     └────────┬────────┘
              ▼
        ┌──────────────────┐
        │  AIService       │
        │.get_response()   │
        └────┬─────────────┘
             │
             ▼
        ┌──────────────────┐
        │ Gemini API       │
        └────┬─────────────┘
             │ (AI response)
             ▼
        ┌──────────────────────┐
        │ ChatService          │
        │ .save_message()      │
        │ (save assistant msg) │
        └────┬─────────────────┘
             │
             ▼
        ┌──────────────────┐
        │ Display response │
        │ to user          │
        └──────────────────┘
```

### Login Flow
```
┌─────────────────────┐
│  User Credentials   │
└────────┬────────────┘
         │
         ▼
    ┌────────────────┐
    │  login.py      │
    │ (UI)           │
    └────┬───────────┘
         │
         ▼
    ┌──────────────────────────┐
    │ AuthService.login()      │
    │ (validate, verify)       │
    └────┬─────────────────────┘
         │
         ▼
    ┌──────────────────────────┐
    │ database.               │
    │ get_users_collection()  │
    └────┬─────────────────────┘
         │
         ▼
    ┌──────────────────────────┐
    │ MongoDB - find user      │
    │ Verify password          │
    └────┬─────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
┌────────┐  ┌────────────┐
│ Valid  │  │ Invalid    │
└────┬───┘  └────┬───────┘
     │           │
     ▼           ▼
┌─────────┐  ┌──────────────┐
│ Login   │  │ Show error   │
│ Success │  │ Try again    │
└─────────┘  └──────────────┘
```

---

## 🔀 Service Layer Details

### AuthService
```
AuthService (Singleton)
├── signup(email, password) → Dict[str, Any]
│   ├── Validate email/password
│   ├── Hash password (bcrypt)
│   ├── Check if user exists
│   ├── Insert into users collection
│   └── Return user info
├── login(email, password) → Dict[str, Any]
│   ├── Find user by email
│   ├── Verify password (bcrypt)
│   └── Return user info or error
└── change_password(email, old_pwd, new_pwd) → bool
    ├── Verify old password
    ├── Hash new password
    └── Update in users collection
```

### ChatService
```
ChatService (Singleton)
├── create_chat(user_id, chat_id, msg) → Dict[str, Any]
│   ├── Generate title from message
│   └── Insert into chats collection
├── save_message(user_id, chat_id, role, content) → Dict[str, Any]
│   ├── Validate content
│   ├── Insert into messages collection
│   └── Update chat metadata
├── load_chat(user_id, chat_id) → List[Dict]
│   ├── Verify chat belongs to user
│   └── Load messages sorted by time
├── get_user_chats(user_id) → List[Dict]
│   └── Get all user's chats
├── delete_chat(user_id, chat_id) → bool
│   ├── Delete chat
│   └── Delete all messages in chat
└── rename_chat(user_id, chat_id, title) → bool
    └── Update chat title
```

### AIService
```
AIService (Singleton)
├── initialize() → AIService
│   └── Initialize Gemini client
├── get_client() → genai.Client
│   └── Return Gemini client
├── get_system_prompt() → str
│   └── Return Milo AI system prompt
├── get_response(messages, model, temp, tokens) → str
│   ├── Call Gemini API
│   └── Return AI response
└── get_ai_response(...) → str
    └── Wrapper for get_response()
```

### SentimentModel
```
SentimentModel (Singleton)
├── load() → SentimentModel
│   ├── Load model.pkl
│   └── Load vectorizer.pkl
├── predict_risk(text) → Tuple[str, float, Dict]
│   ├── Preprocess text
│   ├── Vectorize
│   ├── Predict
│   └── Return (risk_level, confidence, scores)
├── get_sentiment_insights(text) → Dict
│   ├── Get predictions
│   ├── Count words
│   └── Return detailed analysis
└── predict_sentiment(text) → Tuple
    └── Wrapper for predict_risk()
```

---

## 🔌 API Connections

### MongoDB Connection
```
CONFIG (config.py)
  ├── mongo.user
  ├── mongo.password
  ├── mongo.cluster
  └── mongo.connection_uri → mongodb+srv://...

Database (database.py)
  ├── Connect using CONFIG.mongo.connection_uri
  ├── Certificate: certifi.where()
  ├── Timeouts configured
  └── Collections:
      ├── users
      ├── chats
      └── messages
```

### Gemini API Connection
```
CONFIG (config.py)
  └── gemini.api_key

AIService (ai_service.py)
  ├── Initialize with CONFIG.gemini.api_key
  ├── Create genai.Client()
  └── Call:
      ├── models/gemini-2.0-flash
      ├── system_prompt: Milo AI instructions
      └── user_message: Chat message
```

### ML Model
```
CONFIG (config.py)
  ├── model_path: "model.pkl"
  └── vectorizer_path: "vectorizer.pkl"

SentimentModel (sentiment_model.py)
  ├── Load joblib.load(model.pkl)
  ├── Load joblib.load(vectorizer.pkl)
  └── Predict:
      ├── Input: text
      ├── Process: TextProcessor.preprocess()
      ├── Vectorize: vectorizer.transform()
      ├── Predict: model.predict()
      └── Return: risk level, confidence, scores
```

---

## 🧬 Inheritance & Dependency Hierarchy

```
Dependencies (no dependencies):
├── config.py
├── exceptions.py
├── logger.py
└── validators.py

Layer 1 (depends on base):
├── database.py (uses config, logger, exceptions)
└── utils.py (uses logger, validators)

Layer 2 (depends on Layer 1):
├── auth_service.py (uses database, validators, logger, exceptions)
├── chat_service.py (uses database, utils, validators, logger, exceptions)
├── ai_service.py (uses config, logger, exceptions)
└── sentiment_model.py (uses utils, config, logger, exceptions)

Layer 3 (UI - depends on Layer 2):
├── login.py (uses auth_service, logger, exceptions)
├── signup.py (uses auth_service, validators, logger, exceptions)
├── ui_login.py (uses auth_service, exceptions, logger)
└── ui_signup.py (uses auth_service, validators, logger, exceptions)

Layer 4 (App - depends on all):
├── app.py (uses all modules)
└── app_enhanced.py (uses all modules)

No Circular Dependencies ✅
```

---

## 📊 Communication Protocols

### Request-Response Pattern
```
UI/App
  │ Request
  ├─────────────────────┐
  │ (data, parameters)   │
  ▼                      ▼
Service Layer       Database
  │                      │
  │ Process          Query/Insert
  │                      │
  ▼                      ▼
Response           Result
  │                      │
  └──────────┬───────────┘
             ▼
          Return to UI
```

### Error Handling Pattern
```
Try to execute operation
  │
  ├─ Success → Return result
  │
  └─ Error → 
      ├─ Catch specific exception
      ├─ Log error (logger)
      ├─ Handle gracefully
      └─ Re-raise or return error response
```

### Configuration Pattern
```
.env file
  │ (environment variables)
  ▼
config.py (load_config())
  │
  ├─ Parse and validate
  ├─ Create MongoConfig
  ├─ Create GeminiConfig
  ├─ Create AppConfig
  │
  ▼
CONFIG singleton
  │
  └─ Accessed by all modules
```

---

## ✅ Integration Checklist

- [x] All imports properly connected
- [x] No circular dependencies
- [x] Singleton pattern for resources (DB, AI, Models)
- [x] Configuration centralized
- [x] Error handling standardized
- [x] Logging integrated
- [x] Type hints complete
- [x] Service layer abstraction
- [x] Database access unified
- [x] API connections configured
- [x] UI properly bound to services
- [x] No hardcoded values
- [x] Environment-driven setup
- [x] Scalable architecture
- [x] Maintainable code structure

---

## 🚀 Deployment Ready

The architecture supports:
- **Horizontal Scaling:** Stateless services can be replicated
- **Vertical Scaling:** Resources can be increased
- **Load Balancing:** Multiple instances can be load balanced
- **Monitoring:** All modules log and can be monitored
- **Testing:** Service layer enables unit and integration testing
- **Maintenance:** Clear separation of concerns

---

**Architecture Status:** ✅ COMPLETE & OPTIMIZED
