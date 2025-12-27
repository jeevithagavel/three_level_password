import bcrypt
import random
import mysql.connector
from config.db_config import db_config  # Make sure to set up db_config.py
from getpass import getpass


# Get a MySQL database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Hash the password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


# Verify the password against the hashed value
def verify_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))


# Register a new user in the database
def register_user(username, password, image_sequence, email):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result:
            print("Username already exists. Please choose a different one.")
            return False
        
        # Hash the password before storing it
        hashed_password = hash_password(password)
        
        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO users (username, password, image_sequence, email)
            VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, image_sequence, email))
        
        conn.commit()
        print("User registered successfully!")
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
    finally:
        cursor.close()
        conn.close()


# Level 1 Authentication: Check the username and password
def level_one(username, input_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        stored_password = result[0]
        if verify_password(input_password, stored_password):
            return True
    return False


# Level 2 Authentication: Check the image sequence
def level_two(username, input_sequence):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_sequence FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        stored_sequence = result[0]
        if input_sequence == stored_sequence:
            return True
        else:
            print("Incorrect image sequence.")
    return False


# Level 3 Authentication: OTP verification
def level_three(user_otp, stored_otp):
    return user_otp == stored_otp


# Generate and send an OTP (for demonstration purposes, we print it)
def generate_and_send_otp(username):
    otp = random.randint(100000, 999999)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET otp=%s WHERE username=%s", (str(otp), username))
    conn.commit()

    cursor.execute("SELECT email FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        email = result[0]
        # For now, we will just print the OTP
        print(f"Sending OTP {otp} to {email}")
    
    cursor.close()
    conn.close()

    return otp


# Main Authentication Flow
def authenticate_user():
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    if level_one(username, password):
        print("Level 1 authentication successful!")

        image_sequence = input("Enter your image sequence: ")
        if level_two(username, image_sequence):
            print("Level 2 authentication successful!")

            otp = input("Do you want to receive OTP? (y/n): ")
            if otp.lower() == 'y':
                stored_otp = generate_and_send_otp(username)
                user_otp = input("Enter the OTP sent to your email: ")

                if level_three(user_otp, str(stored_otp)):
                    print("Level 3 authentication successful! Access granted.")
                else:
                    print("Level 3 authentication failed! Incorrect OTP.")
            else:
                print("OTP authentication skipped. Access granted without OTP.")
        else:
            print("Level 2 authentication failed! Incorrect image sequence.")
    else:
        print("Level 1 authentication failed! Invalid username or password.")


# Registration Flow
def registration_flow():
    username = input("Enter new username: ")
    password = getpass("Enter new password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        return

    image_sequence = input("Enter image sequence for Level 2 authentication: ")
    email = input("Enter email for OTP verification: ")

    if register_user(username, password, image_sequence, email):
        print("Registration successful. You can now log in.")


if __name__ == "__main__":
    choice = input("Do you want to (r)egister or (a)uthenticate? ").lower()
    if choice == 'r':
        registration_flow()
    elif choice == 'a':
        authenticate_user()
    else:
        print("Invalid choice. Please choose 'r' for registration or 'a' for authentication.")
