import streamlit as st
import hashlib
from supabase import create_client

# -----------------------------
# CONFIGURATION
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
ADMIN_KEY = st.secrets["ADMIN_KEY"]

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
        # Check if user already exists
        existing = supabase.table("users").select("*").eq("username", username).execute()
        if existing.data:
            return False
        supabase.table("users").insert({"username": username, "password": hashed}).execute()
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

def delete_account(username: str):
    """Delete the logged-in user's account"""
    try:
        supabase.table("users").delete().eq("username", username).execute()
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.success("✅ Account deleted!")
    except Exception as e:
        st.error(f"Error: {e}")

def admin_reset_password(target_username: str, new_password: str):
    """Reset any user's password (Admin only)"""
    try:
        hashed = hash_password(new_password)
        supabase.table("users").update({"password": hashed}).eq("username", target_username).execute()
        st.success(f"✅ Password for '{target_username}' has been reset!")
    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🔐 Supabase Login System")

mode = st.radio("Choose an action:", ["Login", "Sign Up"])

# -----------------------------
# SIGN UP
# -----------------------------
if mode == "Sign Up":
    new_user = st.text_input("New Username", key="sign_user")
    new_password = st.text_input("New Password", type="password", key="sign_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="sign_confirm")

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

# -----------------------------
# LOGIN
# -----------------------------
elif mode == "Login":
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        # Admin hidden mode: blank username + admin key
        if username.strip() == "" and password == ADMIN_KEY:
            st.session_state["admin_mode"] = True
            st.success("✅ Admin mode activated!")
        elif authenticate(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("❌ Invalid username or password")

# -----------------------------
# LOGGED IN USER CONTROLS
# -----------------------------
if st.session_state.get("logged_in"):
    st.write(f"Logged in as: **{st.session_state['username']}**")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.success("Logged out!")

    if st.button("Delete Account"):
        delete_account(st.session_state["username"])

# -----------------------------
# ADMIN MODE CONTROLS
# -----------------------------
if st.session_state.get("admin_mode"):
    st.subheader("🛠 Admin Controls (Hidden Mode)")

    target_user = st.text_input("Target Username to Reset Password")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Reset User Password"):
        if target_user and new_pass:
            admin_reset_password(target_user, new_pass)
        else:
            st.warning("Enter both username and new password.")

    if st.button("Exit Admin Mode"):
        st.session_state["admin_mode"] = False
        st.success("Exited admin mode.")
