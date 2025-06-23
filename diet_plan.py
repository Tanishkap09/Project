import sys
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")

# Indian Diet Plan for Each Trimester
diet_plans = {
    "First Trimester": [
        "Focus on Folic Acid & Iron",
        "Why? Prevents neural tube defects, supports fetal development.",
        "1. Leafy greens (spinach, methi)",
        "2. Citrus fruits (oranges, mosambi)",
        "3. Whole grains (roti, daliya)",
        "4. Lentils and dals",
        "5. Dairy (milk, curd, paneer)",
        "6. Eggs",
        "7. Bananas",
        "8. Carrots and beets",
        "9. Amla (Indian gooseberry)",
        "10. Soaked almonds and walnuts",
        "Avoid: Junk food, raw papaya, excessive caffeine, too much salt"
    ],
    "Second Trimester": [
        "Focus on Calcium & Protein",
        "Why? Strengthens bones, supports muscle growth.",
        "1. Milk and curd",
        "2. Ragi (nachni) and bajra",
        "3. Chicken and fish (well-cooked)",
        "4. Boiled eggs",
        "5. Rajma and chole",
        "6. Palak (spinach) paneer",
        "7. Seasonal fruits (mango, guava, apple)",
        "8. Rice with ghee",
        "9. Dates and figs",
        "10. Buttermilk and coconut water",
        "Avoid: Excess salt, processed foods, sugary drinks"
    ],
    "Third Trimester": [
        "Focus on Energy & Omega-3",
        "Why? Supports baby’s brain growth and prepares for labor.",
        "1. Oats and porridge",
        "2. Boiled vegetables with ghee",
        "3. Methi and dill leaves",
        "4. Roasted chana",
        "5. Masoor dal",
        "6. Soft roti with sabzi",
        "7. Paneer bhurji",
        "8. Khichdi with moong dal",
        "9. Tender coconut water",
        "10. Seasonal fruits and soaked dry fruits",
        "Avoid: Fried food, excess tea/coffee, carbonated drinks"
    ]
}

def show_diet(trimester):
    root = ctk.CTk()
    root.title(f"{trimester} Diet Plan")
    root.geometry("900x700")
    root.configure(fg_color="white")

    ctk.CTkLabel(root, text=f"{trimester} Diet Plan", font=("Arial", 28, "bold"), text_color="black").pack(pady=20)

    if trimester in diet_plans:
        for item in diet_plans[trimester]:
            ctk.CTkLabel(root, text=item, font=("Arial", 18), text_color="#333").pack(anchor="w", padx=40, pady=5)
    else:
        ctk.CTkLabel(root, text="No plan available.", font=("Arial", 16), text_color="red").pack(pady=10)

    ctk.CTkButton(root, text="Close", command=root.destroy, width=120, height=40, fg_color="black", text_color="white", hover_color="#007acc").pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        trimester = sys.argv[1]
        show_diet(trimester)
    else:
        messagebox.showerror("Error", "No trimester provided.")
