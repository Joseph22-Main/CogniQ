import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

class DataAnalyzer:
    def __init__(self, mood_data, journal_data):
        self.mood_data = mood_data
        self.journal_data = journal_data

    def mood_trend(self):
        daily_moods = defaultdict(list)

        for entry in self.mood_data:
            daily_moods[entry['date']].append(entry['mood'])

        dates = sorted(daily_moods.keys())
        avg_moods = [sum(moods) / len(moods) for date, moods in sorted(daily_moods.items())]

        plt.figure(figsize=(8, 5))
        plt.bar(dates, avg_moods, color='skyblue')
        plt.title('Average Daily Mood')
        plt.xlabel('Date')
        plt.ylabel('Mood (1–5)')
        plt.ylim(1, 5)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def journal_frequency(self):
        journal_count = defaultdict(int)

        for entry in self.journal_data:
            journal_count[entry['date']] += 1

        dates = sorted(journal_count.keys())
        frequencies = [journal_count[date] for date in dates]

        plt.figure(figsize=(8, 5))
        plt.bar(dates, frequencies, color='orange')
        plt.title('Journal Entry Frequency')
        plt.xlabel('Date')
        plt.ylabel('Number of Entries')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def wellness_score(self):
        mood_avg = sum(entry['mood'] for entry in self.mood_data) / len(self.mood_data) if self.mood_data else 0
        journal_avg = len(self.journal_data) / len(set(entry['date'] for entry in self.journal_data)) if self.journal_data else 0

        wellness = (mood_avg * 0.7) + (journal_avg * 0.3)
        print(f"📊 Estimated Wellness Score: {wellness:.2f} (Mood-based)")
