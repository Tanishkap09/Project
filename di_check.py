import tkinter as tk
from PIL import Image, ImageTk
from riskdetector import Detect_disease  # Import the separate function
import sys  # Required to accept username from UserProfile.py
from subprocess import call  # To navigate back to UserProfile

# Example min-max values for normalization with units
min_max_dict = {
    "Glucose (mg/dL)": (70, 140),
    "Cholesterol (mg/dL)": (125, 300),
    "Hemoglobin (g/dL)": (5.5, 18),
    "Platelets (per µL)": (150000, 450000),
    "White Blood Cells (per µL)": (4000, 11000),
    "Red Blood Cells (million/µL)": (3.5, 6.0),
    "Insulin (µU/mL)": (2, 30),
    "BMI (kg/m²)": (15, 40),
    "Systolic BP (mmHg)": (90, 180),
    "Diastolic BP (mmHg)": (60, 120),
    "HbA1c (%)": (4, 6),
    "Heart Rate (bpm)": (50, 150),
    "Troponin (ng/mL)": (0, 0.04),
    "C-reactive Protein (mg/L)": (0, 3)
}

def normalize_input(values):
    return [(user_value - X_min) / (X_max - X_min) for (X_min, X_max), user_value in zip(min_max_dict.values(), values)]

def denormalize_output(normalized_values):
    return [(norm_value * (X_max - X_min)) + X_min for (X_min, X_max), norm_value in zip(min_max_dict.values(), normalized_values)]

def Train(username):
    root = tk.Tk()
    root.title("Disease Detection System")
    root.state("zoomed")  # Set to full screen
    root.configure(background="purple")

    # Background Image
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    image = Image.open('Images/di.jpg').resize((w, h))
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)

    # Variables
    variables = [tk.DoubleVar() for _ in range(14)]
    user_name_var = tk.StringVar(value=username)  # Pre-filled with username

    # Centered Container
    container = tk.Frame(root, bg="white", padx=20, pady=20)
    container.place(relx=0.5, rely=0.5, anchor="center")

    # Heading
    tk.Label(container, text="Disease Detection System", font=("Arial", 22, "bold"), bg="white", fg="black").grid(row=0, column=0, columnspan=3, pady=10)

    # Column Headers
    tk.Label(container, text="Input Fields", font=("Arial", 14, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(container, text="Enter Value", font=("Arial", 14, "bold"), bg="white").grid(row=1, column=1, padx=10, pady=5, sticky="w")
    tk.Label(container, text="Normal Range", font=("Arial", 14, "bold"), bg="white", fg="red").grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # Input Fields & Normal Ranges
    labels = list(min_max_dict.keys())
    for i, (label, var) in enumerate(zip(labels, variables)):
        tk.Label(container, text=label, font=('Arial', 12), bg="white").grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(container, font=("Arial", 12), width=15, textvariable=var)
        entry.grid(row=i + 2, column=1, padx=10, pady=5)
        tk.Label(container, text=f"{min_max_dict[label][0]} - {min_max_dict[label][1]}", font=('Arial', 12, 'bold'), bg="white", fg="red").grid(row=i + 2, column=2, padx=10, pady=5, sticky="w")

    # Username Input (Read-Only)
    tk.Label(container, text="Username", font=('Arial', 14, 'bold'), bg="white").grid(row=len(labels) + 2, column=0, pady=5, sticky="w")
    user_entry = tk.Entry(container, font=("Arial", 12), width=15, textvariable=user_name_var, state="readonly")
    user_entry.grid(row=len(labels) + 2, column=1, pady=5)

    # Result Label
    result_label = tk.Label(container, text="", background="white", font=('Arial', 14, 'bold'), width=30)
    result_label.grid(row=len(labels) + 3, column=0, columnspan=3, pady=10)

    # Function to Get Inputs, Normalize, and Call Detect
    def submit():
        values = [var.get() for var in variables]
        print("Original Input Values:", values)

        normalized_values = normalize_input(values)
        print("Normalized Values:", normalized_values)

        denormalized_values = denormalize_output(normalized_values)
        print("Denormalized Values (should match input):", denormalized_values)

        user_name = user_entry.get().strip()
        result_text, bg_color, fg_color = Detect_disease(normalized_values, user_name)
        result_label.config(text=result_text, background=bg_color, foreground=fg_color)

    # Function to return to User Profile
    def go_back():
        root.destroy()
       # call(["python", "UserProfile.py", username])  # Redirect to User Profile with username

    # Buttons
    tk.Button(container, text="Submit", command=submit, font=('Arial', 14, 'bold'), bg="green", fg="white", width=12).grid(row=len(labels) + 4, column=0, pady=10)
    
    tk.Button(container, text="Done", command=go_back, font=('Arial', 14, 'bold'), bg="blue", fg="white", width=12).grid(row=len(labels) + 4, column=2, pady=10)

    root.mainloop()

# Run only if username is passed
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]  # Accept username from UserProfile.py
        Train(username)
    else:
        print("❌ Error: No username provided!")
