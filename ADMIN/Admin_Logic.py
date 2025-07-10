from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import datetime
import re

try:
    class Chart:
        def mood_graph(self, mood_data: List[int], dates: List[str]):
            try:
                plt.plot(dates, mood_data, marker='o')
                plt.title("User Mood Over Time")
                plt.xlabel("Date")
                plt.ylabel("Mood Level")
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            except Exception as e:
                print("Error generating mood graph:", e)

        def journal_graph(self, keywords: Dict[str, int]):
            try:
                plt.bar(keywords.keys(), keywords.values())
                plt.title("Journal Keyword Frequency")
                plt.xlabel("Keywords")
                plt.ylabel("Frequency")
                plt.tight_layout()
                plt.show()
            except Exception as e:
                print("Error generating journal graph:", e)

        def conclusion_graph(self):
            print("Conclusion graph feature under development.")

    class Database:
        def __init__(self):
            self.users = {}

        def save_user_mood(self, email: str, mood: int):
            if email not in self.users:
                self.users[email] = {'mood': [], 'journal': []}
            self.users[email]['mood'].append((datetime.date.today().isoformat(), mood))

        def save_user_journal(self, email: str, entry: str):
            if email not in self.users:
                self.users[email] = {'mood': [], 'journal': []}
            self.users[email]['journal'].append((datetime.date.today().isoformat(), entry))

        def get_user_data(self, email: str):
            return self.users.get(email, None)

        def recommendation(self, mood: int, entry: str) -> str:
            if mood <= 3:
                return "You seem down. Consider talking to a counselor or practicing mindfulness."
            elif "stress" in entry.lower():
                return "Try deep breathing exercises or light walking."
            return "Keep up the good work! You're doing great."

    class Admin:
        def __init__(self, email: str, password: str, name: str):
            if not self._validate_email(email):
                raise ValueError("Invalid email format.")
            self.admin_email = email
            self.admin_password = password
            self.admin_name = name
            self.population = 0
            self.db = Database()
            self.chart = Chart()

        def _validate_email(self, email: str) -> bool:
            return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

        def obs_journal(self, user_email: str, entry: str):
            if not entry.strip():
                raise ValueError("Journal entry cannot be empty.")
            self.db.save_user_journal(user_email, entry)
            print("Journal saved successfully.")

        def obs_mood_user(self, user_email: str, mood: int):
            if not (1 <= mood <= 10):
                raise ValueError("Mood must be between 1 and 10.")
            self.db.save_user_mood(user_email, mood)
            print("Mood saved successfully.")

        def obs_login(self, user_email: str):
            data = self.db.get_user_data(user_email)
            if not data:
                raise ValueError("User not found.")
            dates, moods = zip(*data['mood']) if data['mood'] else ([], [])
            _, journals = zip(*data['journal']) if data['journal'] else ([], [])

            if moods:
                self.chart.mood_graph(list(moods), list(dates))
            else:
                print("No mood data available.")

            if journals:
                keywords = self._extract_keywords(" ".join(journals))
                self.chart.journal_graph(keywords)
            else:
                print("No journal data available.")

        
        def get_recommendation(self, user_email: str) -> str:
            data = self.db.get_user_data(user_email)
            if not data:
                raise ValueError("User not found.")
            latest_mood = data['mood'][-1][1] if data['mood'] else 5
            latest_entry = data['journal'][-1][1] if data['journal'] else ""
            return self.db.recommendation(latest_mood, latest_entry)

       
        def _extract_keywords(self, text: str) -> Dict[str, int]:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower()) 
            keywords = {}
            for word in words:
                keywords[word] = keywords.get(word, 0) + 1
            return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])  

        def del_user(self, user_email: str):
            if user_email in self.db.users:
                del self.db.users[user_email]
                print(f"User {user_email} deleted.")
            else:
                print("User not found.")
except Exception as e:
    print("Error", e)

