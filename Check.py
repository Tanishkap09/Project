import tkinter as tk
from PIL import Image, ImageTk
import riskdetector  
from subprocess import call  
import sys  # Import sys to get the passed username

def Train(username):
    root = tk.Tk()
    root.title("Maternity Risk Detection")
    root.configure(background="purple")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")

    # Background Image
    image = Image.open('Images/2.jpg').resize((w, h))
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)

    # Variables
    user_name_var = tk.StringVar(value=username)  # Pre-fill username
    age_var = tk.IntVar()
    SystolicBP_var = tk.IntVar()
    DiastolicBP_var = tk.IntVar()
    BS_var = tk.DoubleVar()
    BodyTemp_var = tk.IntVar()
    HeartRate_var = tk.IntVar()

    # Valid Ranges for Input
    input_ranges = {
        "Username": "Required",
        "Age": "18 - 100",
        "SystolicBP": "90 - 180 mmHg",
        "DiastolicBP": "60 - 120 mmHg",
        "BS": "70 - 140 mg/dL",
        "BodyTemp": "95 - 105 °F",
        "HeartRate": "50 - 150 bpm"
    }

    # Centered Container for Input Form
    container = tk.Frame(root, bg="white", padx=40, pady=40)
    container.place(relx=0.5, rely=0.5, anchor="center")

    # Heading
    tk.Label(container, text="Maternity Risk Detection", font=("Arial", 28, "bold"), bg="white", fg="black").grid(row=0, column=0, columnspan=3, pady=20)

    # Column Headers
    tk.Label(container, text="Input Fields", font=("Arial", 18, "bold"), bg="white").grid(row=1, column=0, padx=20, pady=10, sticky="w")
    tk.Label(container, text="Enter Value", font=("Arial", 18, "bold"), bg="white").grid(row=1, column=1, padx=20, pady=10, sticky="w")
    tk.Label(container, text="Normal Range", font=("Arial", 18, "bold"), bg="white", fg="red").grid(row=1, column=2, padx=20, pady=10, sticky="w")

    # Input Fields & Normal Ranges
    labels = ["Username", "Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]
    variables = [user_name_var, age_var, SystolicBP_var, DiastolicBP_var, BS_var, BodyTemp_var, HeartRate_var]

    for i, (label, var) in enumerate(zip(labels, variables)):
        tk.Label(container, text=label, font=('Arial', 16), bg="white").grid(row=i + 2, column=0, padx=20, pady=10, sticky="w")
        
        if label == "Username":
            tk.Entry(container, font=("Arial", 16), width=20, textvariable=var, state="readonly").grid(row=i + 2, column=1, padx=20, pady=10)  # User can't edit
        else:
            tk.Entry(container, font=("Arial", 16), width=20, textvariable=var).grid(row=i + 2, column=1, padx=20, pady=10)

        tk.Label(container, text=input_ranges[label], font=('Arial', 16, 'bold'), bg="white", fg="red").grid(row=i + 2, column=2, padx=20, pady=10, sticky="w")

    # Label to Display Risk Level
    risk_label = tk.Label(container, text="", background="white", font=('Arial', 20, 'bold'), width=40)
    risk_label.grid(row=len(labels) + 3, column=0, columnspan=3, pady=20)

    # Function to Get Data and Call External Detect Function
    def detect_and_display():
        e1, e2, e3, e4, e5, e6 = age_var.get(), SystolicBP_var.get(), DiastolicBP_var.get(), BS_var.get()/18, BodyTemp_var.get(), HeartRate_var.get()
        user_name = user_name_var.get().strip()

        if not user_name:
            risk_label.config(text="Error: Username Required", background="yellow", foreground="black")
            return

        # Call Detect function and store risk level
        risk_text, bg_color, fg_color = riskdetector.Detect_risk(e1, e2, e3, e4, e5, e6, user_name)

        # Update label on the main UI
        risk_label.config(text=risk_text, background=bg_color, foreground=fg_color)

    # Function to Navigate to Next Page
    def log():
        root.destroy()
        call(["python", "di_check.py",user_name_var.get()])  # Change 'di_check.py' to your actual next page filename

    # Submit Button (Detect Risk Level)
    tk.Button(container, text="Submit", command=detect_and_display, font=('Arial', 18, 'bold'), bg="green", fg="white", width=12).grid(row=len(labels) + 4, column=0, pady=20)

    # Next Button (Navigates to Next Page)
    tk.Button(container, text="Next", command=log, font=('Arial', 18, 'bold'), bg="blue", fg="white", width=12).grid(row=len(labels) + 4, column=2, pady=20)

    root.mainloop()

# Run the program only if username is passed
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        Train(username)
    else:
        print("❌ Error: No username provided!")
