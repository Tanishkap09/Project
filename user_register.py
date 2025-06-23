import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from subprocess import call
import sqlite3
from tkinter import messagebox as ms
import re
import random
import email_sender
from datetime import datetime

# Initialize the main window
ctk.set_appearance_mode("light")  # Set light theme

root = ctk.CTk()
root.title("Pregnancy Care System - Registration")
root.configure(bg="#52C1DD")  # Light blue background

# Set window to native resolution
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")

# Header label
label_l1 = ctk.CTkLabel(
    root,
    text="Pregnancy Care System - Registration",
    font=("Arial", 26, 'bold'),
    fg_color="#007acc",  # Blue header background
    text_color="white",
    height=50,
    corner_radius=10
)
label_l1.pack(fill="x")

# Database setup
db = sqlite3.connect('pregnancy_data.db')
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "user" (
    "fullname"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"cntno"	TEXT NOT NULL,
	"age"	INTEGER NOT NULL,
	"dop"	TEXT NOT NULL,
	"username"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"risklvl"	TEXT NOT NULL,
	"disease"	TEXT NOT NULL,
    "reg_date"	TEXT NOT NULL,
	PRIMARY KEY("username")
)
""")
db.commit()

def validate_inputs():
    fname = entry_vars["user_fullname"].get().strip()
    addr = entry_vars["user_address"].get().strip()
    email = entry_vars["user_email"].get().strip()
    mobile = entry_vars["user_phone"].get().strip()
    age = entry_vars["user_age"].get().strip()
    dop = entry_vars["user_dop"].get().strip()
    username = entry_vars["user_username"].get().strip()
    password = entry_vars["user_password"].get()
    confirm_password = entry_vars["user_password_confirm"].get()

    if not fname or fname.isdigit():
        ms.showerror("Error", "Please enter a valid full name.")
        return False
    if not addr:
        ms.showerror("Error", "Please enter an address.")
        return False
    if not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
        ms.showerror("Error", "Please enter a valid email.")
        return False
    if not mobile.isdigit() or len(mobile) != 10:
        ms.showerror("Error", "Please enter a valid 10-digit phone number.")
        return False
    if not age.isdigit() or int(age) <= 0 or int(age) > 100:
        ms.showerror("Error", "Please enter a valid age between 1-100.")
        return False
    if not re.match(r'\d{4}-\d{2}-\d{2}', dop):
        ms.showerror("Error", "Please enter Date of Pregnancy in YYYY-MM-DD format.")
        return False
    if not username:
        ms.showerror("Error", "Please enter a username.")
        return False
    if len(password) < 6 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char in ['$','@','#','%'] for char in password):
        ms.showerror("Error", "Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.")
        return False
    if password != confirm_password:
        ms.showerror("Error", "Passwords do not match.")
        return False
    return True

def register_user():
    if validate_inputs():
        fname = entry_vars["user_fullname"].get().strip()
        addr = entry_vars["user_address"].get().strip()
        email = entry_vars["user_email"].get().strip()
        mobile = entry_vars["user_phone"].get().strip()
        age = entry_vars["user_age"].get().strip()
        dop = entry_vars["user_dop"].get().strip()
        username = entry_vars["user_username"].get().strip()
        password = entry_vars["user_password"].get()
        reg_date = datetime.now().strftime('%d-%m-%Y')  # ✅ Today's Date
        risklvl = "Low Risk"
        disease = "Healthy"

        with sqlite3.connect('pregnancy_data.db') as db:
            cursor = db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO pregnant_users (fullname, address, email, cntno, age, dop, username, password, risklvl, disease, reg_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (fname, addr, email, mobile, age, dop, username, password, risklvl, disease, reg_date))

                db.commit()
                ms.showinfo("Success", "Registration Successful!")
                email_sender.send_user_email(email, fname, username, password)
                ms.showinfo("Thank You For Registering", "Your account credentials are sent to your email.")
                root.destroy()
            except sqlite3.IntegrityError:
                ms.showerror("Error", "Username already exists. Choose a different one.")

# Create registration form
container = ctk.CTkFrame(root, fg_color="white", corner_radius=10)
container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.8)

ctk.CTkLabel(container, text="User Registration", font=("Arial", 22, "bold"), fg_color="white", text_color="black").pack(pady=10)

fields = [
    ("Full Name", "user_fullname"),
    ("Address", "user_address"),
    ("Email", "user_email"),
    ("Phone Number", "user_phone"),
    ("Age", "user_age"),
    ("Date of Pregnancy (YYYY-MM-DD)", "user_dop"),  # ← new field
    ("Username", "user_username"),
    ("Password", "user_password", "*"),
    ("Confirm Password", "user_password_confirm", "*")
]

entry_vars = {}

for field in fields:
    label_text, var_name = field[:2]
    show_char = field[2] if len(field) > 2 else None
    ctk.CTkLabel(container, text=label_text, font=("Arial", 14), fg_color="white", text_color="black").pack()
    entry_vars[var_name] = ctk.CTkEntry(container, placeholder_text=label_text, show=show_char, width=300, height=30)
    entry_vars[var_name].pack(pady=2)

# Submit button
submit_button = ctk.CTkButton(container, text='Register', command=register_user, fg_color="black", text_color="white", hover_color="#007acc", width=200, height=40)
submit_button.place(relx=0.95, rely=0.95, anchor="se")

# Run the Tkinter event loop
root.mainloop()