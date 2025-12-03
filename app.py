import config
import streamlit as st
from styles.app_styles import load_css

st.set_page_config(
    page_title="Transaction Categorization System",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="custom-header">🔮 Transaction Categorization System</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to the Autonomous Transaction Categorization System
    
    This intelligent system automatically categorizes your transactions using 
    advanced machine learning algorithms and natural language processing.
    
    ### 🚀 Getting Started
    
    1. **Login or Sign Up** - Create an account or login to your existing account
    2. **Make Predictions** - Enter transaction details to get instant categorization
    3. **View History** - Track all your transaction predictions
    4. **Manage Profile** - View your account information and statistics
    
    ### ✨ Key Features
    
    - 🤖 **AI-Powered Classification**: Advanced ML models for accurate predictions
    - ⚡ **Real-time Processing**: Get instant results with confidence scores
    - 📊 **Comprehensive Analytics**: Track your transaction patterns
    - 🔒 **Secure & Private**: Enterprise-grade security with encrypted data
    - 🌙 **Modern Dark Theme**: Eye-friendly interface for extended use
    
    ### 📱 Navigation
    
    Use the sidebar to navigate between different sections:
    - 🔐 **Login**: Authentication page
    - 🔮 **Prediction**: Make new transaction predictions
    - 📜 **History**: View past predictions
    - ℹ️ **About**: User profile and app information
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown('<h2 class="custom-subheader">⚡ Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### 🔐")
        st.markdown("**Login**")
        if st.button("Sign In", key="login_home", use_container_width=True):
            st.switch_page("pages/1_🔐_Login.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### 🔮")
        st.markdown("**Predict**")
        if st.button("Start Predicting", key="predict_home", use_container_width=True):
            st.switch_page("pages/2_🔮_Prediction.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### 📜")
        st.markdown("**History**")
        if st.button("View Records", key="history_home", use_container_width=True):
            st.switch_page("pages/3_📜_History.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### ℹ️")
        st.markdown("**Profile**")
        if st.button("User Info", key="about_home", use_container_width=True):
            st.switch_page("pages/4_ℹ️_About.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # System information
    st.markdown('<h2 class="custom-subheader">🛠️ System Information</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Supported Categories
        - Food & Beverage
        - Groceries
        - Shopping
        - Fuel
        - Transport & Travel
        - Bills & Utilities
        """)
    
    with col2:
        st.markdown("""
        ### 🏆 More Categories
        - Entertainment
        - Health & Medical
        - Personal Care
        - Education
        - Financial Services
        - Others / Unknown
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: var(--text-secondary);">'
        '💡 Built with Streamlit • 🔒 Secured with JWT • 🗄️ Powered by MongoDB'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()