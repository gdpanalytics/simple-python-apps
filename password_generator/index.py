import tkinter as tk
from tkinter import ttk
import random
import string


def update_label(event):
    current_value = int(slider_length.get())
    label_length.config(text=f"Password length: {current_value}")


def generate_password():
    password_characters = ""
    if var_upper.get():
        password_characters += string.ascii_uppercase
    if var_lower.get():
        password_characters += string.ascii_lowercase
    if var_numbers.get():
        password_characters += string.digits
    if var_special.get():
        password_characters += string.punctuation

    if password_characters:
        length = int(slider_length.get())
        password = "".join(random.choice(password_characters) for i in range(length))
        password_var.set(password)
    else:
        password_var.set("Select at least one set")


# main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x300")

# configure style
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"))
style.configure("TCheckbutton", font=("Helvetica", 12))

# variables
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=False)
password_var = tk.StringVar()

# slider
label_length = ttk.Label(root, text="Password length: 8")
label_length.pack(pady=10)
slider_length = ttk.Scale(
    root, from_=1, to_=24, orient="horizontal", command=update_label
)
slider_length.set(8)
slider_length.pack()

# params
frame_checks = ttk.Frame(root)
frame_checks.pack(pady=10)

check_upper = ttk.Checkbutton(
    frame_checks, text="Include uppercase", variable=var_upper
)
check_upper.grid(row=0, column=0, sticky="w", padx=20)
check_lower = ttk.Checkbutton(
    frame_checks, text="Include lowercase", variable=var_lower
)
check_lower.grid(row=0, column=1, sticky="w", padx=20)
check_numbers = ttk.Checkbutton(
    frame_checks, text="Include numbers", variable=var_numbers
)
check_numbers.grid(row=1, column=0, sticky="w", padx=20)
check_special = ttk.Checkbutton(
    frame_checks, text="Include special characters", variable=var_special
)
check_special.grid(row=1, column=1, sticky="w", padx=20)

# button
button_generate = ttk.Button(root, text="Generate Password", command=generate_password)
button_generate.pack(pady=20)

# show password
entry_password = ttk.Entry(
    root,
    textvariable=password_var,
    font=("Helvetica", 12, "bold"),
    foreground="red",
    justify="center",
)
entry_password.pack(pady=20)
entry_password.config(state="readonly")

root.mainloop()
