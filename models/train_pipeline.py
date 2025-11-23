import pandas as pd
import numpy as np
import re
import json
import joblib
from sentence_transformers import SentenceTransformer
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# ==============================
# 1. SAFE PIPELINE CLASS 
# ==============================
class SafeTransactionPipeline:

    def __init__(self, model, embedder_name, taxonomy):
        self.model = model
        self.embedder_name = embedder_name
        self.embedder = SentenceTransformer(embedder_name)
        self.categories = taxonomy["categories"]

    # ---- Clean merchant name ----
    def clean_merchant(self, text):
        text = str(text)
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.lower().strip()

    # ---- Extract time features ----
    def extract_time_features(self, ts):
        ts = pd.to_datetime(ts)
        return np.array([
            ts.hour,
            ts.dayofweek,
            ts.day,
            ts.month
        ])

    # ---- Generate embedding safely ----
    def embed(self, merchant):
        merchant = self.clean_merchant(merchant)
        vec = self.embedder.encode([merchant])
        return np.array(vec).reshape(1, -1)

    # ---- Combine features ----
    def prepare_features(self, merchant, timestamp):
        emb = self.embed(merchant)
        time_feats = self.extract_time_features(timestamp).reshape(1, -1)
        return np.hstack([emb, time_feats])

    # ---- Prediction ----
    def predict(self, merchant, timestamp):
        X = self.prepare_features(merchant, timestamp)
        probs = self.model.predict_proba(X)[0]
        idx = np.argmax(probs)

        return {
            "merchant": merchant,
            "timestamp": timestamp,
            "predicted_category": self.categories[idx],
            "confidence": float(probs[idx]),
            "raw_scores": probs.tolist()
        }


# ==============================
# 2. LOAD DATA & TAXONOMY
# ==============================
print("Loading dataset...")

df = pd.read_csv("synthetic_transactions_12000_balanced_unique.csv")

with open("taxonomy.json", "r") as f:
    taxonomy = json.load(f)

categories = taxonomy["categories"]
label2id = {c: i for i, c in enumerate(categories)}
df["label"] = df["category"].map(label2id)

# Time feature extraction
df["time"] = pd.to_datetime(df["time"])
df["hour"] = df["time"].dt.hour
df["dayofweek"] = df["time"].dt.dayofweek
df["day"] = df["time"].dt.day
df["month"] = df["time"].dt.month

# Clean merchant names
def clean_text(t):
    t = str(t)
    t = re.sub(r"[^a-zA-Z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()

df["clean_merchant"] = df["merchant_name"].apply(clean_text)

texts = df["clean_merchant"].tolist()


# ==============================
# 3. LightEmbed Embeddings
# ==============================
print("Generating embeddings using MiniLM...")

embedder_name = "paraphrase-MiniLM-L6-v2"
embedder = SentenceTransformer(embedder_name)
embeddings = embedder.encode(texts, batch_size=64, show_progress_bar=True)

tabular = df[["hour", "dayofweek", "day", "month"]].values
X = np.hstack([embeddings, tabular])
y = df["label"].values


# ==============================
# 4. TRAIN TEST SPLIT
# ==============================
print("Preparing train-test split...")

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ==============================
# 5. TRAIN XGBOOST
# ==============================
print("Training XGBoost model...")

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softprob",
    num_class=len(categories),
    eval_metric="mlogloss"
)

model.fit(X_train, y_train)


# ==============================
# 6. BUILD SAFE PIPELINE
# ==============================
print("Building safe pipeline...")

pipeline = SafeTransactionPipeline(
    model=model,
    embedder_name=embedder_name,
    taxonomy=taxonomy
)


# ==============================
# 7. SAVE PIPELINE SAFELY
# ==============================
print("Saving full pipeline...")

joblib.dump(pipeline, "full_pipeline.pkl")

print("\n🎉 Training complete! Your pipeline is saved as: full_pipeline.pkl")
