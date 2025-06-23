# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:39:04 2025

@author: parge
"""

import tkinter as tk
import customtkinter as ctk
import sqlite3
from datetime import datetime, timedelta
from collections import Counter

class RegistrationStats(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("User Registration Statistics")
        self.geometry("600x800")
        #self.configure(bg="white")

        ctk.CTkLabel(
            self, text="📊 User Registration Stats", font=("Arial", 26, "bold"),
            text_color="white"
        ).pack(pady=20)

        self.stats_frame = ctk.CTkFrame(self, corner_radius=10)
        self.stats_frame.pack(pady=20, fill="both", expand=True)

        self.load_stats()

    def load_stats(self):
        today = datetime.today()
        this_week_start = today - timedelta(days=today.weekday())
        current_month = today.month
        current_year = today.year

        # Counters
        today_count = 0
        week_count = 0
        month_count = 0
        past_months = Counter()

        with sqlite3.connect("pregnancy_data.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT reg_date FROM PREGNANT_users")
            rows = cursor.fetchall()

            for (reg_date_str,) in rows:
                try:
                    reg_date = datetime.strptime(reg_date_str, "%d-%m-%Y")
                except ValueError:
                    continue  # Skip invalid formats

                if reg_date.date() == today.date():
                    today_count += 1
                if reg_date >= this_week_start:
                    week_count += 1
                if reg_date.month == current_month and reg_date.year == current_year:
                    month_count += 1
                elif reg_date < datetime(current_year, current_month, 1):
                    key = reg_date.strftime("%b %Y")  # e.g., "Mar 2024"
                    past_months[key] += 1

        # Display Results
        stats = [
            ("Registered Today", today_count),
            ("Registered This Week", week_count),
            ("Registered This Month", month_count),
        ]

        for text, value in stats:
            ctk.CTkLabel(self.stats_frame, text=f"{text}: {value}", font=("Arial", 18), text_color="white").pack(pady=8)

        if past_months:
            ctk.CTkLabel(self.stats_frame, text="Past Months:", font=("Arial", 20, "bold"), text_color="#007acc").pack(pady=(20, 10))
            for month, count in past_months.items():
                ctk.CTkLabel(self.stats_frame, text=f"{month}: {count} user(s)", font=("Arial", 16), text_color="gray").pack()

if __name__ == "__main__":
    app = RegistrationStats()
    app.mainloop()
