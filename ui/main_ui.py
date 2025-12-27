import tkinter as tk
from tkinter import messagebox
import random
from src.user_management import add_user, user_exists, send_otp_email, verify_otp, check_password, get_user_email

class AuthenticationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication App")
        self.root.geometry("300x400")

        # Initialize necessary attributes
        self.username = None
        self.password = None
        self.email = None
        self.otp = None

        # Set up the login frame
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username")
        self.username_label.grid(row=0, column=0, padx=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10)

        self.password_label = tk.Label(self.login_frame, text="Password")
        self.password_label.grid(row=1, column=0, padx=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.process_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.show_registration)
        self.register_button.grid(row=3, column=0, columnspan=2)

        # Set up the registration frame
        self.registration_frame = tk.Frame(root)
        self.registration_frame.pack(pady=20)
        self.registration_frame.pack_forget()

        self.register_username_label = tk.Label(self.registration_frame, text="Username")
        self.register_username_label.grid(row=0, column=0, padx=10)
        self.register_username_entry = tk.Entry(self.registration_frame)
        self.register_username_entry.grid(row=0, column=1, padx=10)

        self.register_password_label = tk.Label(self.registration_frame, text="Password")
        self.register_password_label.grid(row=1, column=0, padx=10)
        self.register_password_entry = tk.Entry(self.registration_frame, show="*")
        self.register_password_entry.grid(row=1, column=1, padx=10)

        self.confirm_password_label = tk.Label(self.registration_frame, text="Confirm Password")
        self.confirm_password_label.grid(row=2, column=0, padx=10)
        self.confirm_password_entry = tk.Entry(self.registration_frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10)

        self.register_next_button = tk.Button(self.registration_frame, text="Next", command=self.register_user)
        self.register_next_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.register_back_button = tk.Button(self.registration_frame, text="Back to Login", command=self.show_login)
        self.register_back_button.grid(row=4, column=0, columnspan=2)

        # Set up the email verification frame
        self.email_verification_frame = tk.Frame(root)
        self.email_verification_frame.pack(pady=20)
        self.email_verification_frame.pack_forget()

        self.register_email_label = tk.Label(self.email_verification_frame, text="Email")
        self.register_email_label.grid(row=0, column=0, padx=10)
        self.register_email_entry = tk.Entry(self.email_verification_frame)
        self.register_email_entry.grid(row=0, column=1, padx=10)

        self.email_verify_button = tk.Button(self.email_verification_frame, text="Send OTP", command=self.send_otp)
        self.email_verify_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.email_back_button = tk.Button(self.email_verification_frame, text="Back", command=self.show_registration)
        self.email_back_button.grid(row=2, column=0, columnspan=2)

        # Set up the email OTP verification frame
        self.email_otp_verification_frame = tk.Frame(root)
        self.email_otp_verification_frame.pack(pady=20)
        self.email_otp_verification_frame.pack_forget()

        self.email_otp_label = tk.Label(self.email_otp_verification_frame, text="Enter OTP")
        self.email_otp_label.grid(row=0, column=0, padx=10)
        self.email_otp_entry = tk.Entry(self.email_otp_verification_frame)
        self.email_otp_entry.grid(row=0, column=1, padx=10)

        self.email_otp_verify_button = tk.Button(self.email_otp_verification_frame, text="Verify OTP", command=self.verify_registration_otp)
        self.email_otp_verify_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.email_otp_back_button = tk.Button(self.email_otp_verification_frame, text="Back", command=self.show_email_verification)
        self.email_otp_back_button.grid(row=2, column=0, columnspan=2)

    def show_login(self):
        self.registration_frame.pack_forget()
        self.email_verification_frame.pack_forget()
        self.email_otp_verification_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def show_registration(self):
        self.login_frame.pack_forget()
        self.email_verification_frame.pack_forget()
        self.email_otp_verification_frame.pack_forget()
        self.registration_frame.pack(pady=20)

    def show_email_verification(self):
        self.registration_frame.pack_forget()
        self.email_otp_verification_frame.pack_forget()
        self.email_verification_frame.pack(pady=20)

    def show_otp_verification(self):
        self.email_verification_frame.pack_forget()
        self.email_otp_verification_frame.pack(pady=20)

    def process_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required.")
            return

        if user_exists(username):
            if check_password(username, password):
                email = get_user_email(username)
                if email:
                    self.username = username
                    self.password = password
                    self.email = email
                    self.otp = random.randint(100000, 999999)

                    send_otp_email(email, self.otp)
                    messagebox.showinfo("Info", "OTP sent to your email.")
                    self.show_otp_verification()
                    self.email_otp_verify_button.config(command=self.verify_login_otp)
                else:
                    messagebox.showerror("Error", "User email not found.")
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "Username does not exist.")

    def register_user(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return

        self.username = username
        self.password = password
        self.show_email_verification()

    def send_otp(self):
        email = self.register_email_entry.get()
        if not email:
            messagebox.showerror("Error", "Email is required.")
            return
        
        self.email = email
        self.otp = random.randint(100000, 999999)
        send_otp_email(email, self.otp)
        messagebox.showinfo("Info", "OTP sent to your email.")
        self.show_otp_verification()

    # OTP verification for registration
    def verify_registration_otp(self):
        otp_input = self.email_otp_entry.get()  # Get the OTP entered by the user

        if verify_otp(otp_input, str(self.otp)):  # Verify the OTP
            # Call add_user to insert the user into the database
            add_user(self.username, self.password, self.email)

            # Show success message in a messagebox
            messagebox.showinfo("Success", f"Registration successful! Please log in.\nUsername: {self.username}")

            # Redirect to the login page
            self.show_login()
        else:
            # Show an error message if OTP verification fails
            messagebox.showerror("Error", "Invalid OTP.")

    # OTP verification for login
    def verify_login_otp(self):
        otp_input = self.email_otp_entry.get()

        if verify_otp(otp_input, str(self.otp)):  # Verify the OTP for login
            messagebox.showinfo("Success", f"Login successful!\nUsername: {self.username}")
            self.show_login()  # Redirect to the login page
        else:
            messagebox.showerror("Error", "Invalid OTP.")

# Create the Tkinter window and run the app
root = tk.Tk()
app = AuthenticationApp(root)
root.mainloop()