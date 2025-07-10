import datetime
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, mood_entries, journal_entries):
        self.mood_entries = mood_entries  # List of dicts: {'date': ..., 'mood': ...}
        self.journal_entries = journal_entries  # List of dicts: {'date': ..., 'text': ...}

    def mood_trend(self):
        # Group moods by date
        daily_moods = defaultdict(list)
        for entry in self.mood_entries:
            date = entry['date']
            mood = entry['mood']
            daily_moods[date].append(mood)

        # Calculate average mood per day
        avg_daily_mood = {
            date: sum(moods) / len(moods)
            for date, moods in daily_moods.items()
        }

        # Plot mood trend
        dates = sorted(avg_daily_mood.keys())
        mood_scores = [avg_daily_mood[date] for date in dates]

        plt.figure(figsize=(10, 4))
        plt.plot(dates, mood_scores, marker='o', linestyle='-', color='purple')
        plt.title("Mood Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Average Mood Score")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return avg_daily_mood

    def journal_frequency(self):
        # Count journal entries by date
        frequency = defaultdict(int)
        for entry in self.journal_entries:
            frequency[entry['date']] += 1

        # Plot journal frequency
        dates = sorted(frequency.keys())
        counts = [frequency[date] for date in dates]

        plt.figure(figsize=(10, 4))
        plt.bar(dates, counts, color='teal')
        plt.title("Journal Entry Frequency")
        plt.xlabel("Date")
        plt.ylabel("Entries")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return frequency

    def wellness_score(self):
        # Combine mood and journaling data to generate a wellness score
        score_by_day = defaultdict(lambda: {"moods": [], "journals": 0})
        for m in self.mood_entries:
            score_by_day[m['date']]['moods'].append(m['mood'])

        for j in self.journal_entries:
            score_by_day[j['date']]['journals'] += 1

        # Compute score: mood average + journal impact (e.g., +0.5 per entry)
        wellness_scores = {}
        for date, values in score_by_day.items():
            mood_avg = statistics.mean(values['moods']) if values['moods'] else 0
            journal_bonus = 0.5 * values['journals']
            wellness_scores[date] = round(mood_avg + journal_bonus, 2)

        # Plot wellness score
        dates = sorted(wellness_scores.keys())
        scores = [wellness_scores[date] for date in dates]

        plt.figure(figsize=(10, 4))
        plt.plot(dates, scores, marker='o', linestyle='-', color='green')
        plt.title("Overall Wellness Score")
        plt.xlabel("Date")
        plt.ylabel("Score")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return wellness_scores
