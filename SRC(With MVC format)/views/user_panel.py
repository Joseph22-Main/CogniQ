import flet as ft
from database import CogniQDatabase
from recommendation import get_web_recommendations

db = CogniQDatabase()

def user_ui(page: ft.Page, user_email: str):
    from auth import login_signup_view

    page.title = "CogniQ - User Panel"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"

    def go_to_mood_input(e=None):
        page.clean()
        mood_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(str(i)) for i in range(1, 6)],
            width=250
        )
        btn = ft.ElevatedButton("Next", on_click=lambda e: go_to_journal_input(mood_dropdown.value))
        page.add(
            ft.Stack([
                ft.Image(src="user_mood_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=mood_dropdown, left=835, top=500),
                ft.Container(content=btn, left=860, top=580, width=200, height=60)
            ])
        )

    def go_to_journal_input(mood_value):
        page.clean()
        journal_field = ft.TextField(
            multiline=True, min_lines=10, max_lines=15,
            width=800, height=300
        )
        submit_btn = ft.ElevatedButton("Submit Entry", on_click=lambda e: submit_entry(mood_value, journal_field.value))
        page.add(
            ft.Stack([
                ft.Image(src="user_journal_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=journal_field, left=240, top=250),
                ft.Container(content=submit_btn, left=860, top=580, width=200, height=60)
            ])
        )

    def submit_entry(mood, journal_text):
        db.save_mood(user_email, int(mood))
        db.save_journal(user_email, journal_text)
        go_to_recommendation(journal_text)

    def go_to_recommendation(journal_text=""):
        page.clean()
        recommendations = get_web_recommendations(journal_text)
        page.add(
            ft.Stack([
                ft.Image(src="user_wellness_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(
                    content=ft.Column([
                        ft.Text("You're doing great today!", size=24),
                        ft.Column([ft.Text(f"- {rec}") for rec in recommendations]),
                        ft.ElevatedButton("View Logs", on_click=view_logs),
                        ft.ElevatedButton("Logout", on_click=logout)
                    ], spacing=15),
                    left=680, top=400
                )
            ])
        )

    def view_logs(e):
        logs = db.get_journals(user_email)
        page.clean()

        if not logs:
            page.add(
                ft.Stack([
                    ft.Image(src="user_logs_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                    ft.Container(
                        content=ft.Text("No journal entries found.", size=22),
                        left=450, top=300
                    ),
                    ft.Container(
                        content=ft.ElevatedButton("Back", on_click=lambda e: go_to_recommendation()),
                        left=860, top=580, width=200, height=60
                    )
                ])
            )
            return

        formatted_logs = "\n\n".join([f"📝 {date} —\n\"{content}\"" for content, date in logs])

        logs_display = ft.Text(
            value=formatted_logs,
            size=16,
            width=1000,
            selectable=True,
            no_wrap=False
        )

        page.add(
            ft.Stack([
                ft.Image(src="user_logs_ui.png", width=1280, height=720, fit=ft.ImageFit.COVER),
                ft.Container(content=logs_display, left=140, top=100),
                ft.Container(
                    content=ft.ElevatedButton("Back", on_click=lambda e: go_to_recommendation()),
                    left=860, top=580, width=200, height=60
                )
            ])
        )



    def logout(e):
        def login_clicked(email, password):
            if email.endswith("@admin.ph"):
                from admin_panel import admin_interface
                admin_interface(page)
            else:
                user_ui(page, email)

        def signup_clicked(email, password):
            page.snack_bar = ft.SnackBar(ft.Text("Signup successful. Please login."))
            page.snack_bar.open = True
            login_signup_view(page, login_clicked, signup_clicked)

        page.clean()
        login_signup_view(page, login_clicked, signup_clicked)
        page.update()

    go_to_mood_input()
