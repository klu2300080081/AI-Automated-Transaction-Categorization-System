import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.user_service import UserService
from services.transaction_service import TransactionService
from styles.app_styles import load_css

st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
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

def main():
    check_authentication()
    
    st.markdown('<h1 class="custom-header">👤 User Profile</h1>', unsafe_allow_html=True)
    
    # Navigation bar at the top
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**👤 {st.session_state.user_data['username']}** | {st.session_state.user_data['email']}")
    with col2:
        if st.button("🔮 Prediction", use_container_width=True):
            st.switch_page("pages/2_🔮_Prediction.py")
    with col3:
        if st.button("📜 History", use_container_width=True):
            st.switch_page("pages/3_📜_History.py")
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.switch_page("pages/1_🔐_Login.py")
    
    st.markdown("---")
    
    # Initialize services
    user_service = UserService()
    transaction_service = TransactionService()
    
    # Get user data from database
    user_data = user_service.get_user_by_id(st.session_state.user_data['user_id'])
    
    if user_data:
        # User Information Card
        st.markdown('<h2 class="custom-subheader">📋 Account Information</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Details")
            st.markdown(f"**👤 Username:** {user_data['username']}")
            st.markdown(f"**📧 Email:** {user_data['email']}")
            st.markdown(f"**🆔 User ID:** {user_data['user_id']}")
            st.markdown(f"**📅 Member Since:** {user_data['user_created_on'].strftime('%B %d, %Y')}")
        
        with col2:
            # Get stats
            stats = transaction_service.get_transaction_stats(user_data['user_id'])
            
            st.markdown("### Activity Statistics")
            st.markdown(f"**📊 Total Predictions:** {stats['total_transactions']}")
            
            if stats['category_distribution']:
                most_common = max(stats['category_distribution'], key=lambda x: x['count'])
                st.markdown(f"**🏆 Favorite Category:** {most_common['_id']}")
                st.markdown(f"**🔢 Unique Categories:** {len(stats['category_distribution'])}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About the Application
        st.markdown('<h2 class="custom-subheader">ℹ️ About This Application</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🔮 Transaction Categorization System
        
        This autonomous transaction categorization system uses advanced machine learning 
        to automatically classify your transactions into relevant categories.
        
        #### 🎯 Features:
        - **AI-Powered Predictions**: Uses sentence transformers and machine learning models
        - **Real-time Classification**: Instant category predictions with confidence scores
        - **Transaction History**: Track all your predictions in one place
        - **Secure Authentication**: JWT-based authentication with encrypted passwords
        - **Dark Theme Interface**: Modern, eye-friendly design
        
        #### 📊 Categories:
        - Food & Beverage
        - Groceries
        - Shopping
        - Fuel
        - Transport & Travel
        - Bills & Utilities
        - Entertainment
        - Health & Medical
        - Personal Care
        - Education
        - Financial Services
        - Others / Unknown
        
        #### 🔒 Security:
        - All passwords are hashed using bcrypt
        - JWT tokens for session management
        - MongoDB for secure data storage
        - Environment variables for sensitive data
        
        #### 🛠️ Technology Stack:
        - **Frontend & Backend**: Streamlit
        - **Database**: MongoDB
        - **ML Framework**: Scikit-learn, Sentence Transformers
        - **Authentication**: JWT, Passlib
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown('<h2 class="custom-subheader">⚡ Quick Actions</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### 🔮")
            st.markdown("**New Prediction**")
            if st.button("Predict Now", key="predict_btn", use_container_width=True):
                st.switch_page("pages/2_🔮_Prediction.py")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### 📜")
            st.markdown("**View History**")
            if st.button("See History", key="history_btn", use_container_width=True):
                st.switch_page("pages/3_📜_History.py")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### 🚪")
            st.markdown("**Logout**")
            if st.button("Sign Out", key="logout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_data = None
                st.success("Logged out successfully!")
                st.switch_page("pages/1_🔐_Login.py")
            st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.error("Unable to fetch user data")

if __name__ == "__main__":
    main()