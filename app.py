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


# ---------------- Load assets ----------------
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
                # Expect columns: word, meaning
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
    entries = []
    with open(PUBLIC_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def load_journal_entries():
    entries = []
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def save_journal_entry(date, user, mood, text):
    with open(JOURNAL_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, user, mood, text])


# ---------------- App UI ----------------
st.title("✍️ WriteDaily+")
st.sidebar.write("📅 Today:", str(datetime.date.today()))

# daily quote
daily_quote = random.choice(QUOTES)
st.sidebar.write("💡 Daily Quote:")
st.sidebar.info(daily_quote)

# user chooses inspiration type in sidebar
inspiration_choice = st.sidebar.radio("Choose today's inspiration:", ["Theme of the Day", "Word of the Day"])

# choose the actual inspiration based on choice
if inspiration_choice == "Theme of the Day":
    if THEMES:
        inspiration = random.choice(THEMES)
    else:
        inspiration = "Reflection"
    inspiration_full = inspiration  # for storage: same as theme text
    st.sidebar.write("📝 Theme of the Day:")
    st.sidebar.success(inspiration)

else:  # Word of the Day
    selected = random.choice(WORDS)
    inspiration = selected["word"]
    meaning = selected.get("meaning", "")
    inspiration_full = f"{inspiration} — {meaning}"  # store word + meaning as requested
    st.sidebar.write("📚 Word of the Day:")
    st.sidebar.success(inspiration)
    st.sidebar.caption(f"Meaning: {meaning}")

# load saved entries
public_entries = load_public_entries()
journal_entries = load_journal_entries()

# Streak calculation based on journal entries (no change to journal behaviour)
written_dates = sorted(list(set([e["date"] for e in journal_entries]))) if journal_entries else []
streak = 0
for i in range(len(written_dates)):
    try:
        d = datetime.date.fromisoformat(written_dates[-1 - i])
    except Exception:
        continue
    if d == datetime.date.today() - datetime.timedelta(days=i):
        streak += 1
    else:
        break
st.sidebar.write("🔥 Journal Streak:", streak, "days")

# Main menu
menu = ["Write Today", "Daily Writings Feed", "Personal Journal"]
choice = st.sidebar.selectbox("Menu", menu)

today = str(datetime.date.today())

# ---------------- Write Today (public) ----------------
if choice == "Write Today":
    st.header("✏️ Today's Creative Writing (Public)")

    st.write("Today's Inspiration:", f"**{inspiration}**")
    if inspiration_choice == "Word of the Day":
        st.info("Meaning: " + (meaning if meaning else "No meaning available"))

    username = st.text_input("Your name")
    anonymous = st.checkbox("Post anonymously")
    writing_type = st.selectbox("Writing Type", ["Poem", "Short Story", "Sonnet", "Essay", "Free Write"])
    writing = st.text_area("Start writing here...")

    if st.button("Save Public Writing"):
        if writing.strip() == "":
            st.warning("Please write something before saving.")
        else:
            # store inspiration_type, inspiration (word or theme), and inspiration_full (word + meaning if word)
            save_public_entry(today, username, str(anonymous), inspiration_choice, inspiration, inspiration_full, writing_type, writing)
            st.success("Public creative writing saved!")

# ---------------- Daily Writings Feed (public) ----------------
elif choice == "Daily Writings Feed":
    st.header("📖 Today's Public Submissions")
    today_public = [e for e in public_entries if e["date"] == today]

    if not today_public:
        st.info("No public submissions yet today.")
    else:
        for e in today_public:
            name = "Anonymous" if e.get("anonymous", "").lower() == "true" else e.get("username", "")
            insp_type = e.get("inspiration_type", "")
            insp = e.get("inspiration", "")
            insp_full = e.get("inspiration_full", "")
            st.subheader(f"{name} — {e.get('type', '')}")
            st.caption(f"{insp_type}: {insp}")
            # if it's a word and meaning was stored, show meaning under caption for readers
            if insp_type == "Word of the Day" and insp_full and "—" in insp_full:
                _, meaning_part = insp_full.split("—", 1)
                st.caption("Meaning:" + meaning_part.strip())
            st.write(e.get("writing", ""))
            st.markdown("---")

# ---------------- Personal Journal (private) ----------------
elif choice == "Personal Journal":
    st.header("🔐 Personal Journal (Private)")
    st.info("Journal mode is private — mood selector and edits only here. No change from previous behaviour.")

    user = st.text_input("Enter your name to open your journal")

    if user:
        # add a new entry
        st.subheader("➕ Add a new journal entry")
        mood = st.selectbox("Mood Emoji", ["🙂", "😢", "😡", "🤩", "😐", "🤔", "😭", "🥳", "😌"], key="new_mood")
        journal_text = st.text_area("Journal writing...")

        if st.button("Save Journal Entry"):
            if journal_text.strip() == "":
                st.warning("Please write something before saving.")
            else:
                save_journal_entry(today, user, mood, journal_text)
                st.success("Journal entry saved!")

        st.markdown("---")

        # show previous entries for this user and allow edits (simple rewrite)
        user_entries = [e for e in journal_entries if e.get("username", "") == user]
        st.subheader("🗂 Your previous entries")
        if not user_entries:
            st.info("No journal entries yet.")
        else:
            # display editable fields and allow save which rewrites the entire journal CSV
            for i, e in enumerate(user_entries):
                st.write(f"📅 {e.get('date', '')}")
                mood_index = 0
                moods = ["🙂", "😢", "😡", "🤩", "😐", "🤔", "😭", "🥳", "😌"]
                try:
                    mood_index = moods.index(e.get("mood", moods[0]))
                except ValueError:
                    mood_index = 0
                new_mood = st.selectbox("Mood", moods, index=mood_index, key=f"m{i}")
                new_text = st.text_area("Edit entry:", value=e.get("writing", ""), key=f"t{i}")

                if st.button(f"Save Edit #{i}"):
                    # update in-memory list
                    e["mood"] = new_mood
                    e["writing"] = new_text
                    # rewrite CSV
                    with open(JOURNAL_FILE, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(["date", "username", "mood", "writing"])
                        for x in journal_entries:
                            writer.writerow([x.get("date", ""), x.get("username", ""), x.get("mood", ""), x.get("writing", "")])
                    st.success("Journal entry updated!")
                st.markdown("---")
