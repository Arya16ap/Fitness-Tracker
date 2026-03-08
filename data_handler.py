# data_handler.py

import json
import os
from tkinter import messagebox
import config

def load_data():
    if not os.path.exists(config.FILENAME):
        return {}
    try:
        with open(config.FILENAME, 'r') as f:
            content = f.read()
            if not content:
                return {}
            data = json.loads(content)
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        messagebox.showerror("Data Error", f"Could not read or parse {config.FILENAME}. Starting with empty data.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred loading data: {e}")
        return {}

def save_data(data):
    try:
        with open(config.FILENAME, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
         messagebox.showerror("Save Error", f"Could not save data to {config.FILENAME}: {e}")