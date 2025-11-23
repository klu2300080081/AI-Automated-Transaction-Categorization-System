import streamlit as st
import json
import joblib
import os
from SafeTransactionPipeline import SafeTransactionPipeline
from pymongo import MongoClient

# -------------------------------
# Load Pipeline
# -------------------------------
@st.cache_resource
def load_pipeline():
    try:
        pipeline = joblib.load("full_pipeline.pkl")
        return pipeline
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

pipeline = load_pipeline()

# -------------------------------
# MongoDB Connector
# -------------------------------
def get_mongo_collection():
    uri = "mongodb+srv://2300080081:Mongodb150@cluster0.uxnkrpu.mongodb.net/?appName=Cluster0"
    if not uri:
        st.error("MongoDB URI not found. Set MONGO_URI environment variable.")
        return None
    client = MongoClient(uri)
    db = client["transaction_categorization"]
    collection = db["user_feedback"]
    return collection


st.title("Transaction Category Prediction (Simple App with Feedback)")

# -------------------------------
# Prediction Section
# -------------------------------
st.subheader("🔮 Predict Category")

merchant = st.text_input("Merchant Name")
timestamp = st.text_input("Timestamp (DD-MM-YYYY HH:MM)")

predicted_result = None

if st.button("Predict"):
    if not pipeline:
        st.error("Model pipeline not loaded.")
    elif not merchant or not timestamp:
        st.warning("Please enter both merchant and timestamp.")
    else:
        try:
            predicted_result = pipeline.predict(merchant, timestamp)
            st.success(f"Category: **{predicted_result['predicted_category']}**")
            st.write("Confidence:", predicted_result["confidence"])
        except Exception as e:
            st.error(f"Prediction error: {e}")

st.markdown("---")

# -------------------------------
# Human Feedback Section
# -------------------------------
st.subheader("🧠 Human Feedback")

if predicted_result:
    st.write(f"Model predicted: **{predicted_result['predicted_category']}**")

    # Load taxonomy for dropdown
    TAX_PATH = "taxonomy.json"
    try:
        taxonomy = json.load(open(TAX_PATH, "r", encoding="utf-8"))
        categories = taxonomy["categories"]
    except:
        categories = []

    correct_category = st.selectbox("Select Correct Category", categories)

    if st.button("Submit Feedback"):
        coll = get_mongo_collection()
        if coll:
            feedback_doc = {
                "merchant": merchant,
                "timestamp": timestamp,
                "model_predicted": predicted_result["predicted_category"],
                "correct_category": correct_category
            }
            res = coll.insert_one(feedback_doc)
            st.success(f"Feedback submitted (ID: {res.inserted_id})")
else:
    st.info("Make a prediction first to submit feedback.")

st.markdown("---")

# -------------------------------
# Taxonomy Editor
# -------------------------------
st.subheader("⚙️ Edit Taxonomy")

try:
    taxonomy = json.load(open("taxonomy.json", "r", encoding="utf-8"))
    current_categories = taxonomy["categories"]
except:
    st.error("Could not load taxonomy.json.")
    current_categories = []

st.write("### Current Categories:")
for i, c in enumerate(current_categories, start=1):
    st.write(f"{i}. {c}")

st.write("### Edit Categories (same count required):")
new_text = st.text_area("One category per line", "\n".join(current_categories))

if st.button("Save Taxonomy"):
    new_list = [x.strip() for x in new_text.split("\n") if x.strip()]

    if len(new_list) != len(current_categories):
        st.error("❌ Category count must MATCH the existing taxonomy. Changing count requires retraining.")
    else:
        taxonomy["categories"] = new_list
        with open("taxonomy.json", "w", encoding="utf-8") as f:
            json.dump(taxonomy, f, indent=2)
        if pipeline:
            pipeline.categories = new_list
        st.success("✅ taxonomy.json updated successfully!")
