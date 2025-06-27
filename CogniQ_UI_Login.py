import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Login UI")
app.geometry("1280x720")
app.resizable(False, False)

bg_image = Image.open("CogniQln.png").resize((1280, 720))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(master=app, text="", image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

form_frame = ctk.CTkFrame(
    master=app,
    width=400,
    height=250,
    fg_color="transparent",  # allowed
    bg_color="#edeec9"   # allowed
)
form_frame.place(x=650, y=250)

field_bg = "#98c9a3"
border_color = "#2ecc71"

email_entry = ctk.CTkEntry(
    master=form_frame,
    width=400,
    height=50,
    corner_radius=16,
    placeholder_text="Email",
    font=("Raleway", 16),
    fg_color=field_bg,
    border_color=border_color,
    border_width=2,
    text_color="white",
)
email_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    master=form_frame,
    width=400,
    height=50,
    corner_radius=16,
    placeholder_text="Password",
    font=("Raleway", 16),
    fg_color=field_bg,
    border_color=border_color,
    border_width=2,
    text_color="white",
    show="*"
)
password_entry.pack(pady=10)

signup_button = ctk.CTkButton(
    master=form_frame,
    text="Login",
    width=150,
    height=45,
    corner_radius=16,
    font=("Raleway", 16, "bold"),
    fg_color="#A3E4D7",
    hover_color="#98c9a3",
    text_color="white"
)
signup_button.pack(pady=20)

app.mainloop()
