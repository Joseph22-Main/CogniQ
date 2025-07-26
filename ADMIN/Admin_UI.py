import flet as ft
import matplotlib.pyplot as plt
from datetime import datetime
import tempfile
import os

sample_journal_entries = [
    "I felt stressed today because of deadlines.",
    "I had a great day at work!",
    "I'm feeling anxious about tomorrow."
]

sample_mood_data = {
    "2025-07-06": 3,
    "2025-07-07": 6,
    "2025-07-08": 5,
    "2025-07-09": 8
}

def main(page: ft.Page):
    page.title = "CogniQ Admin Dashboard"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#0D1B2A"

    btn_style = ft.ButtonStyle(
        bgcolor="#2ecc71",
        color="white",
        overlay_color={"hovered": "#98c9a3"},
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=20
    )
    text_style = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color="white")

    def view_journal(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Journal Entries", style=text_style),
            content=ft.Text("\n\n".join(sample_journal_entries) if sample_journal_entries else "No entries.", style=text_style),
        )
        page.dialog.open = True
        page.update()

    def view_mood(e):
        mood_text = "\n".join([f"{k}: Mood Level {v}" for k, v in sample_mood_data.items()])
        page.dialog = ft.AlertDialog(
            title=ft.Text("Mood Tracker", style=text_style),
            content=ft.Text(mood_text if mood_text else "No mood data available.", style=text_style),
        )
        page.dialog.open = True
        page.update()

    def show_analysis(e):
        if not sample_journal_entries:
            analysis_text = "No data to analyze."
        else:
            keywords = extract_keywords(" ".join(sample_journal_entries))
            analysis_text = "\n".join([f"{k}: {v}" for k, v in keywords.items()])
        page.dialog = ft.AlertDialog(
            title=ft.Text("Keyword Frequency", style=text_style),
            content=ft.Text(analysis_text, style=text_style),
        )
        page.dialog.open = True
        page.update()

    def plot_graph(e):
        if not sample_mood_data:
            page.dialog = ft.AlertDialog(title=ft.Text("No data to display.", style=text_style))
            page.dialog.open = True
            page.update()
            return

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

        page.dialog = ft.AlertDialog(
            title=ft.Text("Mood Graph", style=text_style),
            content=ft.Image(src=temp_file, width=600, height=400)
        )
        page.dialog.open = True
        page.update()

    def extract_keywords(text):
        import re
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        keywords = {}
        for word in words:
            keywords[word] = keywords.get(word, 0) + 1
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])

    page.add(
        ft.Stack(
            controls=[
                ft.Image(src="COGNIQ_ADMINUI.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.ElevatedButton("📔 View Journal Entries", on_click=view_journal, style=btn_style, width=300),
                            ft.ElevatedButton("😊 View Mood Tracker", on_click=view_mood, style=btn_style, width=300),
                            ft.ElevatedButton("📊 Show Data Analysis", on_click=show_analysis, style=btn_style, width=300),
                            ft.ElevatedButton("📈 Show Graphs", on_click=plot_graph, style=btn_style, width=300),
                        ],
                        spacing=25,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    left=680,
                    top=250,
                    padding=20
                )
            ]
        )
    )

ft.app(target=main)
