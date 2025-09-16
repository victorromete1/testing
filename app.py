import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# App base configuration
st.set_page_config(
    page_title="Intelligent Learning Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================
# Dummy Session State for GUI Display
# This data is hardcoded to make the GUI render.
# ===============================================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "username" not in st.session_state:
    st.session_state.username = "Learner"
if "notes" not in st.session_state:
    st.session_state.notes = [
        {"title": "Biology Summary", "content": "A summary of key concepts in biology.", "category": "Science", "timestamp": "2025-02-10 11:30:00"}
    ]
if "flashcards" not in st.session_state:
    st.session_state.flashcards = [
        {"front": "What is the primary function of chloroplasts?", "back": "To conduct photosynthesis.", "category": "Science"}
    ]
if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = [
        {'activity_type': 'quiz', 'timestamp': '2025-09-15T10:00:00', 'score': 90.0, 'subject': 'Physics', 'correct_answers': 18, 'total_questions': 20, 'difficulty': 'Hard'},
        {'activity_type': 'flashcards', 'timestamp': '2025-09-15T11:00:00', 'flashcards_studied': 25, 'correct_answers': 22, 'subject': 'Science'},
        {'activity_type': 'flashcards_created', 'timestamp': '2025-09-14T09:00:00', 'flashcards_created': 15, 'subject': 'General'}
    ]
if "events" not in st.session_state:
    st.session_state.events = [
        {"name": "Physics Midterm", "date": datetime.now().date().isoformat(), "color": "#ff4b4b", "notes": "Review chapters 5-8"},
        {"name": "Essay Draft Due", "date": "2025-09-19", "color": "#1f77b4", "notes": "Literature paper"}
    ]
# ===============================================
# End of Dummy Data
# ===============================================

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("🧠 Learning Hub")

    if not st.session_state.get("logged_in", False):
        st.subheader("🚀 Get Started")
        action = st.radio("Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        if action == "Sign Up":
            st.text_input("Choose Username", max_chars=15)
            st.text_input("Create Password", type="password")
            st.text_input("Confirm Password", type="password")
            st.button("Sign Up Now", use_container_width=True)
        else:
            st.text_input("Username")
            st.text_input("Password", type="password")
            st.button("Log In", use_container_width=True)

    else:
        # This is the ONLY functional part: page navigation
        page = st.selectbox(
            "Go to:",
            ["🏠 Dashboard", "✍️ My Notebook", "📚 Flashcard Deck", "❓ Quiz Center",
             "📈 Performance", "🗓️ Schedule", "🤖 AI Assistant", "⚙️ Settings"],
        )
        st.session_state.page = page

        st.subheader(f"Hello, {st.session_state['username']}")
        if st.session_state.get("admin_mode"):
            st.caption("Admin Mode")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Sync Data", use_container_width=True)

        st.subheader("📊 Your Stats")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("✍️ Notes", len(st.session_state.notes))
            st.metric("📚 Cards", len(st.session_state.flashcards))
        with c2:
            st.metric("❓ Quizzes", 1)
            st.metric("🗓️ Sessions", len(st.session_state.study_sessions))

        st.button("Logout", use_container_width=True, type="secondary")


# ----------------------------
# Home Page (Dashboard)
# ----------------------------
if st.session_state.page == "🏠 Dashboard":
    st.markdown("""
    <style>
    .stat-card { background: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%); color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    .activity-item { background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #8f94fb; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1d2b64 0%, #f8cdda 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 2.5rem;">🧠 Learning Dashboard</h1>
        <h2 style="margin: 0; font-weight: 400;">Good to see you again, {st.session_state['username']}!</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.notes)}</h3><p style="margin: 0;">Notes</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card" style="background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.flashcards)}</h3><p style="margin: 0;">Flashcards</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card" style="background: linear-gradient(135deg, #f7b733 0%, #fc4a1a 100%);"><h3 style="margin: 0; font-size: 2rem;">1</h3><p style="margin: 0;">Quizzes Taken</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card" style="background: linear-gradient(135deg, #159957 0%, #155799 100%);"><h3 style="margin: 0; font-size: 2rem;">{len(st.session_state.study_sessions)}</h3><p style="margin: 0;">Study Sessions</p></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### ⚡ Quick Links")
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            st.button("✍️ New Note", use_container_width=True)
        with action_col2:
            st.button("📚 Review Cards", use_container_width=True)
        with action_col3:
            st.button("❓ Start Quiz", use_container_width=True)

        st.markdown("### 📊 Latest Sessions")
        st.markdown('<div class="activity-item" style="border-left-color: #159957"><div style="display: flex; justify-content: space-between; align-items: center;"><div><b>❓ Quiz Completed</b> - Physics</div><div style="color: #159957; font-weight: bold;">90.0%</div></div><div style="color: #666; font-size: 0.9em;">2025-09-15 10:00</div></div>', unsafe_allow_html=True)

        st.markdown("### 📝 Quick Memo")
        with st.form("quick_memo_form"):
            st.text_area("Jot something down:", placeholder="Type a quick memo here...", height=100, label_visibility="collapsed")
            st.form_submit_button("💾 Save Memo", use_container_width=True)

    with col_right:
        st.markdown("### 🗓️ Upcoming Deadlines")
        st.markdown("<div style='background-color: #f9f9f9; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #ff4b4b'><div style='font-weight: bold;'>Physics Midterm</div><div style='color: #666; font-size: 0.9em;'>Today</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: #f9f9f9; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #1f77b4'><div style='font-weight: bold;'>Essay Draft Due</div><div style='color: #666; font-size: 0.9em;'>In 3 days</div></div>", unsafe_allow_html=True)

        st.markdown("### ✨ Pro Tip")
        st.info("💡 To better remember a concept, try explaining it to a friend in simple terms.")

# ----------------------------
# Notes Page (My Notebook)
# ----------------------------
elif st.session_state.page == "✍️ My Notebook":
    st.title("✍️ My Notebook")
    st.subheader("📘 Manual Note Entry")
    st.text_input("Note Title:", placeholder="Title for your note...")
    st.text_area("Content:", placeholder="Start writing your notes here...", height=200)
    st.text_input("Assign Category:", value="General")
    st.checkbox("🤖 Summarize with AI", value=True)
    st.button("💾 Commit Note")

    st.markdown("---")
    st.subheader("🤖 AI Note Assistant")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input("✨ Topic:", placeholder="e.g., The Roman Empire, Quantum Physics...")
    with col2:
        st.text_input("Category:", value="AI-Generated")
    st.file_uploader("📂 Or upload a document (.txt, .pdf):", type=['txt', 'pdf'])
    st.button("🚀 Create with AI")

    st.divider()
    st.subheader("🗂️ Saved Notes")
    st.selectbox("Filter by Category:", ["All", "Science", "General", "AI-Generated"])
    note = st.session_state.notes[0]
    with st.expander(f"📄 {note['title']} ({note['category']})"):
        st.caption(f"Created: {note['timestamp']}")
        st.markdown(note['content'])
        c1, c2, c3 = st.columns(3)
        c1.button("📚 Create Flashcards", key="f_btn")
        c2.download_button("📥 Export Note", data="dummy", file_name="note.txt")
        c3.button("🗑️ Delete Note", key="d_btn", type="secondary")

# ----------------------------
# Flashcards Page (Flashcard Deck)
# ----------------------------
elif st.session_state.page == "📚 Flashcard Deck":
    st.title("📚 Flashcard Deck")
    tab1, tab2, tab3 = st.tabs(["🧐 Review", "➕ New Cards", "🗂️ Organize"])

    with tab1:
        st.subheader("🧐 Review Session")
        st.selectbox("Select Deck to Review:", ["All", "Science"])
        st.progress(0.5, text="Card 1 of 2")
        st.markdown('<div style="border: 2px solid #ddd; border-radius: 10px; padding: 30px; margin: 20px 0; background-color: #f9f9f9; text-align: center; min-height: 150px;"><h3>What is the primary function of chloroplasts?</h3></div>', unsafe_allow_html=True)
        st.button("Show Answer", use_container_width=True)

    with tab2:
        st.subheader("➕ Create New Cards")
        st.radio("How to create?", ["From Text", "From File", "Manually", "From Note"], horizontal=True)
        st.text_area("Paste text here:", placeholder="Paste study material...", height=150)
        c1, c2, c3 = st.columns(3)
        c1.number_input("Number of cards:", 3, 20, 10)
        c2.select_slider("Difficulty:", ["Simple", "Medium", "Complex"])
        c3.text_input("Deck Name:", value="General")
        st.button("🤖 Generate Cards with AI", type="primary")

    with tab3:
        st.subheader("🗂️ Organize Your Deck")
        st.write(f"**Total cards in collection:** {len(st.session_state.flashcards)}")
        st.selectbox("Filter by Deck:", ["All", "Science"])
        card = st.session_state.flashcards[0]
        with st.expander(f"🃏 {card['front'][:50]}..."):
            st.markdown(f"**Question:** {card['front']}")
            st.markdown(f"**Answer:** {card['back']}")
            st.caption(f"Deck: {card['category']}")
            st.button("Delete Card", key="del_card", type="secondary")

# ----------------------------
# Quizzes Page (Quiz Center)
# ----------------------------
elif st.session_state.page == "❓ Quiz Center":
    st.title("❓ Quiz Center")
    tab1, tab2 = st.tabs(["🚀 Start New Quiz", "📜 Past Results"])

    with tab1:
        st.subheader("⚙️ Configure Your Quiz")
        c1, c2 = st.columns(2)
        with c1:
            st.radio("Quiz based on:", ["My Notes", "Pasted Text", "Uploaded File"])
            st.selectbox("Question Format:", ["Multiple Choice", "True/False", "Mix"])
        with c2:
            st.slider("Number of Questions:", 5, 20, 10)
            st.select_slider("Quiz Difficulty:", ["Easy", "Medium", "Hard"])
        st.selectbox("Select from My Notes:", [n['title'] for n in st.session_state.notes])
        st.button("Begin Quiz", type="primary", use_container_width=True)

    with tab2:
        st.subheader("📜 Past Results")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Quizzes", 1)
        c2.metric("Average Score", "90.0%")
        c3.metric("Top Score", "90.0%")
        with st.expander("✅ 2025-09-15 10:00 - 90.0% (18/20)"):
            st.write("**Subject:** Physics")
            st.button("🔄 Try Again")

# ----------------------------
# Progress Page (Performance)
# ----------------------------
elif st.session_state.page == "📈 Performance":
    st.title("📈 Your Performance")
    st.subheader("📊 Performance Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sessions", 3)
    c2.metric("Quizzes Taken", 1)
    c3.metric("Avg. Score", "90.0%")
    c4.metric("Cards Reviewed", 25)
    st.subheader("🗓️ Activity This Week")
    # A placeholder for a line chart
    fig, ax = plt.subplots(figsize=(10, 4))
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    activity = np.random.randint(0, 5, size=7)
    ax.plot(days, activity, marker='o', linestyle='-', color='b')
    ax.set_title('Study Sessions This Week')
    ax.set_ylabel('Number of Sessions')
    ax.grid(True)
    st.pyplot(fig)

# ----------------------------
# Calendar Page (Schedule)
# ----------------------------
elif st.session_state.page == "🗓️ Schedule":
    st.title("🗓️ Study Schedule")
    st.subheader("➕ New Schedule Item")
    with st.form("add_item_form"):
        st.text_input("Item Name:", placeholder="e.g., Physics Midterm")
        st.date_input("Date:")
        st.text_area("Description (optional):")
        st.color_picker("Choose a color:", "#1f77b4")
        st.form_submit_button("Add to Schedule")
    st.divider()
    c1, c2, c3 = st.columns([1, 3, 1])
    c1.button("◀️")
    c2.markdown(f"<h2 style='text-align:center;margin:0'>September 2025</h2>", unsafe_allow_html=True)
    c3.button("▶️")
    st.markdown("---")
    st.markdown("*(A calendar grid would be displayed here)*")
    st.divider()
    st.subheader("🗑️ Remove Item")
    st.selectbox("Select item to remove:", ["2025/09/16 — Physics Midterm"])
    st.button("❌ Remove Selected Item")

# ----------------------------
# Autograder Page (AI Assistant)
# ----------------------------
elif st.session_state.page == "🤖 AI Assistant":
    st.title("🤖 AI Writing Assistant")
    st.text_area("Enter your text for feedback:", height=250, placeholder="Paste your essay, report, or creative writing here...")
    c1, c2 = st.columns(2)
    c1.selectbox("What type of text is this?", ["Essay", "Story", "Report", "Email"])
    c2.text_input("Any specific instructions?", placeholder="e.g., Check for clarity...")
    st.button("🚀 Analyze Text", type="primary", use_container_width=True)

    st.subheader(f"📊 Overall Score: 8.5/10")
    st.progress(0.85)
    st.markdown("<h5>✅ What's Good:</h5>", unsafe_allow_html=True)
    st.markdown("- Strong thesis statement and clear arguments.")
    st.markdown("<h5>⚠️ Areas for Improvement:</h5>", unsafe_allow_html=True)
    st.markdown("- Could use more varied sentence structure.")

# ----------------------------
# Settings Page (Account Management)
# ----------------------------
elif st.session_state.page == "⚙️ Settings":
    st.title("⚙️ Account Management")
    st.subheader("🔒 Update Password")
    with st.form("update_password_form"):
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm New Password", type="password")
        st.form_submit_button("Update Password")
    st.divider()
    st.subheader("🛑 Account Deletion")
    with st.expander("Delete Your Account"):
        st.error("Warning: This action cannot be undone. All data will be lost.")
        st.text_input("To confirm, type `DELETE MY ACCOUNT`:")
        st.button("I understand, delete my account", type="primary")
