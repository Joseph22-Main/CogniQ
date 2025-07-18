import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter.messagebox as msgbox

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

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CogniQ Admin Dashboard")
        self.geometry("1920x1080")
        self.resizable(False, False)

        # Load background image
        bg_image = Image.open("COGNIQ_ADMINUI.png")
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Set CustomTkinter appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Create label with image background
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_tk, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_buttons()

    def create_buttons(self):
        # Coordinates and sizes based on image design
        btn_width = 500
        btn_height = 60
        x_start = 1150
        y_start = 180
        y_gap = 100

        button_style = {
            "fg_color": "#62bda6",
            "corner_radius": 30,
            "width": btn_width,
            "height": btn_height,
            "font": ("Arial", 20)
        }

        self.journal_btn = ctk.CTkButton(
            self, text="📔 View Journal Entries",
            command=self.view_journal, **button_style
        )
        self.journal_btn.place(x=x_start, y=y_start)

        self.mood_btn = ctk.CTkButton(
            self, text="😊 View Mood Tracker",
            command=self.view_mood, **button_style
        )
        self.mood_btn.place(x=x_start, y=y_start + y_gap)

        self.analysis_btn = ctk.CTkButton(
            self, text="📊 Show Data Analysis",
            command=self.show_analysis, **button_style
        )
        self.analysis_btn.place(x=x_start, y=y_start + 2 * y_gap)

        self.graph_btn = ctk.CTkButton(
            self, text="📈 Show Graphs",
            command=self.plot_graph, **button_style
        )
        self.graph_btn.place(x=x_start, y=y_start + 3 * y_gap)


    def view_journal(self):
        if not sample_journal_entries:
            msgbox.showinfo("Info", "No journal entries available.")
            return
        msgbox.showinfo("Journal Entries", "\n\n".join(sample_journal_entries))

    def view_mood(self):
        if not sample_mood_data:
            msgbox.showinfo("Info", "No mood data available.")
            return
        mood_text = "\n".join([f"{k}: Mood Level {v}" for k, v in sample_mood_data.items()])
        msgbox.showinfo("Mood Tracker", mood_text)

    def show_analysis(self):
        if not sample_journal_entries:
            msgbox.showinfo("Info", "No data to analyze.")
            return
        keywords = self.extract_keywords(" ".join(sample_journal_entries))
        analysis_text = "\n".join([f"{k}: {v}" for k, v in keywords.items()])
        msgbox.showinfo("Keyword Frequency", analysis_text)

    def plot_graph(self):
        try:
            if not sample_mood_data:
                raise ValueError("No data to display.")
            dates = list(sample_mood_data.keys())
            moods = list(sample_mood_data.values())

            plt.figure(figsize=(8, 5))
            plt.plot(dates, moods, marker='o', color='teal')
            plt.title("Mood Tracker")
            plt.xlabel("Date")
            plt.ylabel("Mood Level")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            msgbox.showerror("Graph Error", str(e))

    def extract_keywords(self, text: str):
        import re
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        keywords = {}
        for word in words:
            keywords[word] = keywords.get(word, 0) + 1
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
