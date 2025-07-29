import flet as ft

def login_signup_view(page: ft.Page, login_clicked_cb, signup_clicked_cb):
    page.title = "CogniQ Login"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"

    font = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color="white")

    def show_login(e=None):
        page.controls.clear()
        email = ft.TextField(hint_text="Email", bgcolor="#98c9a3", border_color="#2ecc71",
                             border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        password = ft.TextField(hint_text="Password", password=True, can_reveal_password=True,
                                bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16,
                                text_style=font, height=50, width=400, cursor_color="white")
        msg = ft.Text("", style=font)

        def login_clicked(e):
            login_clicked_cb(email.value.strip(), password.value.strip())

        login_btn = ft.ElevatedButton(text="Login", on_click=login_clicked, bgcolor="#77bfa3", color="white",
                                      style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=16),
                                                           overlay_color="#98c9a3"), width=150, height=45)

        signup_text = ft.TextButton(text="Don't have an account?", on_click=show_signup,
                                    style=ft.ButtonStyle(color="#77bfa3", overlay_color="#98c9a3"))

        form = ft.Column(controls=[email, password, login_btn, signup_text, msg], spacing=20,
                         horizontal_alignment="center")
        form_container = ft.Container(content=form, left=680, top=250, width=400, height=300)

        page.add(ft.Stack(controls=[
            ft.Image(src="CogniQsn.png", width=1280, height=720, fit=ft.ImageFit.COVER),
            form_container
        ]))
        page.update()

    def show_signup(e=None):
        page.controls.clear()
        email = ft.TextField(hint_text="Email", bgcolor="#98c9a3", border_color="#2ecc71",
                             border_radius=16, text_style=font, height=50, width=400, cursor_color="white")
        password = ft.TextField(hint_text="Password", password=True, can_reveal_password=True,
                                bgcolor="#98c9a3", border_color="#2ecc71", border_radius=16,
                                text_style=font, height=50, width=400, cursor_color="white")
        msg = ft.Text("", style=font)

        def register(e):
            signup_clicked_cb(email.value.strip(), password.value.strip())

        sign_up_btn = ft.ElevatedButton(text="Sign Up", on_click=register, bgcolor="#77bfa3", color="white",
                                        style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=16),
                                                             overlay_color="#98c9a3"), width=150, height=45)

        back_btn = ft.TextButton(text="Back to Login", on_click=show_login,
                                 style=ft.ButtonStyle(color="#77bfa3", overlay_color="#98c9a3"))

        form = ft.Column(controls=[email, password, sign_up_btn, back_btn, msg], spacing=20,
                         horizontal_alignment="center")
        form_container = ft.Container(content=form, left=680, top=250, width=400, height=300)

        page.add(ft.Stack(controls=[
            ft.Image(src="COGNIQ_SIGNUP.png", width=1280, height=720, fit=ft.ImageFit.COVER),
            form_container
        ]))
        page.update()

    show_login()
