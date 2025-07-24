import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import requests

# Mood word-to-number map
MOOD_MAP = {
    "very happy": 5, "happy": 4,
    "neutral": 3,
    "sad": 2, "very sad": 1
}

class DataAnalyzer:
    def __init__(self, mood_data, journal_data, user_id):
        self.user_id = user_id
        self.mood_data = self._filter_and_validate(mood_data)
        self.journal_data = self._filter_and_validate(journal_data)

    def _filter_and_validate(self, data):
        valid_entries = []
        for entry in data:
            try:
                if entry['user_id'] != self.user_id:
                    continue
                # Validate date
                datetime.strptime(entry['date'], "%Y-%m-%d")

                # Convert letter mood to number
                if 'mood' in entry and isinstance(entry['mood'], str):
                    mood_str = entry['mood'].strip().lower()
                    entry['mood'] = MOOD_MAP.get(mood_str, 3)  # default to neutral (3)

                valid_entries.append(entry)
            except Exception as e:
                print(f"Skipping invalid entry: {entry} - Reason: {e}")
        return valid_entries

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
        print(f"📊 Estimated Wellness Score for {self.user_id}: {wellness:.2f}")

# Optional: Sentiment API Function
def analyze_sentiment(text):
    url = "https://sentim-api.herokuapp.com/api/v1/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        sentiment = response.json()["result"]["type"]
        polarity = response.json()["result"]["polarity"]
        print(f"Sentiment: {sentiment}, Polarity: {polarity}")
        return sentiment, polarity
    else:
        print("API request failed.")
        return None, None

# Example usage
if __name__ == "__main__":
    # Example data for testing
    mood_data = [
        {"user_id": "charleigh", "date": "2025-07-21", "mood": "happy"},
        {"user_id": "charleigh", "date": "2025-07-22", "mood": "sad"},
        {"user_id": "charleigh", "date": "invalid-date", "mood": "neutral"},  # This will be skipped
        {"user_id": "anotheruser", "date": "2025-07-22", "mood": 4},  # Filtered by user_id
    ]

    journal_data = [
        {"user_id": "charleigh", "date": "2025-07-21", "entry": "Today was good."},
        {"user_id": "charleigh", "date": "2025-07-22", "entry": "Feeling low."},
    ]

    analyzer = DataAnalyzer(mood_data, journal_data, user_id="charleigh")
    analyzer.mood_trend()
    analyzer.journal_frequency()
    analyzer.wellness_score()

    # Run sentiment analysis if you want
    text = input("Write a journal line: ")
    analyze_sentiment(text)
