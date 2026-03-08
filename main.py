# main.py

import tkinter as tk
from login import LoginWindow
from workout import WorkoutApp
# Updated import for the new DietApp class
from diet import DietApp
import data_handler

def create_main_selection_window(username):
    """Creates the main app window after successful login."""
    main_root = tk.Tk()
    main_root.title(f"Fitness Tracker - {username}")
    main_root.geometry("400x300")
    main_root.configure(bg="#2C3E50")

    # --- Define Actions for Buttons ---
    def open_workout():
        all_user_data = data_handler.load_data()
        workout_top_level = tk.Toplevel(main_root)
        # Pass the Toplevel, username, and the loaded data
        app = WorkoutApp(workout_top_level, username, all_user_data)

    def open_diet():
        all_user_data = data_handler.load_data()
        diet_top_level = tk.Toplevel(main_root)
        # Instantiate the DietApp class
        app = DietApp(diet_top_level, username, all_user_data)

    # --- Create Widgets ---
    tk.Label(main_root, text=f"Welcome {username}!", font=("Arial", 16, "bold"), bg="#2C3E50", fg="#39FF14").pack(pady=20)
    tk.Button(main_root, text="Workout Tracker", width=25, command=open_workout, bg="#1ABC9C", fg="white").pack(pady=5)
    tk.Button(main_root, text="Diet Tracker", width=25, command=open_diet, bg="#27AE60", fg="white").pack(pady=5)
    tk.Button(main_root, text="Exit", width=25, command=main_root.destroy, bg="red", fg="white").pack(pady=20)

    main_root.mainloop()


# --- Main Execution ---
if __name__ == "__main__":
    # Start with the LoginWindow, passing the function to call on success
    LoginWindow(create_main_selection_window)