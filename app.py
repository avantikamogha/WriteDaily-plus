# app.py
import streamlit as st
import os
import datetime
import random
from config import *
from helpers import *
from ui import *

# ---------------- Setup ----------------
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

if not os.path.exists(PUBLIC_FILE):
    with open(PUBLIC_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "username", "anonymous", "inspiration_type",
                         "inspiration", "inspiration_full", "type", "writing"])

if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "username", "mood", "writing"])

# ---------------- Load assets ----------------
QUOTES = load_quotes(QUOTES_FILE)
THEMES = load_themes(THEMES_FILE)
WORDS = load_words(WORDS_FILE)

# ---------------- Sidebar / Session ----------------
st.title("✍️ WriteDaily+")
today = str(datetime.date.today())
st.sidebar.write("📅 Today:", today)

if "stored_date" not in st.session_state or st.session_state.stored_date != today:
    st.session_state.clear()
    st.session_state.stored_date = today

if "daily_quote" not in st.session_state:
    st.session_state.daily_quote = random.choice(QUOTES)

st.sidebar.write("💡 Daily Quote:")
st.sidebar.info(st.session_state.daily_quote)

inspiration_choice = st.sidebar.radio("Choose today's inspiration:", ["Theme of the Day", "Word of the Day"])

if "last_inspiration_choice" not in st.session_state or st.session_state.last_inspiration_choice != inspiration_choice:
    if inspiration_choice == "Theme of the Day":
        chosen = random.choice(THEMES)
        st.session_state.inspiration = chosen
        st.session_state.inspiration_full = chosen
    else:
        selected = random.choice(WORDS)
        st.session_state.inspiration = selected["word"]
        st.session_state.inspiration_full = f"{selected['word']} — {selected.get('meaning', '')}"
    st.session_state.last_inspiration_choice = inspiration_choice

display_daily_inspiration(inspiration_choice, st.session_state.inspiration, st.session_state.inspiration_full)

# ---------------- Load entries ----------------
if "public_entries" not in st.session_state:
    st.session_state.public_entries = load_public_entries(PUBLIC_FILE)
journal_entries = load_journal_entries(JOURNAL_FILE)

# ---------------- Journal streak ----------------
written_dates = sorted(set(e["date"] for e in journal_entries if "date" in e and e["date"].strip()))
streak = 0
for i in range(len(written_dates)):
    try:
        d = datetime.date.fromisoformat(written_dates[-1 - i])
    except:
        continue
    if d == datetime.date.today() - datetime.timedelta(days=i):
        streak += 1
    else:
        break
st.sidebar.write("🔥 Journal Streak:", streak, "days")

# ---------------- Menu ----------------
menu = ["Write Today", "Daily Writings Feed", "Personal Journal"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Write Today":
    def save_callback(wtype, text):
        if text.strip() == "":
            st.warning("Please write something before saving.")
        else:
            save_public_entry(PUBLIC_FILE, today, "", "Anonymous", inspiration_choice,
                              st.session_state.inspiration, st.session_state.inspiration_full, wtype, text)
            st.session_state.public_entries = load_public_entries(PUBLIC_FILE)
            st.success("Public creative writing saved!")

    write_today_ui("", st.session_state.inspiration, st.session_state.inspiration_full, save_callback)

elif choice == "Daily Writings Feed":
    today_public = [e for e in st.session_state.public_entries if e.get("date") == today]
    daily_feed_ui(today_public)

elif choice == "Personal Journal":
    user = st.text_input("Enter your name to open your journal")
    if user:
        def save_journal_entry_file(text):
            save_journal_entry(JOURNAL_FILE, today, user, "🙂", text)
        personal_journal_ui(user, journal_entries, save_journal_entry_file)
