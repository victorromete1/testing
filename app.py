import streamlit as st
import hashlib
from supabase import create_client

# -----------------------------
# CONFIGURATION
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> bool:
    """Insert a new user into Supabase 'users' table"""
    try:
        hashed = hash_password(password)
        response = supabase.table("users").insert({"username": username, "password": hashed}).execute()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def authenticate(username: str, password: str) -> bool:
    """Check username + password"""
    try:
        hashed = hash_password(password)
        response = supabase.table("users").select("*").eq("username", username).eq("password", hashed).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🔐 Supabase Login System")

mode = st.radio("Choose an action:", ["Login", "Sign Up"])

if mode == "Sign Up":
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if not new_user or not new_password:
            st.warning("Please enter both username and password.")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            if register_user(new_user, new_password):
                st.success("✅ Account created! You can now login.")

elif mode == "Login":
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("❌ Invalid username or password")

if st.session_state.get("logged_in"):
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.success("Logged out!")
