import customtkinter as ctk
import sqlite3
from tkinter import ttk, messagebox
from subprocess import call
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from reportlab.lib import colors


class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Panel - User Health Data")
        self.geometry("1920x1080")
        self.configure(bg="#52C1DD")

        # Header
        header_label = ctk.CTkLabel(
            self,
            text="Admin Panel - User Health Status",
            font=("Arial", 26, 'bold'),
            fg_color="#007acc",
            text_color="white",
            height=50,
            corner_radius=10
        )
        header_label.pack(fill="x")

        # Table Container Frame
        table_container = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=2, border_color="black")
        table_container.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.7)

        # Table (Treeview)
        self.tree = ttk.Treeview(
    table_container,
    columns=("Full Name", "Age", "Contact Number", "Date of Pregnancy", "EDD", "Risk Level", "Disease Status"),
    show="headings",
    height=15
)

        # Column Headings
        headings = ["Full Name", "Age", "Contact Number", "Date of Pregnancy", "EDD", "Risk Level", "Disease Status"]
        for col in headings:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=200 if col != "Full Name" else 250)


        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        font=("Arial", 12),
                        rowheight=30,
                        background="white",
                        fieldbackground="white")

        style.configure("Treeview.Heading",
                        font=("Arial", 14, "bold"),
                        background="blue",
                        foreground="white",
                        relief="ridge",
                        padding=5)

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        self.user_count_label = ctk.CTkLabel(self, text="Total Users: 0", font=("Arial", 16, "bold"))
        self.user_count_label.place(relx=0.5, rely=0.87, anchor="n")

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="bottom", pady=30)
        
        ctk.CTkButton(
            button_frame, text="Refresh Data", command=self.load_users,
            fg_color="green", text_color="white", width=200, height=40
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            button_frame, text="Registration Stats", command=self.open_registration_stats,
            fg_color="#ffffff", text_color="black", hover_color="#007acc", width=220, height=40
        ).pack(side="left", padx=20)
        
        generate_pdf_button = ctk.CTkButton(
        button_frame, text="Generate PDF", command=self.generate_user_pdf, 
        fg_color="blue", text_color="white", width=200, height=40
        )
        generate_pdf_button.pack(side="left", padx=20)

        
        ctk.CTkButton(
            button_frame, text="Logout", command=self.logout,
            fg_color="red", text_color="white", width=200, height=40
        ).pack(side="right", padx=20)

        
        # Summary Frame (Disease Count)
        self.summary_frame = ctk.CTkFrame(self, corner_radius=10)
        self.summary_frame.place(relx=0.5, rely=0.80, anchor="n")  # Adjust rely to move up/down
        # Disease Row Frame (Scrollable row of diseased users)
        #self.disease_row_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", fg_color="white", height=60)
        #self.disease_row_frame.pack(pady=(5, 15), fill="x", padx=20)

    
        self.load_users()
        
        

    def load_users(self):
        self.tree.delete(*self.tree.get_children())

        with sqlite3.connect("pregnancy_data.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    SELECT fullname, age, cntno, dop, risklvl, disease FROM PREGNANT_users
""")

            users = cursor.fetchall()

            if users:
                for user in users:
                    fullname, age, contact, dop_str, risklvl, disease = user

                    try:
                        dop = datetime.strptime(dop_str, "%Y-%m-%d")
                        edd = dop + timedelta(days=280)
                        dop_fmt = dop.strftime("%d-%b-%Y")
                        edd_fmt = edd.strftime("%d-%b-%Y")
                    except:
                        dop_fmt = "N/A"
                        edd_fmt = "N/A"

                    tag = "normal"
                    if risklvl == "Mid":
                        tag = "mid_risk"
                    elif risklvl == "High":
                        tag = "high_risk"
                    if disease.lower() != "healthy":
                        tag = "disease_detected"

                    self.tree.insert("", "end", values=(fullname, age, contact, dop_fmt, edd_fmt, risklvl, disease), tags=(tag,))

                self.tree.tag_configure("mid_risk", background="#FFEB3B", font=("Arial", 14, "bold"))
                self.tree.tag_configure("high_risk", background="#FF5733", font=("Arial", 14, "bold"))
                self.tree.tag_configure("disease_detected", background="#FFCDD2", font=("Arial", 14, "bold"))

                self.user_count_label.configure(text=f"Total Users: {len(users)}")
                # 🧼 Clear previous widgets
                for widget in self.summary_frame.winfo_children():
                    widget.destroy()
                
                # 🧮 Count users per disease (excluding Healthy)
                disease_counts = {}
                for user in users:
                    disease = user[5].strip()
                    if disease.lower() != "healthy":
                        disease_counts[disease] = disease_counts.get(disease, 0) + 1
                
                # 🎨 Display summary as horizontal badges
                row = 0
                col = 0
                for disease, count in disease_counts.items():
                    color = "#D32F2F"  # Default red
                    if "anemia" in disease.lower(): color = "#FF9800"
                    elif "thalassemia" in disease.lower(): color = "#C2185B"
                    elif "thrombocytopenia" in disease.lower(): color = "#6A1B9A"
                
                    badge = ctk.CTkLabel(
                        self.summary_frame,
                        text=f"{disease}: {count}",
                        font=("Arial", 14, "bold"),
                        text_color="white",
                        fg_color=color,
                        corner_radius=8,
                        height=35,
                        width=160
                    )
                    badge.grid(row=row, column=col, padx=10, pady=5)
                    col += 1

                    
            else:
                messagebox.showinfo("Info", "No users found in the database.")
    
    def generate_user_pdf(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to generate PDF.")
            return
    
        user_data = self.tree.item(selected_item, "values")
        filename = f"{user_data[0].replace(' ', '_')}_profile.pdf"
    
        # Folder setup
        folder_path = "reports"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
    
        # PDF canvas
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
    
        # Header
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 60, "Pregnancy Care Report")
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(50, height - 70, width - 50, height - 70)
    
        timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 60, f"Generated on: {timestamp}")
    
        # Personal Information
        y = height - 110
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Personal Information")
        y -= 20
    
        c.setFont("Helvetica", 12)
        labels = ["Full Name", "Age", "Contact Number", "Date of Pregnancy", "EDD", "Risk Level", "Disease Status"]
        for label, value in zip(labels, user_data):
            c.drawString(70, y, f"{label}:")
            c.drawString(200, y, str(value))
            y -= 20
    
        # Get Risk Level and Disease Status
        risk = user_data[5].lower()
        disease = user_data[6].lower()
    
        # Doctor's Note Logic
        c.setFont("Helvetica-Bold", 14)
        y -= 20
        c.drawString(50, y, "Doctor's Note:")
        y -= 20
        c.setFont("Helvetica", 12)
    
        note_lines = []
    
        # Risk-based advice
        if "high" in risk:
            note_lines.append("This patient is classified as high-risk. Recommend frequent checkups and close fetal monitoring.")
        elif "moderate" in risk:
            note_lines.append("Moderate risk noted. Advise monthly visits and lifestyle monitoring.")
        elif "low" in risk:
            note_lines.append("Low-risk pregnancy. Regular antenatal care is sufficient.")
    
        # Disease-specific advice
        if "diabetes" in disease:
            note_lines.append("Monitor blood sugar regularly. Consider insulin therapy and a diabetic meal plan.")
        elif "anemia" in disease:
            note_lines.append("Recommend iron supplementation and folic acid. Monitor hemoglobin monthly.")
        elif "thalassemia" in disease:
            note_lines.append("Monitor iron overload and hemoglobin. Genetic counseling recommended.")
        elif "thrombocytopenia" in disease:
            note_lines.append("Platelet count monitoring required. Avoid invasive procedures without consultation.")
    
        for line in note_lines:
            c.drawString(70, y, f"- {line}")
            y -= 20
    
        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 30, "Confidential Report - For Medical Use Only")
    
        # Save PDF
        c.save()
        messagebox.showinfo("Success", f"PDF saved in '{folder_path}/' as {filename}")
    
    def open_registration_stats(self):
        call(["python", "registration_stats.py"])

    
    def logout(self):
        self.destroy()
        # call(["python", "Login.py"])

if __name__ == "__main__":
    app = AdminPanel()
    app.mainloop()
