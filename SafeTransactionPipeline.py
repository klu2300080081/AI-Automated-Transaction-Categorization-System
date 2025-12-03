import numpy as np
import re
import pandas as pd
from sentence_transformers import SentenceTransformer

class SafeTransactionPipeline:

    def __init__(self, model, embedder_name, taxonomy):
        self.model = model
        self.embedder_name = embedder_name
        self.embedder = SentenceTransformer(embedder_name)
        self.categories = taxonomy["categories"]

    def clean_merchant(self, text):
        text = str(text)
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.lower().strip()

    def extract_time_features(self, ts):
        ts = pd.to_datetime(ts)
        return np.array([
            ts.hour,
            ts.dayofweek,
            ts.day,
            ts.month
        ])

    def embed(self, merchant):
        merchant = self.clean_merchant(merchant)
        vec = self.embedder.encode([merchant])
        return np.array(vec).reshape(1, -1)

    def prepare_features(self, merchant, timestamp):
        emb = self.embed(merchant)
        time_feats = self.extract_time_features(timestamp).reshape(1, -1)
        return np.hstack([emb, time_feats])

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
