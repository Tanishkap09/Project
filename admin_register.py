# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import string
from tkinter import messagebox
import email_sender 

window = tk.Tk()
window.geometry("700x700")
window.title("ADMIN REGISTRATION FORM")
window.configure(background="white")

full_Name = tk.StringVar()
address = tk.StringVar()
user_Name = tk.StringVar()
email = tk.StringVar()
cnt_No = tk.StringVar()
gendr = tk.IntVar()
age = tk.StringVar()
password = tk.StringVar()
cnf_pass = tk.StringVar()
sec_code = tk.StringVar()

#random.randint(1, 1000)

# Database setup
db = sqlite3.connect('adminDb.db')
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "admin" (
	"Name"	TEXT NOT NULL,
	"Address"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Contact_number"	TEXT NOT NULL,
	"Gender"	TEXT NOT NULL,
	"Age"	INTEGER NOT NULL,
	"User_name"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL,
	"Security_code"	TEXT NOT NULL,
	PRIMARY KEY("Security_code")
)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "admin_verify" (
	"user_Name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"security_code"	TEXT NOT NULL,
	PRIMARY KEY("security_code")
)
""")
db.commit()

def generate_unique_sec_code(db_connection):
    
    def generate_sec_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    cursor = db_connection.cursor()

    while True:
        new_code = generate_sec_code()
        cursor.execute("SELECT COUNT(*) FROM admin_verify WHERE security_code = ?", (new_code,))
        if cursor.fetchone()[0] == 0:  # If not found in database
            return new_code  # Unique value found

# Example Usage:
conn = sqlite3.connect("adminDb.db")  # Connect to your database
unique_code = generate_unique_sec_code(conn)
sec_code = unique_code

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    if len(passwd) < 6 or len(passwd) > 20:
        return False
    if not any(char.isdigit() for char in passwd):
        return False
    if not any(char.isupper() for char in passwd):
        return False
    if not any(char.islower() for char in passwd):
        return False
    if not any(char in SpecialSym for char in passwd):
        return False
    return True

def send_credentials(email, fname, user_name, s_code, password):
    """Function to send email with credentials."""
    if email and fname:
        email_sender.send_admin_email(email, fname, user_name, s_code, password)  # Call function from email_sender.py
        messagebox.showinfo("Success", "Email sent successfully!")
    else:
        messagebox.showerror("Error", "Please enter both Name and Email.")


def insert():
    fname = full_Name.get().strip()
    addr = address.get().strip()
    un = user_Name.get().strip()
    Email = email.get().strip()
    mobile = cnt_No.get().strip()
    gender = gendr.get()
    Age = age.get().strip()
    pwd = password.get()
    cnpwd = cnf_pass.get()

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not fname or fname.isdigit():
        ms.showinfo("Message", "Please enter a valid name")
    elif not addr:
        ms.showinfo("Message", "Please enter an address")
    elif not Email or not re.search(regex, Email):
        ms.showinfo("Message", "Please enter a valid email")
    elif not mobile.isdigit() or len(mobile) != 10:
        ms.showinfo("Message", "Please enter a 10-digit mobile number")
    elif not Age.isdigit() or int(Age) <= 0 or int(Age) > 100:
        ms.showinfo("Message", "Please enter a valid age")
    elif not un:
        ms.showinfo("Message", "Please enter a username")
    elif not gender:
        ms.showinfo("Message", "Please select a gender")
    elif not pwd or not password_check(pwd):
        ms.showinfo("Message", "Password must contain at least 1 uppercase letter, 1 symbol, and 1 number")
    elif pwd != cnpwd:
        ms.showinfo("Message", "Password and Confirm Password must match")
    else:
        with sqlite3.connect('adminDb.db') as db:
            c = db.cursor()
            c.execute('SELECT * FROM admin WHERE user_name = ?', (un,))
            if c.fetchone():
                ms.showerror('Error!', 'Username taken. Try a different one.')
            else:
                c.execute(
                    'INSERT INTO admin(name, address, email, contact_number, gender, age, user_name , password, security_code) VALUES(?,?,?,?,?,?,?,?,?)',
                    (fname, addr, Email, mobile, gender, Age, un, pwd, sec_code))
                c.execute(
                    'INSERT INTO admin_verify(user_name, password, security_code) VALUES(?,?,?)',
                    (un, pwd, sec_code))
                db.commit()
                ms.showinfo('Success!', f'Account Created Successfully!\nYour Security Code is {sec_code}')
                

                send_credentials(Email, fname, un, sec_code, pwd)
                window.destroy()


image2 = Image.open('Images/2.jpg').resize((700, 700))
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0)

tk.Label(window, text="Create your account here!!", font=("Times new roman", 30, "bold"), bg="white").place(x=130, y=50)

def create_label(text, y):
    return tk.Label(window, text=text, width=12, font=("Times new roman", 15, "bold"), bg="snow").place(x=130, y=y)

def create_entry(var, y, show=None):
    return tk.Entry(window, textvar=var, width=20, font=('', 15), show=show).place(x=330, y=y)

create_label("Full Name:", 150)
create_entry(full_Name, 150)
create_label("Address:", 200)
create_entry(address, 200)
create_label("E-mail:", 250)
create_entry(email, 250)
create_label("Phone number:", 300)
create_entry(cnt_No, 300)
create_label("Gender:", 350)
tk.Radiobutton(window, text="Male", padx=5, width=5, bg="snow", font=("bold", 15), variable=gendr, value=1).place(x=330, y=350)
tk.Radiobutton(window, text="Female", padx=20, width=4, bg="snow", font=("bold", 15), variable=gendr, value=2).place(x=440, y=350)
create_label("Age:", 400)
create_entry(age, 400)
create_label("User Name:", 450)
create_entry(user_Name, 450)
create_label("Password:", 500)
create_entry(password, 500, show="*")
create_label("Confirm Password:", 550)
create_entry(cnf_pass, 550, show="*")

tk.Button(window, text="Register", bg="white", font=("", 20), fg="black", width=9, height=1, command=insert).place(x=260, y=620)
window.mainloop()
