"""
MIGRATION GUIDE - From Old to New Architecture
Quick reference for transitioning your Milo AI codebase
"""

# ===== QUICK START =====

## Step 1: Backup Your Current Work
```bash
# Create backup
cp -r . ../mhsd_backup
```

## Step 2: Install Updated Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Update Your Main App
- Rename: `app.py` → `app_old.py`
- Use: `app_enhanced.py` as your new main app
- Or rename `app_enhanced.py` → `app.py` if desired

## Step 4: Run the Application
```bash
streamlit run app_enhanced.py
```

---

# ===== IMPORT MIGRATION GUIDE =====

## Authentication

### Old Way
```python
import auth_mongo as auth

user = auth.login(email, password)
success = auth.signup(email, password)
```

### New Way
```python
from auth_service import login_user, signup_user

user = login_user(email, password)
success = signup_user(email, password)
```

---

## Database Operations

### Old Way
```python
from mongo_db import users_collection, chats_collection, messages_collection

users_collection.find_one({"username": email})
chats_collection.insert_one({...})
messages_collection.find({...})
```

### New Way
```python
from database import get_users_collection, get_chats_collection, get_messages_collection

get_users_collection().find_one({"username": email})
get_chats_collection().insert_one({...})
get_messages_collection().find({...})
```

Or use the Database class:
```python
from database import Database

db = Database.get_database()
db.users_collection.find_one({"username": email})
db.chats_collection.insert_one({...})
```

---

## Chat Management

### Old Way
```python
import chat_db

chat_db.create_chat(user_id, chat_id, title)
chat_db.save_message(user_id, chat_id, role, content)
messages = chat_db.load_chat(user_id, chat_id)
chats = chat_db.get_user_chats(user_id)
chat_db.delete_chat(user_id, chat_id)
chat_db.rename_chat(user_id, chat_id, new_title)
```

### New Way
```python
from chat_service import (
    create_new_chat,
    save_chat_message,
    load_chat_history,
    get_all_user_chats,
    delete_user_chat,
    rename_user_chat
)

create_new_chat(user_id, chat_id, "First message")
save_chat_message(user_id, chat_id, "user", "Hello")
messages = load_chat_history(user_id, chat_id)
chats = get_all_user_chats(user_id)
delete_user_chat(user_id, chat_id)
rename_user_chat(user_id, chat_id, "New Title")
```

---

## Model Loading

### Old Way
```python
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

vec = vectorizer.transform([text])
pred = model.predict(vec)[0]
conf = max(model.predict_proba(vec)[0])
```

### New Way
```python
from sentiment_model import load_models, predict_sentiment

models = load_models()  # Loads both model and vectorizer

risk_level, confidence, scores = predict_sentiment(text)
# risk_level: "HIGH" or "LOW"
# confidence: 0.85
# scores: {"LOW": 0.15, "HIGH": 0.85}
```

---

## AI Service

### Old Way
```python
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages
)
```

### New Way
```python
from ai_service import get_ai_response

response = get_ai_response(messages, temperature=0.7)
```

---

## CSS Styling

### Old Way
```python
import css

if user:
    css.load_chat_css()
else:
    css.load_auth_css()
```

### New Way
```python
import ui_styles

if user:
    ui_styles.load_chat_css()
else:
    ui_styles.load_auth_css()
```

---

## UI Components

### Old Way
```python
import login
import signup

if page == "login":
    login.show_login()
else:
    signup.show_signup()
```

### New Way
```python
import ui_login
import ui_signup

if page == "login":
    ui_login.show_login()
else:
    ui_signup.show_signup()
```

---

## Configuration

### Old Way
```python
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))
cluster = os.getenv("MONGO_CLUSTER")
```

### New Way
```python
from config import CONFIG

mongo_uri = CONFIG.mongo.connection_uri
gemini_key = CONFIG.gemini.api_key
log_level = CONFIG.log_level
```

---

## Error Handling

### Old Way
```python
try:
    user = users_collection.find_one({"username": email})
except Exception as e:
    print("Error:", e)
    st.error("An error occurred")
```

### New Way
```python
from exceptions import UserNotFoundError, DatabaseError
from logger import setup_logger

logger = setup_logger(__name__)

try:
    user = login_user(email, password)
except UserNotFoundError:
    logger.warning(f"User not found: {email}")
    st.error("User not found")
except DatabaseError as e:
    logger.error(f"Database error: {str(e)}")
    st.error("Database unavailable")
```

---

## Input Validation

### Old Way
```python
import re

def _is_valid_email(email):
    return bool(re.match(r'^[\w\.\+\-]+@[\w\-]+\.\w{2,}$', email))

if not _is_valid_email(email):
    st.error("Invalid email")
```

### New Way
```python
from validators import validate_email, validate_password
from exceptions import ValidationError

try:
    validate_email(email)
    validate_password(password)
except ValidationError as e:
    st.error(f"❌ {str(e)}")
```

---

## Text Processing

