import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from subprocess import call

# Initialize Main Window
ctk.set_appearance_mode("light")  # Light mode
root = ctk.CTk()
root.title("Pregnancy Care System")
root.geometry("1920x1080")
root.configure(bg="white")  # Simple and professional background

# =================== CONTACT US SECTION ===================
contact_frame = ctk.CTkFrame(root, fg_color="white")
contact_frame.pack(fill="x", pady=(5, 0))

contact_label = ctk.CTkLabel(
    contact_frame,
    text="📍 Contact Us: Email - pregnancycaresystem@gmail.com  |  Phone - +91 9812312312",
    font=("Montserrat", 14, "bold"),
    text_color="black"
)
contact_label.pack()

# =================== HEADER SECTION ===================
header_label = ctk.CTkLabel(
    root, text="Welcome to Pregnancy Care System !",
    font=("Montserrat", 40, "bold"), text_color="black",
    height=80
)
header_label.pack(pady=(10, 10))

sub_label = ctk.CTkLabel(
    root, text="ML-powered early detection and health assessment \nfor expecting mothers and newborns.",
    font=("Montserrat", 25), text_color="gray"
)
sub_label.pack()

# =================== CONTENT AREA ===================
content_frame = ctk.CTkFrame(root, fg_color="white")
content_frame.pack(fill="both", expand=True, padx=100, pady=10)

# Use grid layout for side-by-side structure
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)

# -------- LEFT SECTION (Image) --------
image = Image.open("Images/—Pngtree—pregnant woman in white dress_15934595.jpg").resize((500, 550))  
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(content_frame, image=photo, bg="white")
image_label.grid(row=0, column=1, padx=90, pady=30, sticky="w")  # Adjusted padding to avoid overlap

# -------- RIGHT SECTION (Information) --------
info_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=15)
info_frame.grid(row=0, column=0, padx=150, pady=50, sticky="nw")  # Proper spacing

# Heading
info_heading = ctk.CTkLabel(info_frame, text="Smart Maternity Care: Predict Risks & Stay Healthy!", font=("Montserrat", 20, "bold"), text_color="black")
info_heading.pack()

# Description Text
info_text = """
The ML-Driven Pregnancy Care System is an intelligent healthcare solution designed to predict risk levels and potential diseases during pregnancy. Using Machine Learning (ML) algorithms, the system analyzes maternal health data to assess risk factors, enabling early intervention and better prenatal care.

"""
info_label = ctk.CTkLabel(info_frame, text=info_text, font=("Montserrat", 16), text_color="#AE4800", wraplength=500, justify="center")
info_label.pack(pady=(10, 0))

# =================== GET STARTED BUTTON ===================
def get_started():
    call(["python", "userAdmin.py"])  # Modify this to the actual main system file

get_started_btn = ctk.CTkButton(
    root, text="Get Started", command=get_started,
    font=("Montserrat", 18, "bold"), fg_color="black", text_color="white",
    hover_color="gray", width=250, height=60, corner_radius=10
)
get_started_btn.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
