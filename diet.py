# diet.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import data_handler # To save data to the main JSON file

class DietApp:
    """
    Manages the BMI Calculation and Diet Suggestion interface.
    """
    def __init__(self, root, username, data):
        self.root = root # Toplevel window
        self.username = username
        # Full data structure {user: {pass..., workouts: {...}, bmi_history: [...]}}
        self.data = data

        self.root.title(f"Diet & BMI - {username}")
        self.root.geometry("450x600")
        # Use styling from the friend's code example
        self.root.configure(bg="#2c3e50")

        # --- UI Setup ---
        # Main frame using the friend's styling
        self.main_frame = tk.Frame(self.root, bg="#34495e", padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self._create_widgets()
        self._load_last_profile_data() # Load previous inputs


    def _create_widgets(self):
        """Creates the input fields, buttons, and labels for the BMI calculator."""

        # --- Input Fields ---
        tk.Label(self.main_frame, text="Weight (kg):", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack(pady=5)
        self.weight_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.weight_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Height (ft and in):", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack(pady=5)
        height_frame = tk.Frame(self.main_frame, bg="#34495e")
        height_frame.pack(pady=5)
        self.feet_entry = tk.Entry(height_frame, width=5, font=("Arial", 12))
        self.feet_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(height_frame, text="ft", fg="white", bg="#34495e", font=("Arial", 12)).pack(side=tk.LEFT)
        self.inches_entry = tk.Entry(height_frame, width=5, font=("Arial", 12))
        self.inches_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(height_frame, text="in", fg="white", bg="#34495e", font=("Arial", 12)).pack(side=tk.LEFT)

        tk.Label(self.main_frame, text="Age:", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack(pady=5)
        self.age_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.age_entry.pack(pady=5)

        # Gender Selection
        self.gender_var = tk.StringVar(self.root)
        self.gender_var.set("Male") # Default value
        tk.Label(self.main_frame, text="Gender:", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack(pady=5)
        # Apply background color styling to OptionMenu requires more work, using default for now
        gender_menu = tk.OptionMenu(self.main_frame, self.gender_var, "Male", "Female")
        gender_menu.pack(pady=5)

        # Diet Preference Selection
        self.diet_var = tk.StringVar(self.root)
        self.diet_var.set("Veg") # Default value
        tk.Label(self.main_frame, text="Diet Preference:", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack(pady=5)
        diet_menu = tk.OptionMenu(self.main_frame, self.diet_var, "Veg", "Non-Veg", "Vegan")
        diet_menu.pack(pady=5)

        # --- Calculate Button ---
        calculate_btn = tk.Button(
            self.main_frame, text="Calculate BMI",
            command=self.calculate_bmi_and_suggest, # Calls the calculation method
            bg="#e74c3c", fg="white", font=("Arial", 14, "bold")
        )
        calculate_btn.pack(pady=15) # Increased padding

        # --- Result Labels ---
        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 14, "bold"), fg="white", bg="#34495e")
        self.result_label.pack(pady=5)
        self.diet_label = tk.Label(self.main_frame, text="", wraplength=400, justify="center", font=("Arial", 12), fg="white", bg="#34495e")
        self.diet_label.pack(pady=5)

        # Optional: Add a close button for this window
        close_btn = tk.Button(
            self.main_frame, text="Close", command=self.root.destroy,
            bg="#bdc3c7", fg="black", font=("Arial", 10)
        )
        close_btn.pack(pady=10, side=tk.BOTTOM)


    def _load_last_profile_data(self):
        """Loads the last saved profile data into the entry fields."""
        profile_data = self.data.get(self.username, {}).get("profile", None)

        if profile_data:
            # Safely get values, fallback to empty string if None
            weight = profile_data.get("weight_kg", "")
            feet = profile_data.get("height_ft", "")
            inches = profile_data.get("height_in", "")
            age = profile_data.get("age", "")
            gender = profile_data.get("gender", "Male") # Default if not saved
            diet_pref = profile_data.get("diet_preference", "Veg") # Default

            # Clear existing entries before inserting
            self.weight_entry.delete(0, tk.END); self.weight_entry.insert(0, str(weight))
            self.feet_entry.delete(0, tk.END);   self.feet_entry.insert(0, str(feet))
            self.inches_entry.delete(0, tk.END); self.inches_entry.insert(0, str(inches))
            self.age_entry.delete(0, tk.END);    self.age_entry.insert(0, str(age))
            self.gender_var.set(gender)
            self.diet_var.set(diet_pref)


    def calculate_bmi_and_suggest(self):
        """Handles input validation, BMI calculation, and diet suggestion."""
        try:
            # Get values from entries
            weight = float(self.weight_entry.get())
            feet = int(self.feet_entry.get())
            inches = int(self.inches_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            diet_type = self.diet_var.get()

            # Basic validation for positive, sensible values
            if weight <= 0 or feet < 0 or inches < 0 or inches >= 12 or age <= 0:
                messagebox.showerror("Error", "Please enter valid positive values.\n(Inches must be less than 12)", parent=self.root)
                return

            # --- Calculation ---
            total_inches = (feet * 12) + inches
            if total_inches <= 0: # Height cannot be zero
                 messagebox.showerror("Error", "Height cannot be zero.", parent=self.root)
                 return
            height_m = total_inches * 0.0254 # Conversion factor
            bmi = round(weight / (height_m ** 2), 2)

            # --- Get Suggestion ---
            category, diet_suggestion = self._get_diet_suggestion(bmi, gender, diet_type)

            # --- Display Results ---
            self.result_label.config(text=f"BMI: {bmi} ({category})")
            self.diet_label.config(text=f"Diet Suggestion: {diet_suggestion}")

            # --- Prepare Data for Saving ---
            entry_data = {
                "date": datetime.now().isoformat(sep=" ", timespec='microseconds'),
                "weight_kg": weight,
                "height_ft": feet,
                "height_in": inches,
                "age": age,
                "gender": gender,
                "diet_preference": diet_type,
                "bmi": bmi,
                "category": category,
                "suggestion": diet_suggestion
            }

            # --- Save Data ---
            self._save_bmi_data(entry_data)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weight, height, and age.", parent=self.root)
        except Exception as e:
             messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=self.root)


    def _get_diet_suggestion(self, bmi, gender, diet_type):
        """Determines BMI category and provides diet suggestions."""
        # Using thresholds similar to the friend's code
        if gender == "Male":
            bmi_thresholds = [18.5, 24.9, 29.9]
        else: # Assume Female or other uses slightly different thresholds
            bmi_thresholds = [18.0, 23.9, 28.9] # Example thresholds for Female

        # Determine category and base suggestion
        if bmi < bmi_thresholds[0]:
            category = "Underweight"
            diet = "Focus on nutrient-dense, high-calorie meals: include nuts, seeds, dairy (if applicable), avocados, and protein-rich foods."
        elif bmi_thresholds[0] <= bmi < bmi_thresholds[1]:
            category = "Normal Weight"
            diet = "Maintain a balanced diet with adequate protein, complex carbohydrates (whole grains), fruits, vegetables, and healthy fats."
        elif bmi_thresholds[1] <= bmi < bmi_thresholds[2]:
            category = "Overweight"
            diet = "Focus on portion control, reduced intake of processed foods and sugars. Emphasize lean proteins, high-fiber vegetables, and whole grains."
        else: # bmi >= bmi_thresholds[2]
            category = "Obese"
            diet = "Consult a healthcare professional. Generally, requires a significant calorie deficit, focus on whole foods, lean protein, lots of vegetables, and increased physical activity."

        # Add specific examples based on diet preference
        diet_options = {
            "Veg": " (e.g., Paneer, Lentils, Beans, Tofu, Nuts, Seeds, Whole Grains)",
            "Non-Veg": " (e.g., Lean Chicken/Fish, Eggs, Lentils, Beans, Vegetables)",
            "Vegan": " (e.g., Tofu, Tempeh, Lentils, Beans, Quinoa, Nuts, Seeds, Leafy Greens)"
        }
        diet += diet_options.get(diet_type, "") # Append specific examples

        return category, diet


    def _save_bmi_data(self, entry_data):
        """Saves the BMI calculation result to fitness_data.json."""
        try:
            # Ensure user exists in data (should always be true if logged in)
            if self.username not in self.data:
                messagebox.showerror("Error", "Current user data not found.", parent=self.root)
                return

            # Initialize 'profile' and 'bmi_history' if they don't exist
            if "profile" not in self.data[self.username]:
                self.data[self.username]["profile"] = {}
            if "bmi_history" not in self.data[self.username]:
                self.data[self.username]["bmi_history"] = []

            # Update profile with the latest entered data
            profile = self.data[self.username]["profile"]
            profile["weight_kg"] = entry_data["weight_kg"]
            profile["height_ft"] = entry_data["height_ft"]
            profile["height_in"] = entry_data["height_in"]
            profile["age"] = entry_data["age"]
            profile["gender"] = entry_data["gender"]
            profile["diet_preference"] = entry_data["diet_preference"]

            # Append the new calculation to the history list
            self.data[self.username]["bmi_history"].append(entry_data)

            # Save the entire updated data structure using data_handler
            data_handler.save_data(self.data)
            print("BMI data saved successfully.") # Optional console confirmation

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save BMI data: {e}", parent=self.root)