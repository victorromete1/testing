import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# App base configuration
st.set_page_config(
    page_title="AI Study Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================
# Dummy Session State for GUI Display
# This data is hardcoded to make the GUI render.
# In a real app, this would be managed dynamically.
# ===============================================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True # Default to logged in to show the main app
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "username" not in st.session_state:
    st.session_state.username = "User"
if "notes" not in st.session_state:
    st.session_state.notes = [
        {"title": "Sample Note", "content": "This is a sample note about biology.", "category": "Science", "timestamp": "2025-01-01 10:00:00"}
    ]
if "flashcards" not in st.session_state:
    st.session_state.flashcards = [
        {"front": "What is the powerhouse of the cell?", "back": "The mitochondria.", "category": "Science"}
    ]
if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = [
        {'activity_type': 'quiz', 'timestamp': '2025-09-15T10:00:00', 'score': 85.0, 'subject': 'History', 'correct_answers': 17, 'total_questions': 20, 'difficulty': 'Medium'},
        {'activity_type': 'flashcards', 'timestamp': '2025-09-15T11:00:00', 'flashcards_studied': 20, 'correct_answers': 15, 'subject': 'Science'},
        {'activity_type': 'flashcards_created', 'timestamp': '2025-09-14T09:00:00', 'flashcards_created': 10, 'subject': 'General'}
    ]
if "events" not in st.session_state:
    st.session_state.events = [
        {"name": "Math Exam", "date": datetime.now().date().isoformat(), "color": "#FF0000", "notes": "Chapters 1-4"},
        {"name": "Project Due", "date": (datetime.now().date() + st.delta(days=2)).isoformat(), "color": "#0000FF", "notes": "History presentation"}
    ]
# ===============================================
# End of Dummy Data
# ===============================================

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("🎓 Study Platform")

    # This part shows the login/signup GUI if you set logged_in to False above
    if not st.session_state.get("logged_in", False):
        st.subheader("🔑 Account Access")
        mode = st.radio("Choose mode", ["Login", "Sign Up"], horizontal=True, key="auth_mode")
        if mode == "Sign Up":
            st.text_input("Username", max_chars=15, key="su_user")
            st.text_input("Password", type="password", key="su_pass")
            st.text_input("Confirm Password", type="password", key="su_confirm")
            st.button("Create account", use_container_width=True)
        else:
            st.text_input("Username", key="li_user")
            st.text_input("Password", type="password", key="li_pass")
            st.button("Login", use_container_width=True)

    # This part shows the main sidebar when logged_in is True
    else:
        # This is the ONLY functional part: page navigation
        page = st.selectbox(
            "Navigate:",
            ["🏠 Home", "📝 Notes", "📚 Flashcards", "🧠 Quizzes",
             "📊 Progress", "📅 Calendar", "📝 Autograder", "⚙️ Settings"],
            key="navigation"
        )
        st.session_state.page = page

        st.subheader(f"👋 Welcome, {st.session_state['username']}")
        if st.session_state.get("admin_mode"):
            st.caption("🛠 Admin Mode Enabled")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Save", use_container_width=True) # Non-functional button

        # Quick Stats display
        st.subheader("📈 Quick Stats")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("📝 Notes", len(st.session_state.notes))
            st.metric("🎴 Flashcards", len(st.session_state.flashcards))
        with c2:
            st.metric("🧠 Quizzes", 1) # Dummy value
            st.metric("📚 Sessions", len(st.session_state.study_sessions))

        st.button("Logout", use_container_width=True) # Non-functional button


# ----------------------------
# Home Page
# ----------------------------
if st.session_state.page == "🏠 Home":
    st.markdown("""
    <style>
    .feature-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    .stat-card { background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    .activity-item { background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #6a11cb; }
    .admin-panel { background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

    # Logged-in dashboard view
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 2.5rem;">🎓 SmartStudy Dashboard</h1>
        <h2 style="margin: 0; font-weight: 400;">Welcome back, {st.session_state['username']}! 👋</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.notes)}</h3><p style="margin: 0;">Notes</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.flashcards)}</h3><p style="margin: 0;">Flashcards</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card" style="background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%);"><h3 style="margin: 0; font-size: 2rem;">1</h3><p style="margin: 0;">Quizzes Taken</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card" style="background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%);"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.study_sessions)}</h3><p style="margin: 0;">Study Sessions</p></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### ⚡ Quick Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            st.button("📝 New Note", use_container_width=True)
        with action_col2:
            st.button("📚 Study Flashcards", use_container_width=True)
        with action_col3:
            st.button("🧠 Take Quiz", use_container_width=True)

        st.markdown("### 📅 Recent Activity")
        st.markdown('<div class="activity-item" style="border-left-color: #2ca02c"><div style="display: flex; justify-content: space-between; align-items: center;"><div><b>🧠 Quiz Completed</b> - History</div><div style="color: #2ca02c; font-weight: bold;">85.0%</div></div><div style="color: #666; font-size: 0.9em;">2025-09-15 10:00</div></div>', unsafe_allow_html=True)

        st.markdown("### ✏️ Quick Note")
        with st.form("quick_note_form"):
            st.text_area("Jot something down:", placeholder="Type your quick note here...", height=100, label_visibility="collapsed")
            st.form_submit_button("💾 Save Quick Note", use_container_width=True)

    with col_right:
        st.markdown("### 📅 Upcoming Events")
        st.markdown("<div style='background-color: #f9f9f9; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #FF0000'><div style='font-weight: bold;'>Math Exam</div><div style='color: #666; font-size: 0.9em;'>Today</div></div>", unsafe_allow_html=True)

        st.markdown("### 💡 Study Tip")
        st.info("💡 Try the Pomodoro technique: 25 minutes of focused study, then a 5-minute break.")

# ============================
# Notes Page
# ============================
elif st.session_state.page == "📝 Notes":
    st.title("📝 AI Note Generator & Class Notes")
    st.subheader("💡 Freeform Notes Mode")
    st.text_input("Note Name:", placeholder="Enter a title for your note...")
    st.text_area("Type your notes here:", placeholder="Write your class notes here...", height=200)
    st.text_input("Category for these notes:", value="General")
    st.checkbox("🧠 Summarize with AI", value=True)
    st.button("💾 Save Notes")

    st.markdown("---")
    st.subheader("🚀 Generate AI Notes from Topic or File")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input("📖 Topic or subject:", placeholder="e.g., Photosynthesis, WWII...")
    with col2:
        st.text_input("Category:", value="General")
    st.file_uploader("📂 Upload a file (.txt, .pdf, .docx):", type=['txt', 'pdf', 'docx'])
    st.button("🚀 Generate Notes")

    st.divider()
    st.subheader("📚 Your Notes")
    st.selectbox("Filter by category:", ["All", "Science", "General"])
    with st.expander(f"📄 {st.session_state.notes[0]['title']} ({st.session_state.notes[0]['category']})"):
        st.write(f"**Created:** {st.session_state.notes[0]['timestamp']}")
        st.markdown(st.session_state.notes[0]['content'])
        c1, c2, c3, c4 = st.columns(4)
        c1.button("📚 Create Flashcards", key="f_btn")
        c2.download_button("📥 Download", data="dummy", file_name="note.txt")
        c3.button("🗑️ Delete", key="d_btn")
        c4.text_input("Rename to:", value=st.session_state.notes[0]['title'], key="ren_in")
        c4.button("✏️ Rename", key="r_btn")

# ============================
# Flashcards Page
# ============================
elif st.session_state.page == "📚 Flashcards":
    st.title("📚 Interactive Flashcards")
    tab1, tab2, tab3 = st.tabs(["📖 Study", "➕ Create", "📂 Manage"])

    with tab1:
        st.subheader("📖 Study Session")
        st.selectbox("Study category:", ["All", "Science"])
        st.progress(0.5, text="Card 1 of 2")
        st.markdown('<div style="border: 2px solid #ddd; border-radius: 10px; padding: 30px; margin: 20px 0; background-color: #f9f9f9; text-align: center; min-height: 150px;"><h3>What is the powerhouse of the cell?</h3></div>', unsafe_allow_html=True)
        st.button("🔍 Show Answer", use_container_width=True)

    with tab2:
        st.subheader("➕ Create Flashcards")
        st.radio("Creation method:", ["📝 From Text", "📂 Upload File", "✋ Manual Entry", "📚 From Notes"], horizontal=True)
        st.text_area("Paste content:", placeholder="Enter study material...", height=150)
        c1, c2, c3 = st.columns(3)
        c1.slider("Number of cards:", 3, 20, 8)
        c2.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
        c3.text_input("Category:", value="General")
        st.button("🚀 Generate Flashcards", type="primary")

    with tab3:
        st.subheader("📂 Manage Flashcards")
        st.write(f"**Total flashcards:** {len(st.session_state.flashcards)}")
        st.selectbox("Filter:", ["All", "Science"])
        card = st.session_state.flashcards[0]
        with st.expander(f"🎴 {card['front'][:50]}..."):
            st.write(f"**Front:** {card['front']}")
            st.write(f"**Back:** {card['back']}")
            st.write(f"**Category:** {card['category']}")
            st.button("🗑️ Delete", key="del_card")

# ============================
# Quizzes Page
# ============================
elif st.session_state.page == "🧠 Quizzes":
    st.title("🧠 Interactive Quiz System")
    tab1, tab2 = st.tabs(["📝 Take Quiz", "📊 History"])

    with tab1:
        st.subheader("📝 Create New Quiz")
        c1, c2 = st.columns(2)
        with c1:
            st.radio("Quiz source:", ["📚 My Notes", "📝 New Content", "📂 Upload file"])
            st.selectbox("Question Type:", ["Multiple Choice", "True/False", "Mixed"])
        with c2:
            st.slider("Questions:", 3, 15, 8)
            st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
        st.selectbox("Select note:", [n['title'] for n in st.session_state.notes])
        st.button("🚀 Create & Start Quiz", type="primary", use_container_width=True)

    with tab2:
        st.subheader("📊 Quiz History")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Quizzes", 1)
        c2.metric("Average Score", "85.0%")
        c3.metric("Best Score", "85.0%")
        with st.expander("🟢 2025-09-15 10:00 - 85.0% (17/20)"):
            st.write("**Score:** 85.0%")
            st.button("🔄 Retake This Quiz")

# ============================
# Progress Page
# ============================
elif st.session_state.page == "📊 Progress":
    st.title("📊 Learning Analytics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sessions", 3)
    c2.metric("Quizzes Taken", 1)
    c3.metric("Avg Quiz Score", "85.0%")
    c4.metric("Flashcard Sessions", 2)
    st.subheader("📈 Recent Activity")
    # A placeholder for the chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], [1, 0, 2, 1, 0, 0, 3])
    ax.set_title('Study Sessions (Last 7 Days)')
    ax.set_ylabel('Sessions')
    st.pyplot(fig)


# ============================
# Calendar Page
# ============================
elif st.session_state.page == "📅 Calendar":
    st.title("📅 Calendar & Events")
    st.subheader("➕ Add Event")
    with st.form("add_event_form"):
        st.text_input("Event Title:", placeholder="e.g., Math Test")
        st.date_input("Date:")
        st.text_area("Details (optional):")
        st.color_picker("Pick a color:", "#4CAF50")
        st.form_submit_button("➕ Add")
    st.divider()
    c1, c2, c3 = st.columns([1, 3, 1])
    c1.button("‹")
    c2.markdown(f"<h2 style='text-align:center;margin:0'>September 2025</h2>", unsafe_allow_html=True)
    c3.button("›")
    st.markdown("---")
    st.markdown("*(A calendar grid would be displayed here)*")
    st.divider()
    st.subheader("🗑️ Delete Event")
    st.selectbox("Select an event to delete:", ["2025/09/16 — Math Exam"])
    st.button("❌ Delete Selected Event")

# ============================
# Autograder Page
# ============================
elif st.session_state.page == "📝 Autograder":
    st.title("📝 AI Autograder")
    st.text_area("✍️ Paste your essay, story, or text:", height=250)
    c1, c2 = st.columns(2)
    c1.selectbox("Text type:", ["Essay", "Story", "Article", "Other"])
    c2.text_input("Extra notes (optional)", placeholder="e.g., Focus on creativity...")
    st.button("🚀 Grade Now", type="primary", use_container_width=True)
    
    st.subheader(f"📊 Score: 8/10")
    st.progress(0.8)
    st.markdown("### ✅ Strengths")
    st.markdown("- Good structure and flow.")
    st.markdown("### ⚠️ Weaknesses")
    st.markdown("- Some grammatical errors.")

# ============================
# Settings Page
# ============================
elif st.session_state.page == "⚙️ Settings":
    st.title("⚙️ User Settings")
    st.subheader("🔑 Change Your Password")
    with st.form("change_password_form"):
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm New Password", type="password")
        st.form_submit_button("Change Password")
    st.divider()
    st.subheader("🗑️ Danger Zone")
    with st.expander("Delete Account"):
        st.warning("This action is irreversible.")
        st.text_input("To confirm, please type `DELETE`:")
        st.button("Permanently Delete My Account", type="primary")
