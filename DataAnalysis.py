import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from textblob import TextBlob

class DataAnalyzer:
    def __init__(self, mood_data, journal_data):
        self.mood_data = self.validate_and_convert_moods(mood_data)
        self.journal_data = self.validate_journals(journal_data)

    def validate_and_convert_moods(self, mood_data):
        mood_scale = {
            "terrible": 1, "bad": 2, "neutral": 3, "good": 4, "great": 5,
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5
        }
        valid_data = []
        for entry in mood_data:
            try:
                entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                mood = str(entry["mood"]).strip().lower()
                mood_num = mood_scale.get(mood)
                if mood_num:
                    valid_data.append({
                        "user_id": entry["user_id"],
                        "date": entry_date.strftime("%Y-%m-%d"),
                        "mood": mood_num
                    })
                else:
                    print(f"Skipping invalid mood value: {mood}")
            except Exception as e:
                print(f"Skipping invalid mood entry: {entry} - Reason: {e}")
        return valid_data

    def validate_journals(self, journal_data):
        valid_journals = []
        for entry in journal_data:
            try:
                entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                valid_journals.append({
                    "user_id": entry["user_id"],
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "text": entry["text"]
                })
            except Exception as e:
                print(f"Skipping invalid journal entry: {entry} - Reason: {e}")
        return valid_journals

    def mood_trend(self):
        daily_moods = defaultdict(list)
        for entry in self.mood_data:
            daily_moods[entry["date"]].append(entry["mood"])

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
            journal_count[entry["date"]] += 1

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
        if not self.mood_data:
            print("No valid mood data.")
            return

        user_id = self.mood_data[0]["user_id"]
        mood_avg = sum(entry['mood'] for entry in self.mood_data) / len(self.mood_data)
        journal_avg = len(self.journal_data) / len(set(entry['date'] for entry in self.journal_data)) if self.journal_data else 0

        wellness = (mood_avg * 0.7) + (journal_avg * 0.3)
        print(f"📊 Estimated Wellness Score for {user_id}: {wellness:.2f}")

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        print(f"🧠 Sentiment: {sentiment}, Polarity: {polarity:.2f}")
        return sentiment, polarity


# Sample manual test (replace with your own interface or script)
if __name__ == "__main__":
    mood_data = [
        {"user_id": "charleigh", "date": "2025-07-21", "mood": "great"},
        {"user_id": "charleigh", "date": "2025-07-22", "mood": "4"},
        {"user_id": "charleigh", "date": "invalid-date", "mood": "neutral"},
    ]

    journal_data = [
        {"user_id": "charleigh", "date": "2025-07-22", "text": "I'm feeling a bit overwhelmed but hopeful."},
        {"user_id": "charleigh", "date": "2025-07-23", "text": "Today was productive and fun."}
    ]

    analyzer = DataAnalyzer(mood_data, journal_data)
    analyzer.mood_trend()
    analyzer.journal_frequency()
    analyzer.wellness_score()

    journal_input = input("Write a journal line: ")
    analyzer.analyze_sentiment(journal_input)
