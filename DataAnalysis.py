import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import requests

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
        plt.title('📈 Average Daily Mood')
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
        plt.title('📘 Journal Entry Frequency')
        plt.xlabel('Date')
        plt.ylabel('Number of Entries')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def wellness_score(self):
        if not self.mood_data and not self.journal_data:
            print("⚠️ Not enough data to compute wellness score.")
            return

        mood_avg = (
            sum(entry['mood'] for entry in self.mood_data) / len(self.mood_data)
            if self.mood_data else 0
        )
        journal_days = set(entry['date'] for entry in self.journal_data)
        journal_avg = (
            len(self.journal_data) / len(journal_days)
            if journal_days else 0
        )

        wellness = (mood_avg * 0.7) + (journal_avg * 0.3)
        print(f"📊 Estimated Wellness Score: {wellness:.2f}")


# ✅ Public Sentiment Analysis API
def analyze_sentiment(text):
    url = "https://sentim-api.herokuapp.com/api/v1/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    data = {"text": text}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()["result"]
        sentiment = result["type"]
        polarity = result["polarity"]
        print(f"🧠 Sentiment: {sentiment.capitalize()} (Polarity: {polarity:.2f})")
        return sentiment, polarity
    except requests.exceptions.RequestException:
        print("❌ Failed to connect to the Sentiment API.")
        return None, None


# ✅ Sample Run for Testing
if __name__ == "__main__":
    print("🔍 Running Sample Mood and Journal Analysis...\n")

    # Example input data
    mood_data = [
        {'date': '2025-07-21', 'mood': 4},
        {'date': '2025-07-21', 'mood': 3},
        {'date': '2025-07-22', 'mood': 5},
    ]

    journal_data = [
        {'date': '2025-07-21', 'entry': 'Had a great day at school.'},
        {'date': '2025-07-22', 'entry': 'Finished my tasks ahead of schedule.'},
        {'date': '2025-07-22', 'entry': 'I feel a bit tired though.'},
    ]

    analyzer = DataAnalyzer(mood_data, journal_data)
    analyzer.mood_trend()
    analyzer.journal_frequency()
    analyzer.wellness_score()

    # Sentiment check
    print("\n💬 Sentiment Analysis")
    user_input = input("Enter a journal or mood description: ").strip()
    if user_input:
        analyze_sentiment(user_input)
    else:
        print("⚠️ No input provided for sentiment analysis.")
