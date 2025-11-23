# ui.py
import streamlit as st
import datetime

def display_daily_inspiration(inspiration_choice, inspiration, inspiration_full):
    if inspiration_choice == "Theme of the Day":
        st.sidebar.write("📝 Theme of the Day:")
        st.sidebar.success(inspiration)
    else:
        word, meaning = inspiration_full.split("—", 1)
        st.sidebar.write("📚 Word of the Day:")
        st.sidebar.success(word.strip())
        st.sidebar.caption("Meaning: " + meaning.strip())

def write_today_ui(username, inspiration, inspiration_full, save_callback):
    st.header("✏️ Today's Creative Writing (Public)")
    st.write("Today's Inspiration:", f"**{inspiration}**")
    writing_type = st.selectbox("Writing Type", ["Poem", "Short Story", "Sonnet", "Essay", "Free Write"])
    writing = st.text_area("Start writing here...")
    if st.button("Save Public Writing"):
        save_callback(writing_type, writing)

def daily_feed_ui(today_public):
    st.header("📖 Today's Public Submissions")
    if not today_public:
        st.info("No public submissions yet today.")
    else:
        for e in today_public:
            name = "Anonymous" if e.get("anonymous", "").lower() == "true" else e.get("username", "")
            st.subheader(f"{name} — {e.get('type', '')}")
            st.caption(f"{e.get('inspiration_type')}: {e.get('inspiration')}")
            if e.get("inspiration_type") == "Word of the Day" and "—" in e.get("inspiration_full", ""):
                _, meaning_part = e["inspiration_full"].split("—", 1)
                st.caption("Meaning: " + meaning_part.strip())
            st.write(e.get("writing", ""))
            st.markdown("---")

def personal_journal_ui(user, journal_entries, save_journal_entry_file):
    st.subheader("➕ Add a new journal entry")
    mood = st.selectbox("Mood Emoji", ["🙂", "😢", "😡", "🤩", "😐", "🤔", "😭", "🥳", "😌"])
    journal_text = st.text_area("Journal writing...")

    if st.button("Save Journal Entry"):
        if journal_text.strip() == "":
            st.warning("Please write something before saving.")
        else:
            save_journal_entry_file(journal_text)
            st.success("Journal entry saved!")

    st.markdown("---")
    st.subheader("🗂 Your previous entries")

    user_entries = [e for e in journal_entries if e.get("username") == user]

    if not user_entries:
        st.info("No journal entries yet.")
    else:
        for e in user_entries:
            st.write(f"📅 {e.get('date')} | Mood: {e.get('mood')}")
            st.write(e.get("writing", ""))
            st.markdown("---")

