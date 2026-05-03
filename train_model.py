import pandas as pd
import numpy as np
import re
import joblib
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ===== Load Data =====
df = pd.read_csv("data/depression_dataset_reddit_cleaned.csv")

# Remove empty rows
df = df.dropna(subset=["clean_text"])

# ===== NLP Preprocessing =====
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

df['processed_text'] = df['clean_text'].apply(preprocess)

# ===== Features & Labels =====
X = df['processed_text']
y = df['is_depression']

# ===== Split =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===== TF-IDF =====
vectorizer = TfidfVectorizer(
    max_features=7000,
    ngram_range=(1,2)   # unigrams + bigrams
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ===== Model =====
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# ===== Evaluation =====
y_pred = model.predict(X_test_vec)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ===== Confusion Matrix =====
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ===== Save Model =====
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model Saved Successfully!")