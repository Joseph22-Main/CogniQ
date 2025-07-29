# graph.py
from datetime import datetime
import matplotlib.pyplot as plt
import tempfile
import os
from database import CogniQDatabase

def parse_datetime(date_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date format not supported: {date_str}")

def plot_user_mood_graph(user_email):
    db = CogniQDatabase()
    moods = db.get_moods(user_email) 
    if not moods:
        return ""
    moods_sorted = sorted(moods, key=lambda x: parse_datetime(x['date']))
    dates = [x['date'] for x in moods_sorted]
    mood_levels = [x['mood_level'] for x in moods_sorted]
    plt.figure(figsize=(8, 5))
    plt.plot(dates, mood_levels, marker='o', color='teal')
    plt.title(f"Mood Tracker for {user_email}")
    plt.xlabel("Date")
    plt.ylabel("Mood Level")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    temp_file = os.path.join(tempfile.gettempdir(), f"mood_plot_{user_email}.png")
    plt.savefig(temp_file)
    plt.close()

    return temp_file


