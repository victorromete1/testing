import streamlit as st
import json
import hashlib
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
USERS_FILE = "users.json"  # path to your JSON file

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def load_users():
    """Load user data from JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user data to JSON"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Return a hashed version of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Check if username and password match"""
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

def register_user(username, password):
    """Add a new user"""
    users = load_users()
    if username in users:
        return False  # user already exists
    users[username] = {"password": hash_password(password)}
    save_users(users)
    return True

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.title("🔐 Simple User Login System")

# Choose login or signup
mode = st.radio("Choose an action:", ["Login", "Sign Up"])

if mode == "Sign Up":
    st.subheader("Create a new account")
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
            else:
                st.error("Username already exists.")

elif mode == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("❌ Invalid username or password")

# Optional: show logout button if logged in
if st.session_state.get("logged_in"):
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.success("Logged out!")
