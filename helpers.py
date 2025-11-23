# helpers.py
import csv
import os
import random

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

# ---------------- CSV Helpers ----------------
def save_public_entry(file, date, user, anon, insp_type, insp, insp_full, wtype, text):
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, user, anon, insp_type, insp, insp_full, wtype, text])

def load_public_entries(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except:
        return []

def save_journal_entry(file, date, user, mood, text):
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, user, mood, text])

def load_journal_entries(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except:
        return []
