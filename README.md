# ✍️ WriteDaily+

WriteDaily+ is a **Streamlit** app for daily creative writing and journaling. Users can write **public creative pieces** or maintain a **private personal journal**. Each day has a **theme** or **word of the day** as inspiration.  

## 🌟 Features

- 🎨 Daily inspiration: **Theme of the Day** or **Word of the Day**
- 📝 Public creative writing submissions
- 🔐 Personal private journal with **mood tracking**
- 🔥 Journal streak counter
- 💡 Daily quote displayed in the sidebar
- ✏️ Supports editing past journal entries

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/avantikamogha/WriteDaily-plus.git
cd WriteDaily-plus
(Optional but recommended) Create a virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
🚀 Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open the URL provided by Streamlit in your browser 🌐

Use the sidebar to select daily inspiration, navigate the menu, and track your journal streak 🔥

📂 Project Structure
bash
Copy code
WriteDaily-plus/
├─ app.py          # Main Streamlit app
├─ config.py       # Paths and constants
├─ helpers.py      # CSV and asset helper functions
├─ ui.py           # Streamlit UI components
├─ data/           # Stores public and journal CSV files
├─ assets/         # Quotes, themes, and words
├─ requirements.txt
└─ README.md
🤝 Contributing
Create a branch (git checkout -b feature-name) 🌿

Make your changes ✨

Commit (git commit -am 'Add new feature') 💾

Push to branch (git push origin feature-name) ⬆️

Open a Pull Request 🔀
