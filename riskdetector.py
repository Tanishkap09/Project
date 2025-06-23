import sqlite3
from joblib import load

def Detect_risk(age, systolicBP, diastolicBP, bs, bodyTemp, heartRate, user_name):
    # Connect to Database
    conn = sqlite3.connect("pregnancy_data.db")
    cursor = conn.cursor()

    # Check if Username Exists
    cursor.execute("SELECT * FROM pregnant_users WHERE username = ?", (user_name,))
    user_data = cursor.fetchone()
    
    if not user_data:
        conn.close()
        return "Error: Invalid Username", "yellow", "black"  # Display Error Message
    
    # Load trained model
    try:
        model = load('model_train_data/random_forest.joblib')
        prediction = model.predict([[age, systolicBP, diastolicBP, bs, bodyTemp, heartRate]])[0]

        # Determine Risk Level
        if prediction == 0:
            risk_text, bg_color, fg_color = "High", "red", "white"
        elif prediction == 1:
            risk_text, bg_color, fg_color = "Mid", "orange", "white"
        else:
            risk_text, bg_color, fg_color = "Low", "green", "white"

        # Store Risk Level in Database
        cursor.execute("UPDATE pregnant_users SET risklvl = ? WHERE username = ?", (risk_text, user_name))
        conn.commit()

    except Exception as e:
        risk_text, bg_color, fg_color = "Error: Model Not Found", "yellow", "black"
        print(f"Error: {e}")

    conn.close()
    return risk_text, bg_color, fg_color

def Detect_disease(values, user_name):
    # Connect to Database
    conn = sqlite3.connect("pregnancy_data.db")
    cursor = conn.cursor()

    # Check if Username Exists
    cursor.execute("SELECT * FROM pregnant_users WHERE username = ?", (user_name,))
    user_data = cursor.fetchone()
    
    if not user_data:
        conn.close()
        return "Error: Invalid Username", "yellow", "black"  # Display Error Message
    
    # Load trained model
    try:
        model = load('model_train_data/svm1.joblib')
        prediction = model.predict([values])[0]

        # Determine Disease Detection Result
        disease_map = {
            0: ("Healthy", "green", "white"),
            1: ("Diabetes", "yellow", "black"),
            2: ("Anemia", "blue", "white"),
            3: ("Thalassemia", "violet", "white"),
            4: ("Thrombocytopenia", "red", "white")
        }

        result_text, bg_color, fg_color = disease_map.get(prediction, ("Unknown", "gray", "black"))

        # Store Detection Result in Database
        cursor.execute("UPDATE pregnant_users SET disease = ? WHERE username = ?", (result_text, user_name))
        conn.commit()

    except Exception as e:
        result_text, bg_color, fg_color = "Error: Model Not Found", "yellow", "black"
        print(f"Error: {e}")

    conn.close()
    return result_text, bg_color, fg_color