import streamlit as st
from .utils import authenticate, create_user
from .memory import load_memory

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#4ade80;'>🏗️ RANDOM V4</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Evolution AI Design Studio</p>", unsafe_allow_html=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("Login")
            with col_reg:
                register_btn = st.form_submit_button("Register")

            if login_btn:
                user = authenticate(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data = user
                    st.session_state.memory = load_memory(username)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            if register_btn:
                if not username or not password:
                    st.error("Please fill all fields.")
                else:
                    try:
                        create_user(username, password)
                        st.success("Account created! You can now log in.")
                    except ValueError as e:
                        st.error(str(e))
