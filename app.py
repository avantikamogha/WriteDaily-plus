import streamlit as st
import csv
import datetime
import os
import random

# ---------------- Paths ----------------
PUBLIC_FILE = "data/public_entries.csv"
JOURNAL_FILE = "data/journal_entries.csv"
QUOTES_FILE = "assets/quotes.txt"
THEMES_FILE = "assets/themes.txt"
WORDS_FILE = "assets/words.csv"

# ---------------- Setup ----------------
os.makedirs("data", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# Create public CSV if missing
if not os.path.exists(PUBLIC_FILE):
    with open(PUBLIC_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "username", "anonymous", "inspiration_type",
                         "inspiration", "inspiration_full", "type", "writing"])

# Create journal CSV if missing
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "username", "mood", "writing"])

# ---------------- Asset loaders ----------------
def load_quotes(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return ["Keep writing — your voice matters."]

def load_themes(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return ["Reflection"]

def load_words(path):
    words = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                w = row.get("word", "").strip()
                m = row.get("meaning", "").strip()
                if w:
                    words.append({"word": w, "meaning": m})
    if not words:
        words = [{"word": "Gratitude", "meaning": "Being thankful"}]
    return words

QUOTES = load_quotes(QUOTES_FILE)
THEMES = load_themes(THEMES_FILE)
WORDS = load_words(WORDS_FILE)

# ---------------- Helpers ----------------
def save_public_entry(date, user, anon, insp_type, insp, insp_full, wtype, text):
    with open(PUBLIC_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, user, anon, insp_type, insp, insp_full, wtype, text])

def load_public_entries():
    try:
        with open(PUBLIC_FILE, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except:
        return []

def save_journal_entry(date, user, mood, text):
    with open(JOURNAL_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, user, mood, text])

def load_journal_entries():
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except:
        return []

# ---------------- Sidebar / Daily settings ----------------
st.title("✍️ WriteDaily+")
today = str(datetime.date.today())
st.sidebar.write("📅 Today:", today)

# Reset session state daily
if "stored_date" not in st.session_state or st.session_state.stored_date != today:
    st.session_state.clear()
    st.session_state.stored_date = today

# Persist daily quote
if "daily_quote" not in st.session_state:
    st.session_state.daily_quote = random.choice(QUOTES)

st.sidebar.write("💡 Daily Quote:")
st.sidebar.info(st.session_state.daily_quote)

# Inspiration selection
inspiration_choice = st.sidebar.radio("Choose today's inspiration:", ["Theme of the Day", "Word of the Day"])

# Persist inspiration
if "last_inspiration_choice" not in st.session_state or st.session_state.last_inspiration_choice != inspiration_choice:
    if inspiration_choice == "Theme of the Day":
        chosen = random.choice(THEMES)
        st.session_state.inspiration = chosen
        st.session_state.inspiration_full = chosen
    else:  # Word of the Day
        selected = random.choice(WORDS)
        st.session_state.inspiration = selected["word"]
        st.session_state.inspiration_full = f"{selected['word']} — {selected.get('meaning', '')}"

    st.session_state.last_inspiration_choice = inspiration_choice

inspiration = st.session_state.inspiration
inspiration_full = st.session_state.inspiration_full

if inspiration_choice == "Theme of the Day":
    st.sidebar.write("📝 Theme of the Day:")
    st.sidebar.success(inspiration)
else:
    word, meaning = inspiration_full.split("—", 1)
    st.sidebar.write("📚 Word of the Day:")
    st.sidebar.success(word.strip())
    st.sidebar.caption("Meaning: " + meaning.strip())

# ---------------- Load entries into session ----------------
if "public_entries" not in st.session_state:
    st.session_state.public_entries = load_public_entries()

journal_entries = load_journal_entries()

# ---------------- Journal streak (fixed) ----------------
written_dates = sorted(
    set(e["date"] for e in journal_entries if "date" in e and e["date"].strip())
)
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

# Menu
menu = ["Write Today", "Daily Writings Feed", "Personal Journal"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Write Today ----------------
if choice == "Write Today":
    st.header("✏️ Today's Creative Writing (Public)")
    st.write("Today's Inspiration:", f"**{inspiration}**")

    username = st.text_input("Your name")
    anonymous = st.checkbox("Post anonymously")
    writing_type = st.selectbox("Writing Type", ["Poem", "Short Story", "Sonnet", "Essay", "Free Write"])
    writing = st.text_area("Start writing here...")

    if st.button("Save Public Writing"):
        if writing.strip() == "":
            st.warning("Please write something before saving.")
        else:
            save_public_entry(today, username, str(anonymous), inspiration_choice,
                              inspiration, inspiration_full, writing_type, writing)
            st.session_state.public_entries = load_public_entries()  # refresh feed
            st.success("Public creative writing saved!")

# ---------------- Daily Writings Feed ----------------
elif choice == "Daily Writings Feed":
    st.header("📖 Today's Public Submissions")
    today_public = [e for e in st.session_state.public_entries if e.get("date") == today]

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

# ---------------- Personal Journal ----------------
elif choice == "Personal Journal":
    st.header("🔐 Personal Journal (Private)")
    st.info("Private space — visible only to you.")

    user = st.text_input("Enter your name to open your journal")

    if user:
        st.subheader("➕ Add a new journal entry")
        mood = st.selectbox("Mood Emoji", ["🙂", "😢", "😡", "🤩", "😐", "🤔", "😭", "🥳", "😌"])
        journal_text = st.text_area("Journal writing...")

        if st.button("Save Journal Entry"):
            if journal_text.strip() == "":
                st.warning("Please write something before saving.")
            else:
                save_journal_entry(today, user, mood, journal_text)
                journal_entries = load_journal_entries()
                st.success("Journal entry saved!")

        st.markdown("---")
        st.subheader("🗂 Your previous entries")

        user_entries = [e for e in journal_entries if e.get("username") == user]

        if not user_entries:
            st.info("No journal entries yet.")
        else:
            for i, e in enumerate(user_entries):
                st.write(f"📅 {e.get('date')}")
                moods = ["🙂", "😢", "😡", "🤩", "😐", "🤔", "😭", "🥳", "😌"]
                new_mood = st.selectbox("Mood", moods, index=moods.index(e.get("mood")) if e.get("mood") in moods else 0, key=f"m{i}")
                new_text = st.text_area("Edit entry:", value=e.get("writing", ""), key=f"t{i}")

                if st.button(f"Save Edit #{i}"):
                    e["mood"] = new_mood
                    e["writing"] = new_text
                    with open(JOURNAL_FILE, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(["date", "username", "mood", "writing"])
                        for x in journal_entries:
                            writer.writerow([x.get("date"), x.get("username"), x.get("mood"), x.get("writing")])
                    st.success("Journal entry updated!")
                st.markdown("---")
