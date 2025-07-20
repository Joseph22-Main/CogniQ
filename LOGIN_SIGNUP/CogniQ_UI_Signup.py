import flet as ft

def main(page: ft.Page):
    page.title = "Sign Up UI"
    page.window_width = 1280
    page.window_height = 720
    page.bgcolor = "#edeec9"
    page.padding = 0

    bg = ft.Image(
        src="CogniQsn.png",
        width=1280,
        height=720,
        fit=ft.ImageFit.COVER
    )

    font = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color="white")

    email = ft.TextField(
        hint_text="Email",
        bgcolor="#98c9a3",
        border_color="#2ecc71",
        border_radius=16,
        text_style=font,
        height=50,
        width=400,
        cursor_color="white"
    )

    password = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        bgcolor="#98c9a3",
        border_color="#2ecc71",
        border_radius=16,
        text_style=font,
        height=50,
        width=400,
        cursor_color="white"
    )

    sign_up_btn = ft.ElevatedButton(
        text="Sign Up",
        bgcolor="#A3E4D7",
        color="white",
        style=ft.ButtonStyle(
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=16),
            overlay_color="#98c9a3"
        ),
        width=150,
        height=45
    )

    form = ft.Column(
        controls=[email, password, sign_up_btn],
        spacing=20,
        horizontal_alignment="center"
    )

    form_container = ft.Container(
        content=form,
        left=680,  
        top=250,   
        width=400,
        height=250,
        bgcolor=None
    )

    page.add(
        ft.Stack(
            controls=[
                bg,
                form_container
            ]
        )
    )

ft.app(target=main)
