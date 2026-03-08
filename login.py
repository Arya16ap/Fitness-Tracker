import tkinter as tk
from tkinter import messagebox
import data_handler 
import config       

class LoginWindow:
    
    def __init__(self, on_login_success_callback):
        self.on_login_success = on_login_success_callback 

        self.login_root = tk.Tk() 
        self.login_root.title("Login / Register")
        self.login_root.geometry("300x270") 
        self.login_root.configure(bg="#1F0037")

        self.data = data_handler.load_data()

        tk.Label(self.login_root, text="Username", font=("Arial", 14), bg="#1F0037", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(self.login_root, font=("Arial", 12))
        self.username_entry.pack(pady=5, padx=20, fill=tk.X) # Added padding and fill

        tk.Label(self.login_root, text="Password", font=("Arial", 14), bg="#1F0037", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.login_root, show='*', font=("Arial", 12))
        self.password_entry.pack(pady=5, padx=20, fill=tk.X) # Added padding and fill

        button_frame = tk.Frame(self.login_root, bg="#1F0037") # Match background
        button_frame.pack(pady=15)

        login_button = tk.Button(button_frame, text="Login", font=("Arial", 12), command=self.login, bg="#39FF14", fg="black", width=8) # Green button
        login_button.grid(row=0, column=0, padx=10)

        register_button = tk.Button(button_frame, text="Register", font=("Arial", 12), command=self.register, bg="#1ABC9C", fg="white", width=8) # Using a color from config
        register_button.grid(row=0, column=1, padx=10)

        self.login_root.mainloop()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.", parent=self.login_root)
            return

        self.data = data_handler.load_data()

        user_account_data = self.data.get(username)

        if user_account_data and user_account_data.get("password") == password:
            messagebox.showinfo("Success", f"Welcome back, {username}!", parent=self.login_root)
            self.login_root.destroy()
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.", parent=self.login_root)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.", parent=self.login_root)
            return

        self.data = data_handler.load_data()

        if username in self.data:
            messagebox.showerror("Error", "Username already exists. Please choose another or login.", parent=self.login_root)
        elif not username: # Basic validation
             messagebox.showerror("Error", "Username cannot be empty.", parent=self.login_root)
        elif not password: # Basic validation
             messagebox.showerror("Error", "Password cannot be empty.", parent=self.login_root)
        else:
            self.data[username] = {
                "password": password,
                "workouts": {workout: [] for workout in config.WORKOUT_LIST}
            }
            data_handler.save_data(self.data)
            messagebox.showinfo("Success", f"User '{username}' registered successfully! You can now login.", parent=self.login_root)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)