import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import pandas as pd

from services.transaction_service import TransactionService
from styles.app_styles import load_css

st.set_page_config(
    page_title="Transaction History",
    page_icon="📜",
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

def get_confidence_badge_text(confidence):
    if confidence >= 0.8:
        return "High"
    elif confidence >= 0.5:
        return "Medium"
    else:
        return "Low"

def main():
    check_authentication()
    
    st.markdown('<h1 class="custom-header">📜 Transaction History</h1>', unsafe_allow_html=True)
    
    # Navigation bar at the top
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**👤 {st.session_state.user_data['username']}** | {st.session_state.user_data['email']}")
    with col2:
        if st.button("🔮 Prediction", use_container_width=True):
            st.switch_page("pages/2_🔮_Prediction.py")
    with col3:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/4_ℹ️_About.py")
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.switch_page("pages/1_🔐_Login.py")
    
    st.markdown("---")
    
    # Initialize service
    transaction_service = TransactionService()
    
    # Get statistics
    stats = transaction_service.get_transaction_stats(st.session_state.user_data['user_id'])
    
    # Display stats
    st.markdown('<h2 class="custom-subheader">📊 Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown('<div class="stats-label">Total Transactions</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-number">{stats["total_transactions"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if stats["category_distribution"]:
            most_common = max(stats["category_distribution"], key=lambda x: x['count'])
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown('<div class="stats-label">Most Common Category</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stats-number" style="font-size: 1.3em;">{most_common["_id"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stats-label">{most_common["count"]} transactions</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if stats["category_distribution"]:
            unique_categories = len(stats["category_distribution"])
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown('<div class="stats-label">Unique Categories</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stats-number">{unique_categories}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Category distribution chart
    if stats["category_distribution"]:
        st.markdown('<h2 class="custom-subheader">📈 Category Distribution</h2>', unsafe_allow_html=True)
        
        chart_data = pd.DataFrame(stats["category_distribution"])
        chart_data.columns = ["Category", "Count"]
        chart_data = chart_data.sort_values("Count", ascending=False)
        
        st.bar_chart(chart_data.set_index("Category"))
    
    # Transaction history
    st.markdown('<h2 class="custom-subheader">🗂️ All Transactions</h2>', unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns([3, 1])
    with col1:
        search_merchant = st.text_input("🔍 Search by merchant name", "")
    with col2:
        limit = st.selectbox("Show entries", [10, 25, 50, 100], index=1)
    
    # Get transactions
    transactions = transaction_service.get_user_transactions(
        st.session_state.user_data['user_id'],
        limit=limit
    )
    
    if transactions:
        # Filter by search
        if search_merchant:
            transactions = [
                t for t in transactions 
                if search_merchant.lower() in t['merchant'].lower()
            ]
        
        if not transactions:
            st.info("No transactions match your search")
        else:
            # Display transactions
            for idx, trans in enumerate(transactions):
                st.markdown('<div class="transaction-card">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"### {trans['merchant']}")
                    st.caption(f"🕐 {trans['timestamp']}")
                
                with col2:
                    st.markdown("**Category**")
                    st.markdown(f"`{trans['category']}`")
                
                with col3:
                    st.markdown("**Confidence**")
                    confidence_level = get_confidence_badge_text(trans['confidence'])
                    st.markdown(f"{confidence_level}: {trans['confidence']:.2%}")
                
                with col4:
                    with st.expander("📊 Details"):
                        st.write(f"**Transaction ID:** {trans.get('transaction_id', 'N/A')}")
                        st.write(f"**Created:** {trans.get('created_at', 'N/A')}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Download option
            st.markdown("---")
            
            # Convert to DataFrame for download
            df = pd.DataFrame(transactions)
            df = df[['merchant', 'timestamp', 'category', 'confidence']]
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download History as CSV",
                data=csv,
                file_name=f"transaction_history_{st.session_state.user_data['username']}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📭 No transaction history yet. Start by making predictions!")
        if st.button("🔮 Make Your First Prediction", use_container_width=True):
            st.switch_page("pages/2_🔮_Prediction.py")

if __name__ == "__main__":
    main()