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
    try:
        hashed = hash_password(password)
        supabase.table("users").insert({"username": username, "password": hashed}).execute()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def authenticate(username: str, password: str) -> bool:
    try:
        hashed = hash_password(password)
        response = supabase.table("users").select("*").eq("username", username).eq("password", hashed).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def reset_user_password(target_username: str, new_password: str) -> bool:
    try:
        hashed = hash_password(new_password)
        supabase.table("users").update({"password": hashed}).eq("username", target_username).execute()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🔐 Supabase Login System")

username = st.text_input("Username", key="main_user")

mode = st.radio("Choose an action:", ["Login", "Sign Up"])

# Admin check
if username == "" and "ADMIN_KEY" in st.secrets:
    admin_pass = st.text_input("Enter admin key", type="password")
    if st.button("Admin Login"):
        if admin_pass == st.secrets["ADMIN_KEY"]:
            st.session_state["admin"] = True
            st.success("✅ Admin access granted!")
        else:
            st.error("❌ Invalid admin key")

if st.session_state.get("admin"):
    st.header("Admin Controls")
    target_user = st.text_input("Username to reset password")
    new_pass = st.text_input("New password", type="password")
    if st.button("Reset Password"):
        hashed = hashlib.sha256(new_pass.encode()).hexdigest()
        supabase.table("users").update({"password": hashed}).eq("username", target_user).execute()
        st.success(f"Password for {target_user} reset!")

if mode == "Sign Up" and not st.session_state.get("admin"):
    new_password = st.text_input("Password", type="password", key="signup_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
    if st.button("Sign Up"):
        if not username or not new_password:
            st.warning("Please enter both username and password.")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            if register_user(username, new_password):
                st.success("✅ Account created! You can now login.")

elif mode == "Login" and not st.session_state.get("admin"):
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("❌ Invalid username or password")
