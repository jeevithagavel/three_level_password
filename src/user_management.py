import sys
import os
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import bcrypt

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import db_config

def get_db_connection():
    return mysql.connector.connect(**db_config)

# 1st Level: Username and Password Authentication
def add_user(username, password, email):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("USE auth_db")
    
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                   (username, hashed_password, email))
    
    conn.commit()
    cursor.close()
    conn.close()

def user_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("USE auth_db")
    
    cursor.execute("SELECT 1 FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    exists = result is not None
    cursor.close()
    conn.close()
    
    return exists

def get_user_email(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("USE auth_db")
    
    cursor.execute("SELECT email FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    email = result[0] if result else None
    cursor.close()
    conn.close()
    
    return email


def check_password(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("USE auth_db")
    
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    stored_hashed_password = result[0] if result else None
    cursor.close()
    conn.close()
    
    if stored_hashed_password:
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
    return False


# 2nd Level: OTP (One-Time Password) Authentication
def send_otp_email(email, otp):
    from_address = "sathishvijay14@gmail.com"  # Replace with your email
    to_address = email
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server details
        server.starttls()
        server.login("sathishvijay14@gmail.com", "buefifjscyynnkfq")  # Replace with your email and password
        server.sendmail(from_address, to_address, msg.as_string())

def verify_otp(user_otp, correct_otp):
    """Verify the OTP entered by the user."""
    return user_otp == correct_otp

# 3rd Level: Image Sequence-Based Authentication
def image_sequence_correct(user_sequence):
    correct_sequence = "123"  # This should be the correct sequence for your images
    return user_sequence == correct_sequence

# Complete Authentication Workflow
def authenticate_user(username, password, user_otp, user_image_sequence):
    """
    Full authentication workflow:
    1. Check username and password.
    2. Send and verify OTP.
    3. Check image sequence.
    """
    if not user_exists(username):
        return "User does not exist."

    if not check_password(username, password):
        return "Incorrect password."

    # Get the user's email
    email = get_user_email(username)
    if not email:
        return "Email not found."

    # Generate OTP (this could be a more secure implementation)
    correct_otp = "123456"  # In production, generate a random OTP and send it via email
    send_otp_email(email, correct_otp)

    if not verify_otp(user_otp, correct_otp):
        return "OTP verification failed."

    if not image_sequence_correct(user_image_sequence):
        return "Image sequence verification failed."

    return "Authentication successful!"

# Main code to run the authentication
# if __name__ == "__main__":
#     # Example user input
#     username = input("Enter username: ")
#     password = input("Enter password: ")
#     user_otp = input("Enter the OTP sent to your email: ")
#     user_image_sequence = input("Enter the image sequence (e.g., 123): ")
    
#     result = authenticate_user(username, password, user_otp, user_image_sequence)
#     print(result)
