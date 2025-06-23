import sys
import customtkinter as ctk

def get_treatment(disease, risk):
    suggestions = {
        "Healthy": "✅ You are healthy. Maintain prenatal care, nutrition, and regular checkups.",

        "Diabetes": """
🥗 Diet & Lifestyle:
• Follow a low glycemic diet.
• Eat frequent, small meals.
• Exercise (walking/yoga) regularly.

💊 Medicines:
• Metformin – Helps control blood sugar.
• Insulin – If blood sugar remains high.

**ONLY FOR REFERENCE**

🧴 Supplements:
• Multivitamin (with B-complex & folic acid)
• Chromium (only if prescribed)
• Omega-3 (DHA) – Brain development & inflammation control
        """,

        "Anemia": """
🍲 Diet:
• Eat iron-rich foods: spinach, jaggery, dates, lentils.

💊 Medicines:
• Ferrous Sulfate / Fumarate – Iron tablets.
• Folic Acid (5 mg) – RBC formation.
• Vitamin C – Boosts iron absorption.
• Vitamin B12 – Especially important for vegetarians.

**ONLY FOR REFERENCE**
        """,

        "Thalassemia": """
📌 Genetic condition – Requires monitoring.

💊 Supplements:
• Folic Acid (5 mg daily) – Boosts RBCs.
• Vitamin D & Calcium – Maintains bone health.

⚠️ Avoid iron unless prescribed (iron overload risk).
🩸 Severe cases may need blood transfusions during pregnancy.
        """,

        "Thrombocytopenia": """
🧬 Low platelet count – Needs caution.

💊 Medicines:
• Folic Acid – Helps in blood cell formation.
• Prednisolone – Used in low doses if necessary.
• Eltrombopag / Romiplostim – For chronic immune types (ITP).
• IVIG – Only in severe critical cases.

**ONLY FOR REFERENCE**

📌 Regular monitoring is essential.
        """,

        "Urinary Tract Infection": """
💧 Drink 2-3 liters of water daily.
🧼 Maintain hygiene.
💊 Antibiotics – Prescribed by OB-GYN after testing.
        """
    }

    risk_tips = {
        "Low": "🟢 Low Risk:\nMaintain a balanced diet, hydration, sleep, and prenatal care.",
        "Mid": "🟠 Mid Risk:\nIncrease rest, reduce stress, stay hydrated, and visit OB-GYN regularly.",
        "High": "🔴 High Risk:\nStrict monitoring needed. Follow a personalized plan, diet, and medication."
    }

    return suggestions.get(disease, "Consult your doctor for a proper diagnosis.") + "\n\n" + risk_tips.get(risk, "")

def show_treatment_window(disease, risk):
    app = ctk.CTk()
    app.title("Treatment Suggestions")
    app.geometry("900x600")
    ctk.set_appearance_mode("light")

    ctk.CTkLabel(app, text=f"🩺 Disease: {disease}", font=("Arial", 22, "bold"), text_color="black").pack(pady=(20, 5))
    ctk.CTkLabel(app, text=f"⚠️ Risk Level: {risk}", font=("Arial", 20), text_color="#007acc").pack(pady=5)

    suggestions = get_treatment(disease, risk)

    suggestion_box = ctk.CTkTextbox(app, wrap="word", font=("Arial", 16,"bold"), width=850, height=450)
    suggestion_box.insert("0.0", suggestions)
    suggestion_box.configure(state="disabled")
    suggestion_box.pack(pady=20, padx=20)

    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        disease = sys.argv[1]
        risk = sys.argv[2]
        show_treatment_window(disease, risk)
    else:
        print("⚠️ Disease or risk level not provided.")