### Old Way
```python
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)
    return " ".join(
        lemmatizer.lemmatize(w)
        for w in words if w not in stop_words
    )

processed = preprocess(raw_text)
```

### New Way
```python
from utils import get_text_processor

processor = get_text_processor()
processed = processor.preprocess(raw_text)
```

---

# ===== COMMON PATTERNS =====

## Authenticating User

### Old
```python
user = auth_mongo.login(email, password)
if user:
    st.session_state.user = email
```

### New
```python
from auth_service import login_user
from exceptions import AuthenticationError

try:
    user = login_user(email, password)
    st.session_state.user = email
    st.success("✅ Login successful!")
except AuthenticationError as e:
    st.error(f"❌ {str(e)}")
```

---

## Creating Chat & Saving Messages

### Old
```python
chat_db.create_chat(user_id, chat_id, "New Chat")
chat_db.save_message(user_id, chat_id, "user", message_text)
chat_db.save_message(user_id, chat_id, "assistant", response_text)
```

### New
```python
from chat_service import create_new_chat, save_chat_message
from sentiment_model import predict_sentiment

# Create chat
create_new_chat(user_id, chat_id, message_text)

# Analyze sentiment
risk_level, confidence, scores = predict_sentiment(message_text)

# Save user message with metadata
save_chat_message(
    user_id, chat_id, "user", message_text,
    metadata={
        "risk_level": risk_level,
        "confidence": float(confidence),
        "scores": scores
    }
)

# Get AI response
response = get_ai_response(messages)

# Save assistant message
save_chat_message(user_id, chat_id, "assistant", response)
```

---

## Loading Chat History

### Old
```python
messages = chat_db.load_chat(user_id, chat_id)
for msg in messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
```

### New
```python
from chat_service import load_chat_history

messages = load_chat_history(user_id, chat_id)
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
```

---

## Sentiment Analysis

### Old
```python
vec = vectorizer.transform([preprocess(text)])
pred = model.predict(vec)[0]
conf = max(model.predict_proba(vec)[0])
risk = "HIGH" if pred == 1 else "LOW"
```

### New
```python
from sentiment_model import predict_sentiment

risk_level, confidence, scores = predict_sentiment(text)
# risk_level: "HIGH" or "LOW"
# confidence: 0.85
# scores: {"LOW": 0.15, "HIGH": 0.85}
```

---

# ===== TROUBLESHOOTING =====

## Issue: "ModuleNotFoundError: No module named 'config'"
**Solution**: Ensure all new Python files are in the same directory as app_enhanced.py

## Issue: "Database connection failed"
**Solution**: 
```python
# Check config
from config import CONFIG
print(CONFIG.mongo.connection_uri)

# Check environment variables
import os
print(os.getenv("MONGO_USER"))
print(os.getenv("MONGO_PASS"))
print(os.getenv("MONGO_CLUSTER"))
```

## Issue: "Models not loading"
**Solution**:
```python
# Check files exist
import os
print(os.path.exists("model.pkl"))
print(os.path.exists("vectorizer.pkl"))

# Check paths in config
from config import CONFIG
print(CONFIG.model_path)
print(CONFIG.vectorizer_path)
```

## Issue: "Gemini API key not recognized"
**Solution**:
```python
# Verify key is set
from config import CONFIG
print(CONFIG.gemini.api_key[:10] + "...")
```

---

# ===== FILE MAPPING =====

## Old → New Files

| Old File | New Location | New Approach |
|----------|-------------|-------------|
| app.py | app_enhanced.py | See app for complete refactor |
| login.py | ui_login.py | UI only, better structure |
| signup.py | ui_signup.py | UI only, better structure |
| auth_mongo.py | auth_service.py | Service layer |
| mongo_db.py | database.py | Database manager |
| chat_db.py | chat_service.py | Service layer |
| css.py | ui_styles.py | Styling module |
| (none) | config.py | NEW - Config management |
| (none) | logger.py | NEW - Logging |
| (none) | exceptions.py | NEW - Error handling |
| (none) | validators.py | NEW - Validation |
| (none) | utils.py | NEW - Utilities |
| (none) | sentiment_model.py | NEW - Model service |
| (none) | ai_service.py | NEW - AI service |

---

# ===== VERIFICATION CHECKLIST =====

After migration, verify:

- [ ] App starts without errors: `streamlit run app_enhanced.py`
- [ ] Login works with valid credentials
- [ ] Signup works and creates new user
- [ ] Chat creation works
- [ ] Messages save to database
- [ ] Sentiment analysis runs
- [ ] Gemini API responses work
- [ ] Logout works
- [ ] Chat history loads
- [ ] No console errors in logs

---

# ===== NEXT STEPS =====

1. **Test Thoroughly**: Run through all features
2. **Monitor Logs**: Check logger output for issues
3. **Backup Database**: Before major changes
4. **Deploy Gradually**: Test in staging first
5. **Document Changes**: Update internal docs

---

**Need Help?** Check the comprehensive README.md or ENHANCEMENT_SUMMARY.md
**Questions?** Review the docstrings in each module for detailed documentation
