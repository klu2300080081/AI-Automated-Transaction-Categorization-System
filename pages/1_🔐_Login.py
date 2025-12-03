import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.user_service import UserService
from styles.app_styles import load_css

st.set_page_config(
    page_title="Login - Transaction Categorization",
    page_icon="🔐",
    layout="centered"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

def main():
    st.markdown('<h1 class="custom-header">🔐 Authentication</h1>', unsafe_allow_html=True)
    
    # Check if already logged in
    if st.session_state.authenticated:
        st.markdown('<div class="success-message">✅ You are already logged in!</div>', unsafe_allow_html=True)
        st.markdown(f"**Welcome back, {st.session_state.user_data['username']}!**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Prediction Page", use_container_width=True):
                st.switch_page("pages/2_🔮_Prediction.py")
        with col2:
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_data = None
                st.rerun()
        return
    
    # Tab selection
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    user_service = UserService()
    
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Login", use_container_width=True)
            
            if submit_login:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    with st.spinner("Authenticating..."):
                        result = user_service.login_user(email, password)
                        
                        if result["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user_data = {
                                "user_id": result["user_id"],
                                "username": result["username"],
                                "email": result["email"],
                                "token": result["token"]
                            }
                            st.success(result["message"])
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(result["message"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### Create New Account")
        
        with st.form("signup_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submit_signup = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit_signup:
                if not username or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    with st.spinner("Creating account..."):
                        result = user_service.register_user(username, email, password)
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.info("Please login with your credentials")
                        else:
                            st.error(result["message"])
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()