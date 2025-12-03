import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# CRITICAL: Import SafeTransactionPipeline BEFORE any service that uses it
from SafeTransactionPipeline import SafeTransactionPipeline

from datetime import datetime

from services.prediction_service import PredictionService
from services.transaction_service import TransactionService
from styles.app_styles import load_css

st.set_page_config(
    page_title="Transaction Prediction",
    page_icon="🔮",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

def check_authentication():
    if not st.session_state.get("authenticated", False):
        st.error("Please login first to access this page")
        if st.button("Go to Login Page"):
            st.switch_page("pages/1_🔐_Login.py")
        st.stop()

def get_confidence_badge(confidence):
    if confidence >= 0.8:
        return f'<span class="confidence-high">High: {confidence:.2%}</span>'
    elif confidence >= 0.5:
        return f'<span class="confidence-medium">Medium: {confidence:.2%}</span>'
    else:
        return f'<span class="confidence-low">Low: {confidence:.2%}</span>'

def main():
    check_authentication()
    
    st.markdown('<h1 class="custom-header">🔮 Transaction Category Prediction</h1>', unsafe_allow_html=True)
    
    # Navigation bar at the top
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**👤 {st.session_state.user_data['username']}** | {st.session_state.user_data['email']}")
    with col2:
        if st.button("📜 History", use_container_width=True):
            st.switch_page("pages/3_📜_History.py")
    with col3:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/4_ℹ️_About.py")
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.switch_page("pages/1_🔐_Login.py")
    
    st.markdown("---")
    
    # Initialize services
    prediction_service = PredictionService()
    transaction_service = TransactionService()
    
    # Check if model is loaded
    if not prediction_service.is_model_loaded():
        st.error("⚠️ Prediction model is not loaded. Please ensure 'full_pipeline.pkl' exists.")
        return
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### Enter Transaction Details")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        merchant = st.text_input(
            "Merchant Name",
            placeholder="e.g., Starbucks Mumbai #221",
            help="Enter the merchant or store name"
        )
    
    with col2:
        use_current_time = st.checkbox("Use Current Time", value=True)
    
    if use_current_time:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"Using current timestamp: {timestamp}")
    else:
        col3, col4 = st.columns(2)
        with col3:
            date = st.date_input("Date", value=datetime.now())
        with col4:
            time = st.time_input("Time", value=datetime.now().time())
        timestamp = f"{date} {time}"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predict button
    if st.button("🎯 Predict Category", use_container_width=True, type="primary"):
        if not merchant:
            st.error("Please enter a merchant name")
        else:
            with st.spinner("Analyzing transaction..."):
                result = prediction_service.predict_transaction(merchant, timestamp)
                
                if result["success"]:
                    prediction_data = result["result"]
                    
                    # Display results
                    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                    st.markdown("### 🎉 Prediction Results")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Merchant:** {prediction_data['merchant']}")
                        st.markdown(f"**Timestamp:** {prediction_data['timestamp']}")
                        st.markdown(f"**Predicted Category:** `{prediction_data['predicted_category']}`")
                    
                    with col2:
                        st.markdown("**Confidence Level:**")
                        st.markdown(
                            get_confidence_badge(prediction_data['confidence']),
                            unsafe_allow_html=True
                        )
                    
                    # Save to database
                    save_result = transaction_service.save_transaction(
                        user_id=st.session_state.user_data['user_id'],
                        merchant=prediction_data['merchant'],
                        timestamp=prediction_data['timestamp'],
                        category=prediction_data['predicted_category'],
                        confidence=prediction_data['confidence'],
                        raw_scores=prediction_data['raw_scores']
                    )
                    
                    if save_result["success"]:
                        st.success("✅ Transaction saved to history!")
                    else:
                        st.warning("⚠️ Prediction successful but couldn't save to database")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show detailed scores
                    with st.expander("📊 View Detailed Scores"):
                        import pandas as pd
                        import json
                        
                        # Load taxonomy
                        try:
                            with open("taxonomy.json", "r") as f:
                                taxonomy = json.load(f)
                            categories = taxonomy["categories"]
                        except:
                            categories = [f"Category {i}" for i in range(len(prediction_data['raw_scores']))]
                        
                        scores_df = pd.DataFrame({
                            "Category": categories,
                            "Probability": prediction_data['raw_scores']
                        })
                        scores_df = scores_df.sort_values("Probability", ascending=False)
                        scores_df["Probability"] = scores_df["Probability"].apply(lambda x: f"{x:.2%}")
                        
                        st.dataframe(scores_df, use_container_width=True, hide_index=True)
                    
                    st.balloons()
                else:
                    st.error(f"Prediction failed: {result['message']}")
    
    # Recent predictions preview
    st.markdown('<h2 class="custom-subheader">📋 Recent Predictions</h2>', unsafe_allow_html=True)
    
    recent_transactions = transaction_service.get_user_transactions(
        st.session_state.user_data['user_id'],
        limit=5
    )
    
    if recent_transactions:
        for idx, trans in enumerate(recent_transactions):
            st.markdown('<div class="transaction-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{trans['merchant']}**")
                st.caption(trans['timestamp'])
            
            with col2:
                st.markdown(f"Category: `{trans['category']}`")
            
            with col3:
                st.markdown(
                    get_confidence_badge(trans['confidence']),
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No recent predictions. Make your first prediction above!")

if __name__ == "__main__":
    main()