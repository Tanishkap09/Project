import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from subprocess import call
import tkinter.messagebox as tkmb 
import sqlite3
from tkinter import messagebox as ms

# Initialize the main window
ctk.set_appearance_mode("light")  # Set light theme

root = ctk.CTk()
root.title("Pregnancy Care System")
root.configure(bg="#52C1DD")  # Light blue background

# Set window to native resolution
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")

# Header label
label_l1 = ctk.CTkLabel(
    root,
    text="Pregnancy Care System",
    font=("Arial", 26, 'bold'),
    fg_color="#007acc",  # Blue header background
    text_color="white",
    height=50,
    corner_radius=10
)
label_l1.pack(fill="x")

# Load and place an image on the left side
image = Image.open("Images/vecteezy_female-doctor-and-patient_.jpg")  # Replace with your actual image file
image = image.resize((900, 700))  # Resize image
photo = ImageTk.PhotoImage(image)

image_label = ctk.CTkLabel(root,text="", image=photo, fg_color="#52C1DD")  # Ensure image blends with background
image_label.place(x=50, y=200)

# Login function
# ✅ Modify Login Function to Pass Username to UserProfile
def login():
    username = user_entry.get().strip()
    password = user_pass.get().strip()

    with sqlite3.connect('pregnancy_data.db') as db:
        c = db.cursor()
        c.execute("SELECT username FROM pregnant_users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        if result:
            ms.showinfo("Message", "Login successful")
            
            call(["python", "UserProfile.py", username])  # Pass username
        else:
            ms.showerror("Oops!", "Username or Password is incorrect.")






# Create a frame for login elements
button_frame = ctk.CTkFrame(root, fg_color="#ffffff")  # Match the background
button_frame.place(relx=0.75, rely=0.5, anchor="center")  # Move to the right side and center vertically

# Load and place a logo above the username field
logo_image = Image.open("Images/logo3.png")  # Replace with your actual logo file
logo_image = logo_image.resize((500, 400))  # Resize logo
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ctk.CTkLabel(button_frame, text="", image=logo_photo, fg_color="#52C1DD")
logo_label.pack(pady=(0, 12))  # Add some space below the logo

# Username and password fields
user_entry = ctk.CTkEntry(button_frame, placeholder_text="Username", width=300, height=40)
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(button_frame, placeholder_text="Password", show="*", width=300, height=40)
user_pass.pack(pady=12, padx=10)

# Login button
button = ctk.CTkButton(button_frame, text='Login', command=login, fg_color="black", text_color="white", hover_color="#007acc", width=300, height=40)
button.pack(pady=(20, 12), padx=10)  # Increased top padding only

# Remember Me checkbox
#checkbox = ctk.CTkCheckBox(button_frame, text='Remember Me')
#checkbox.pack(pady=12, padx=10)

# Register label with clickable link
def register():
    call(["python", "user_register.py"])

register_label = ctk.CTkLabel(button_frame, text="Not a user? Register here", text_color="#007acc", cursor="hand2")
register_label.pack(pady=(10,30))
register_label.bind("<Button-1>", lambda e: register())

# Run the Tkinter event loop
root.mainloop()
