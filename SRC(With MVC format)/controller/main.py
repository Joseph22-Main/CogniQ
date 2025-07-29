import flet as ft
from auth import login_signup_view
from user_panel import user_ui
from admin_panel import admin_interface

def main(page: ft.Page):
    page.title = "CogniQ App"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"

    def login_clicked(email, password):
        if email.endswith("@admin.ph"):
            admin_interface(page)
        else:
            user_ui(page, email)

    def signup_clicked(email, password):
        page.snack_bar = ft.SnackBar(ft.Text("Signup successful. Please login."))
        page.snack_bar.open = True
        login_signup_view(page, login_clicked, signup_clicked)

    login_signup_view(page, login_clicked, signup_clicked)

ft.app(target=main)
