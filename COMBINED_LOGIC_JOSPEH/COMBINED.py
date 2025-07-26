import flet as ft
import matplotlib.pyplot as plt
import tempfile
import os
import datetime
import re

# ========== User & Authentication Logic ==========
class User:
    def __init__(self, email, password, user_type):
        self.email = email
        self.password = password
        self.user_type = user_type

    def __str__(self):
        return f"User(email='{self.email}', type='{self.user_type}')"


class AuthSystem:
    def __init__(self):
        self.users = []

    def determine_user_type(self, email):
        if email.endswith('@admin.ph'):
            return 'admin'
        elif email.endswith('@gmail.com'):
            return 'user'
        else:
            raise ValueError("Invalid email domain. Only @admin.ph or @gmail.com allowed")

    def signup(self, email, password):
        if any(user.email == email for user in self.users):
            raise ValueError("Email already registered")
        user_type = self.determine_user_type(email)
        new_user = User(email, password, user_type)
        self.users.append(new_user)
        return new_user

    def login(self, email, password):
        user = next((u for u in self.users if u.email == email), None)
        if user and user.password == password:
            return user
        return None


# ========== Admin Logic ==========
class Chart:
    def mood_graph(self, mood_data, dates):
        plt.plot(dates, mood_data, marker='o')
        plt.title("User Mood Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood Level")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def journal_graph(self, keywords):
        plt.bar(keywords.keys(), keywords.values())
        plt.title("Journal Keyword Frequency")
        plt.xlabel("Keywords")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


class Database:
    def __init__(self):
        self.users = {}

    def save_user_mood(self, email, mood):
        if email not in self.users:
            self.users[email] = {'mood': [], 'journal': []}
        self.users[email]['mood'].append((datetime.date.today().isoformat(), mood))

    def save_user_journal(self, email, entry):
        if email not in self.users:
            self.users[email] = {'mood': [], 'journal': []}
        self.users[email]['journal'].append((datetime.date.today().isoformat(), entry))

    def get_user_data(self, email):
        return self.users.get(email, None)

    def recommendation(self, mood, entry):
        if mood <= 3:
            return "You seem down. Consider talking to a counselor or practicing mindfulness."
        elif "stress" in entry.lower():
            return "Try deep breathing exercises or light walking."
        return "Keep up the good work! You're doing great."


class Admin:
    def __init__(self, email, password, name):
        if not self._validate_email(email):
            raise ValueError("Invalid email format.")
        self.admin_email = email
        self.admin_password = password
        self.admin_name = name
        self.db = Database()
        self.chart = Chart()

    def _validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def _extract_keywords(self, text):
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        keywords = {}
        for word in words:
            keywords[word] = keywords.get(word, 0) + 1
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])


# ========== Flet UI Logic ==========
def main(page: ft.Page):
    auth = AuthSystem()
    page.title = "CogniQ Login"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"

    font = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color="white")

    def show_login(e=None):
        page.controls.clear()
        email = ft.TextField(hint_text="Email", bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        password = ft.TextField(hint_text="Password", password=True, can_reveal_password=True, bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        msg = ft.Text("", style=font)

        def login_clicked(e):
            user = auth.login(email.value.strip(), password.value.strip())
            if user:
                if user.user_type == "admin":
                    load_admin_ui(page, show_login)
                else:
                    page.controls.clear()
                    page.add(ft.Text("User identified", size=30, color="green"))
                    page.update()
            else:
                msg.value = "Login failed."
                page.update()

        login_btn = ft.ElevatedButton(text="Login", on_click=login_clicked, bgcolor="#77bfa3", color="white",
                                       style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=16), overlay_color="#98c9a3"), width=150, height=45)

        signup_text = ft.TextButton(text="Don't have an account?", on_click=show_signup, style=ft.ButtonStyle(color="#77bfa3", overlay_color="#98c9a3"))

        form = ft.Column(controls=[email, password, login_btn, signup_text, msg], spacing=20, horizontal_alignment="center")
        form_container = ft.Container(content=form, left=680, top=250, width=400, height=300, bgcolor=None)

        page.add(ft.Stack(controls=[ft.Image(src="CogniQsn.png", width=1280, height=720, fit=ft.ImageFit.COVER), form_container]))
        page.update()

    def show_signup(e=None):
        page.controls.clear()
        email = ft.TextField(hint_text="Email", bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        password = ft.TextField(hint_text="Password", password=True, can_reveal_password=True, bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        msg = ft.Text("", style=font)

        def register(e):
            try:
                user = auth.signup(email.value.strip(), password.value.strip())
                msg.value = "Signup successful. Redirecting to login..."
                page.update()
                page.controls.clear()
                show_login()
            except Exception as err:
                msg.value = f"Error: {err}"
                page.update()

        sign_up_btn = ft.ElevatedButton(text="Sign Up", on_click=register, bgcolor="#77bfa3", color="white",
                                        style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=16), overlay_color="#98c9a3"), width=150, height=45)

        back_btn = ft.TextButton(text="Back to Login", on_click=show_login, style=ft.ButtonStyle(color="#77bfa3", overlay_color="#98c9a3"))

        form = ft.Column(controls=[email, password, sign_up_btn, back_btn, msg], spacing=20, horizontal_alignment="center")
        form_container = ft.Container(content=form, left=680, top=250, width=400, height=300, bgcolor=None)

        page.add(ft.Stack(controls=[ft.Image(src="COGNIQ_SIGNUP.png", width=1280, height=720, fit=ft.ImageFit.COVER), form_container]))
        page.update()

    show_login()

