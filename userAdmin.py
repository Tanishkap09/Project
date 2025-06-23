# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:02:11 2025

@author: parge
"""

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from subprocess import call

# Initialize Main Window
ctk.set_appearance_mode("light")  # Light mode
root = ctk.CTk()
root.title("Select User Type")
root.geometry("1920x1080")
root.configure(bg="white")  # Keep the theme simple and professional

# =================== HEADER ===================
header_label = ctk.CTkLabel(
    root, text="Welcome to Pregnancy Care System",
    font=("Poppins", 30, "bold"), fg_color="black", text_color="white",
    height=80, corner_radius=10
)
header_label.pack(fill="x", pady=20)

# =================== SELECTION CONTAINER ===================
container = ctk.CTkFrame(root, fg_color="white", corner_radius=15)
container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.5)

# Heading
info_heading = ctk.CTkLabel(container, text="Select Your Role", font=("Poppins", 24, "bold"), text_color="black")
info_heading.pack(pady=(30, 20))

# Function to Navigate
def open_admin():
    call(["python", "admin_login.py"])

def open_user():
    call(["python", "user_login.py"])

# Admin Button
admin_btn = ctk.CTkButton(
    container, text="Admin", command=open_admin,
    fg_color="black", text_color="white", hover_color="#007acc",
    width=300, height=60, corner_radius=10
)
admin_btn.pack(pady=20)

# User Button
user_btn = ctk.CTkButton(
    container, text="User", command=open_user,
    fg_color="black", text_color="white", hover_color="#007acc",
    width=300, height=60, corner_radius=10
)
user_btn.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
