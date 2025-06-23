# -*- coding: utf-8 -*-
import smtplib
import random
import string
from email.message import EmailMessage
import os



def send_admin_email(recipient_email, fname, user_name, security_code, password):
    """Send an email with credentials to the user."""
    
    sender_email = "pregnancycaresystem@gmail.com"  # Replace with your email
    sender_password = "dufx vlgu krrd sekt"  # Use App Password (not your regular password)
    

    # Create email message
    msg = EmailMessage()
    msg["Subject"] = "Your Account Credentials"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(f"Hello {fname},\n\nYour login credentials:\nUsername: {user_name}\nPassword: {password}\nSecurity Code: {security_code}\nPlease keep it safe!")

    # Sending email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        
def send_user_email(recipient_email, fname, user_name, password):
    """Send an email with credentials to the user."""
    
    sender_email = "pregnancycaresystem@gmail.com"  # Replace with your email
    sender_password = "dufx vlgu krrd sekt"  # Use App Password (not your regular password)
    

    # Create email message
    msg = EmailMessage()
    msg["Subject"] = "Your Account Credentials"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(f"Hello {fname},\n\nYour login credentials:\nUsername: {user_name}\nPassword: {password}\nPlease keep it safe!")

    # Sending email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_user_pdf(email_address, subject, body, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'pregnancycaresystem@gmail.com'
    msg['To'] = email_address
    msg.set_content(body)

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
        filename = os.path.basename(pdf_path)
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=filename)

    # Send Email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('pregnancycaresystem@gmail.com', 'dufx vlgu krrd sekt')  # Use App Password if using Gmail