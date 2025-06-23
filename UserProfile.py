import tkinter as tk
import customtkinter as ctk
import sqlite3
from tkinter import messagebox as ms
from subprocess import call
import sys  
import datetime

class UserProfile(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("User Profile")
        self.geometry("1920x1080")
        self.state("zoomed")  # Open Maximized
        self.configure(bg="#52C1DD")  
        self.username = username

        # Header Label
        ctk.CTkLabel(
            self, text="User Profile", font=("Arial", 30, 'bold'),
            fg_color="#007acc", text_color="white", height=60, corner_radius=10
        ).pack(fill="x", pady=10)

        # Fetch User Data
        self.user_data = self.fetch_user_data()
        if not self.user_data:
            ms.showerror("Error", "User data not found!")
            self.destroy()
            return

        # 🎯 **Main Profile Frame**
        self.info_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15, width=900, height=700)
        self.info_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Section Titles
        self.create_section_title("👤 Personal Information", 0, 0)
        self.create_section_title("📞 Contact Details", 0, 2)
        self.create_section_title("🏥 Health Information", 4, 1)  

        # 🎯 **Store User Details**
        self.details = {
            "Full Name": self.user_data[0],
            "Age": self.user_data[4],  
        }
        
        self.contact_details = {
            "Email": self.user_data[2],
            "Phone": self.user_data[3],
            "Address": self.user_data[1]
        }

        dop = self.user_data[5]
        trimester = self.calculate_trimester(dop)
        edd = self.calculate_edd(dop)
        
        self.health_info = {
            "Risk Level": self.user_data[8],
            "Disease Status": self.user_data[9],
            "Date of Pregnancy": dop,
            "Current Trimester": trimester,
            "Expected Delivery Date": edd
        }


        self.labels = {}
        self.entries = {}

        # 🚀 **Personal Details (Left Column)**
        row = 1
        for key, value in self.details.items():
            ctk.CTkLabel(self.info_frame, text=key, font=("Arial", 18, "bold"), text_color="black").grid(row=row, column=0, padx=40, pady=10, sticky="w")
            label = ctk.CTkLabel(self.info_frame, text=value, font=("Arial", 18), text_color="black")
            label.grid(row=row, column=1, padx=40, pady=10, sticky="w")
            self.labels[key] = label
            row += 1
        
        # 📞 **Contact Details (Right Column)**
        row = 1
        for key, value in self.contact_details.items():
            ctk.CTkLabel(self.info_frame, text=key, font=("Arial", 18, "bold"), text_color="black").grid(row=row, column=2, padx=40, pady=10, sticky="w")
            label = ctk.CTkLabel(self.info_frame, text=value, font=("Arial", 18), text_color="black")
            label.grid(row=row, column=3, padx=40, pady=10, sticky="w")
            self.labels[key] = label
            row += 1

        # 🏥 **Health Information (Middle Row)**
        row = 5  
        for key, value in self.health_info.items():
            ctk.CTkLabel(self.info_frame, text=key, font=("Arial", 18, "bold"), text_color="#007acc").grid(row=row, column=1, padx=40, pady=10, sticky="w")
            label = ctk.CTkLabel(self.info_frame, text=value, font=("Arial", 18), text_color="black")
            label.grid(row=row, column=2, padx=40, pady=10, sticky="w")
            self.labels[key] = label
            row += 1


        # 🚀 **Button Frame**
        button_frame = ctk.CTkFrame(self.info_frame, fg_color="white")
        button_frame.grid(row=row + 1, column=0, columnspan=4, pady=40)

        # ✅ **Buttons**
        self.edit_button = ctk.CTkButton(button_frame, text='✏️ Edit Profile', command=self.enable_editing, fg_color="black", text_color="white", hover_color="#007acc", width=220, height=50)
        self.edit_button.pack(side="left", padx=15)
        
        self.refresh_button = ctk.CTkButton(button_frame, text='🔄 Refresh', command=self.reload_profile, fg_color="orange", text_color="white", hover_color="#ff9800", width=220, height=50)
        self.refresh_button.pack(side="left", padx=15)

        self.check_health_button = ctk.CTkButton(button_frame, text='🩺 Check Health Status', command=self.check_health, fg_color="blue", text_color="white", hover_color="#0056b3", width=240, height=50)
        self.check_health_button.pack(side="left", padx=15)

        self.save_button = ctk.CTkButton(button_frame, text='💾 Save Changes', command=self.update_profile, fg_color="green", text_color="white", hover_color="#28a745", width=220, height=50)
        self.save_button.pack(side="left", padx=15)
        self.save_button.pack_forget()  
        
        self.diet_button = ctk.CTkButton(
            button_frame,
            text='🥗 View Diet Plans',
            command=self.open_diet_plan,
            fg_color="#4CAF50",
            text_color="white",
            hover_color="#388E3C",
            width=220,
            height=50
        )
        self.diet_button.pack(side="left", padx=15)

        self.treatment_button = ctk.CTkButton(
            button_frame,
            text='💊 Treatment Suggestions',
            command=self.open_treatment_page,
            fg_color="#9C27B0",
            text_color="white",
            hover_color="#6A1B9A",
            width=240,
            height=50
        )
        self.treatment_button.pack(side="left", padx=15)

        self.logout_button = ctk.CTkButton(button_frame, text='🚪 Logout', command=self.logout, fg_color="red", text_color="white", hover_color="#b22222", width=220, height=50)
        self.logout_button.pack(side="left", padx=15)

    def create_section_title(self, text, row, col):
        """Creates a section title in the profile page with more spacing."""
        ctk.CTkLabel(self.info_frame, text=text, font=("Arial", 22, "bold"), text_color="#007acc").grid(row=row, column=col, columnspan=2, pady=(20, 10))

    def fetch_user_data(self):
        """Fetch user details from the database based on the logged-in username"""
        with sqlite3.connect('pregnancy_data.db') as db:
            cursor = db.cursor()
            cursor.execute("""
    SELECT fullname, address, email, cntno, age, dop, username, password, risklvl, disease
    FROM pregnant_users WHERE username = ?
""", (self.username,))
            return cursor.fetchone()
    
    def calculate_trimester(self, dop_str):
        try:
            dop = datetime.datetime.strptime(dop_str, "%Y-%m-%d").date()
            today = datetime.date.today()
            weeks_pregnant = (today - dop).days // 7
    
            if weeks_pregnant < 13:
                return "First Trimester"
            elif 13 <= weeks_pregnant < 27:
                return "Second Trimester"
            elif 27 <= weeks_pregnant <= 42:
                return "Third Trimester"
            else:
                return "Beyond Term"
        except Exception as e:
            return "Invalid Date"
    
    def calculate_edd(self, dop_str):
        try:
            dop = datetime.datetime.strptime(dop_str, "%Y-%m-%d").date()
            edd = dop + datetime.timedelta(days=280)
            return edd.strftime("%Y-%m-%d")
        except Exception:
            return "Invalid Date"

    
    def enable_editing(self):
        """Switch labels to entry fields for editing"""
        self.edit_button.pack_forget()  
        self.save_button.pack(side="left", padx=15)  

        for key in self.details.keys() | self.contact_details.keys():  
            old_text = self.labels[key].cget("text")
            entry = ctk.CTkEntry(self.info_frame, width=320, font=("Arial", 16))
            entry.insert(0, old_text)
            entry.grid(row=list(self.details.keys()).index(key) + 1 if key in self.details else list(self.contact_details.keys()).index(key) + 1, column=1 if key in self.details else 3, padx=40, pady=10, sticky="w")
            self.labels[key].grid_remove()  
            self.entries[key] = entry  
            
    def update_profile(self):
        """Update user profile information in the database"""
        new_values = {key: self.entries[key].get().strip() for key in self.entries}

        if not new_values["Full Name"] or not new_values["Email"] or not new_values["Phone"].isdigit() or not new_values["Age"].isdigit():
            ms.showerror("Error", "Invalid input. Please enter valid details.")
            return

        with sqlite3.connect('pregnancy_data.db') as db:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE pregnant_users SET fullname = ?, email = ?, cntno = ?, address = ?, age = ? WHERE username = ?
            """, (new_values["Full Name"], new_values["Email"], new_values["Phone"], new_values["Address"], new_values["Age"], self.username))
            db.commit()

        ms.showinfo("Success", "Profile updated successfully!")
        self.reload_profile()  
    
    def open_diet_plan(self):
        """Redirect to diet plan page with current trimester."""
        current_trimester = self.calculate_trimester(self.user_data[5])
        call(["python", "diet_plan.py", current_trimester])
        
    def open_treatment_page(self):
        """Redirect to treatment suggestions page with disease and risk level."""
        disease = self.user_data[9]
        risk = self.user_data[8]
        call(["python", "treatment_suggestions.py", disease, risk])

    
    def check_health(self):
        """Redirect user to the risk level & disease detection page"""
        ms.showinfo("Health Check", "Redirecting to Risk Level & Disease Check...")
        call(["python", "Check.py",self.username])  

    def reload_profile(self):
        """Refresh the profile page with updated details"""
        self.destroy()
        app = UserProfile(self.username)
        app.mainloop()

    def logout(self):
        """Destroy the user profile and return to login page"""
        self.destroy()
        #call(["python", "Login.py"])  

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        app = UserProfile(username)
        app.mainloop()
