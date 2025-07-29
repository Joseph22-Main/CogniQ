import flet as ft
from database import CogniQDatabase
from graph import plot_user_mood_graph
from auth import login_signup_view

db = CogniQDatabase()

def admin_interface(page: ft.Page):
    page.title = "CogniQ - Admin Panel"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"

    def go_back(e=None):
        admin_interface(page)

    def logout(e):
        def login_clicked(email, password):
            if email.endswith("@admin.ph"):
                admin_interface(page)
            else:
                from user_panel import user_ui
                user_ui(page, email)

        def signup_clicked(email, password):
            page.snack_bar = ft.SnackBar(ft.Text("Signup successful. Please login."))
            page.snack_bar.open = True
            login_signup_view(page, login_clicked, signup_clicked)

        page.clean()
        login_signup_view(page, login_clicked, signup_clicked)
        page.update()

    def go_to_view_logs(e=None):
        page.clean()

        user_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(user) for user in db.get_all_users()],
            width=250
        )

        log_display = ft.Text(value="", size=16, selectable=True, width=800)

        def load_logs(e):
            logs = db.get_journals(user_dropdown.value)
            if logs:
                formatted_logs = "\n\n".join([f"📝 {entry[0]} — \"{entry[1]}\"" for entry in logs])
                log_display.value = formatted_logs
            else:
                log_display.value = "No journal entries."
            page.update()

        user_dropdown.on_change = load_logs

        page.add(
            ft.Stack([
                ft.Image(src="admin_bg_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=user_dropdown, left=150, top=200),
                ft.Container(content=log_display, left=150, top=270),
                ft.Container(content=ft.ElevatedButton("Back", on_click=go_back), left=150, top=600),
                ft.Container(content=ft.ElevatedButton("Logout", on_click=logout), left=300, top=600)
            ])
        )

    def go_to_view_mood(e=None):
        page.clean()

        user_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(user) for user in db.get_all_users()],
            width=250
        )

        mood_display = ft.Text(value="", size=16, selectable=True, width=800)

        def load_moods(e):
            moods = db.get_moods(user_dropdown.value)
            if moods:
                formatted_moods = "\n\n".join([f"📊 {entry['date']} — Mood: {entry['mood_level']}" for entry in moods])
                mood_display.value = formatted_moods
            else:
                mood_display.value = "No mood entries."
            page.update()

        user_dropdown.on_change = load_moods

        page.add(
            ft.Stack([
                ft.Image(src="admin_bg_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=user_dropdown, left=150, top=200),
                ft.Container(content=mood_display, left=150, top=270),
                ft.Container(content=ft.ElevatedButton("Back", on_click=go_back), left=150, top=600),
                ft.Container(content=ft.ElevatedButton("Logout", on_click=logout), left=300, top=600)
            ])
        )

    def go_to_view_graphs(e=None):
        page.clean()

        user_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(user) for user in db.get_all_users()],
            width=250
        )

        graph_image = ft.Image(src="", width=800, height=400)

        def load_graph(e):
            image_path = plot_user_mood_graph(user_dropdown.value)
            graph_image.src = image_path
            page.update()

        user_dropdown.on_change = load_graph

        page.add(
            ft.Stack([
                ft.Image(src="admin_bg_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=user_dropdown, left=150, top=200),
                ft.Container(content=graph_image, left=150, top=280),
                ft.Container(content=ft.ElevatedButton("Back", on_click=go_back), left=150, top=600),
                ft.Container(content=ft.ElevatedButton("Logout", on_click=logout), left=300, top=600)
            ])
        )

    page.clean()
    page.add(
        ft.Stack([
            ft.Image(src="admin_bg_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
            ft.Container(content=ft.Column([
                ft.ElevatedButton("View Journals", on_click=go_to_view_logs),
                ft.ElevatedButton("View Mood Tracker", on_click=go_to_view_mood),
                ft.ElevatedButton("View Graphs", on_click=go_to_view_graphs),
                ft.ElevatedButton("Logout", on_click=logout)
            ], spacing=20), left=100, top=250)
        ])
    )
