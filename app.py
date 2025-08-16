import streamlit as st
import hashlib
import json
from github import Github

# -----------------------------
# CONFIGURATION
# -----------------------------
GITHUB_TOKEN = "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"  # store token in Streamlit Secrets
REPO_NAME = "victorromete1/testing"           # replace with your GitHub repo
USERS_FILE = "users.json"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def load_users():
    """Load users.json from GitHub"""
    try:
        contents = repo.get_contents(USERS_FILE)
        return json.loads(contents.decoded_content.decode())
    except Exception:
        return {}

def save_users(users):
    """Save users.json to GitHub"""
    contents = repo.get_contents(USERS_FILE)
    repo.update_file(
        USERS_FILE,
        "Update users.json",
        json.dumps(users, indent=2),
        contents.sha
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users = load_users()
    return username in users and users[username]["password"] == hash_password(password)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": hash_password(password)}
    save_users(users)
    return True

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🔐 Persistent Login System")

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
            else:
                st.error("Username already exists.")

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