def load_admin_ui(page: ft.Page, logout_callback):
    sample_journal_entries = ["I felt stressed today because of deadlines.", "I had a great day at work!", "I'm feeling anxious about tomorrow."]
    sample_mood_data = {"2025-07-06": 3, "2025-07-07": 6, "2025-07-08": 5, "2025-07-09": 8}

    text_style = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color="white")
    btn_style = ft.ButtonStyle(bgcolor="#77bfa3", color="white", overlay_color={"hovered": "#98c9a3"}, shape=ft.RoundedRectangleBorder(radius=12), padding=20)

    def view_journal(e):
        page.dialog = ft.AlertDialog(title=ft.Text("Journal Entries", style=text_style), content=ft.Text("\n\n".join(sample_journal_entries), style=text_style))
        page.dialog.open = True
        page.update()

    def view_mood(e):
        mood_text = "\n".join([f"{k}: Mood Level {v}" for k, v in sample_mood_data.items()])
        page.dialog = ft.AlertDialog(title=ft.Text("Mood Tracker", style=text_style), content=ft.Text(mood_text, style=text_style))
        page.dialog.open = True
        page.update()

    def show_analysis(e):
        text = " ".join(sample_journal_entries)
        keywords = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        freq = {}
        for word in keywords:
            freq[word] = freq.get(word, 0) + 1
        sorted_kw = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10])
        analysis_text = "\n".join([f"{k}: {v}" for k, v in sorted_kw.items()])
        page.dialog = ft.AlertDialog(title=ft.Text("Keyword Frequency", style=text_style), content=ft.Text(analysis_text, style=text_style))
        page.dialog.open = True
        page.update()

    def plot_graph(e):
        dates = list(sample_mood_data.keys())
        moods = list(sample_mood_data.values())

        plt.figure(figsize=(8, 5))
        plt.plot(dates, moods, marker='o', color='teal')
        plt.title("Mood Tracker")
        plt.xlabel("Date")
        plt.ylabel("Mood Level")
        plt.grid(True)
        plt.tight_layout()

        temp_file = os.path.join(tempfile.gettempdir(), "mood_plot.png")
        plt.savefig(temp_file)
        plt.close()

        page.dialog = ft.AlertDialog(title=ft.Text("Mood Graph", style=text_style), content=ft.Image(src=temp_file, width=600, height=400))
        page.dialog.open = True
        page.update()

    def logout(e):
        logout_callback()

    page.controls.clear()
    page.add(
        ft.Stack(controls=[
            ft.Image(src="COGNIQ_ADMINUI.png", width=1280, height=720, fit=ft.ImageFit.COVER),
            ft.Container(
                content=ft.Column([
                    ft.ElevatedButton("📔 View Journal Entries", on_click=view_journal, style=btn_style, width=300),
                    ft.ElevatedButton("😊 View Mood Tracker", on_click=view_mood, style=btn_style, width=300),
                    ft.ElevatedButton("📊 Show Data Analysis", on_click=show_analysis, style=btn_style, width=300),
                    ft.ElevatedButton("📈 Show Graphs", on_click=plot_graph, style=btn_style, width=300),
                    ft.ElevatedButton("🚪 Logout", on_click=logout, style=btn_style, width=300)
                ], spacing=25, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                left=680, top=250, padding=20
            )
        ])
    )
    page.update()

ft.app(target=main)
