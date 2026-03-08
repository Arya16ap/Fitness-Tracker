import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from datetime import datetime
import config
import data_handler

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

GRID_COLUMNS = 3


class WorkoutApp:

    def __init__(self, root, username, data):
        self.root = root
        self.username = username
        self.data = data

        self.root.title(f"Workout Selection - {username}")
        self.root.geometry("500x450")
        self.root.configure(bg=config.BG_COLOR)

        self._create_widgets()

    def _create_widgets(self):
        tk.Label(
            self.root, text="Select an Exercise to Log",
            font=config.TITLE_FONT, bg=config.BG_COLOR, fg="#39FF14"
        ).pack(pady=15)

        grid_frame = tk.Frame(self.root, bg=config.BG_COLOR)
        grid_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self._populate_exercise_grid(grid_frame)

        bottom_frame = tk.Frame(self.root, bg=config.BG_COLOR)
        bottom_frame.pack(pady=20, fill=tk.X, padx=20)
        self._create_bottom_buttons(bottom_frame)

    def _populate_exercise_grid(self, parent_frame):
        for index, workout_name in enumerate(config.WORKOUT_LIST):
            button_command = self._create_popup_command(workout_name)

            button = tk.Button(
                parent_frame,
                text=workout_name,
                font=config.BUTTON_FONT,
                command=button_command,
                bg=config.BUTTON_COLOR,
                fg=config.FG_COLOR,
                width=15,
                height=2
            )

            row = index // GRID_COLUMNS
            col = index % GRID_COLUMNS
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            parent_frame.grid_columnconfigure(col, weight=1)

        num_rows = (len(config.WORKOUT_LIST) + GRID_COLUMNS - 1) // GRID_COLUMNS
        for r in range(num_rows):
            parent_frame.grid_rowconfigure(r, weight=1)

    def _create_popup_command(self, workout_name):
        def command():
            self.open_exercise_popup(workout_name)
        return command

    def _create_bottom_buttons(self, parent_frame):
        tk.Button(
            parent_frame, text="Overall Progress", font=config.BUTTON_FONT,
            command=self.show_overall_graph,
            bg="#8E44AD", fg=config.FG_COLOR, width=15
        ).pack(side=tk.LEFT, expand=True, padx=10)

        tk.Button(
            parent_frame, text="Close Tracker", font=config.BUTTON_FONT,
            command=self.root.destroy,
            bg="red", fg=config.FG_COLOR, width=15
        ).pack(side=tk.RIGHT, expand=True, padx=10)

    def open_exercise_popup(self, workout_name):
        popup_root = Toplevel(self.root)
        popup_root.title(workout_name)
        popup_root.geometry("350x250")
        popup_root.configure(bg=config.BG_COLOR)
        popup_root.resizable(False, False)

        entry_frame = tk.Frame(popup_root, bg=config.BG_COLOR)
        entry_frame.pack(pady=15)

        tk.Label(entry_frame, text="Sets:", font=config.LABEL_FONT, bg=config.BG_COLOR, fg=config.FG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        sets_entry = tk.Entry(entry_frame, width=6, font=config.LABEL_FONT, bg=config.ENTRY_BG)
        sets_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Reps:", font=config.LABEL_FONT, bg=config.BG_COLOR, fg=config.FG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        reps_entry = tk.Entry(entry_frame, width=6, font=config.LABEL_FONT, bg=config.ENTRY_BG)
        reps_entry.grid(row=1, column=1, padx=5, pady=5)

        self._prefill_popup_entries(workout_name, sets_entry, reps_entry)

        button_frame = tk.Frame(popup_root, bg=config.BG_COLOR)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Button(
            button_frame, text="Save Log", font=config.BUTTON_FONT, width=12,
            command=lambda: self.save_single_exercise(workout_name, sets_entry, reps_entry, popup_root),
            bg="#27AE60", fg=config.FG_COLOR
        ).pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        tk.Button(
            button_frame, text="View Graph", font=config.BUTTON_FONT, width=12,
            command=lambda: self.show_workout_graph(workout_name),
            bg="#3498DB", fg=config.FG_COLOR
        ).pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        tk.Button(
            popup_root, text="Close", font=config.BUTTON_FONT, width=8,
            command=popup_root.destroy,
            bg="#E74C3C", fg=config.FG_COLOR
        ).pack(pady=10)

    def _prefill_popup_entries(self, workout_name, sets_widget, reps_widget):
        try:
            user_history = self.data[self.username]["workouts"][workout_name]
            if user_history:
                last_log = user_history[-1]
                last_sets = last_log.get("sets")
                last_reps = last_log.get("reps")
                if last_sets is not None:
                    sets_widget.insert(0, str(last_sets))
                if last_reps is not None:
                    reps_widget.insert(0, str(last_reps))
        except KeyError:
            pass

    def save_single_exercise(self, workout_name, sets_entry, reps_entry, popup_window):
        sets_str = sets_entry.get().strip()
        reps_str = reps_entry.get().strip()

        sets_num, reps_num = self._validate_and_get_set_rep(sets_str, reps_str, popup_window)

        if sets_num is None and reps_num is None and (sets_str or reps_str):
            return
        elif not sets_str and not reps_str:
            messagebox.showwarning("Input Needed", "Please enter Sets or Reps.", parent=popup_window)
            return

        timestamp = datetime.now().isoformat(sep=" ", timespec='microseconds')
        log_entry = {"date": timestamp, "sets": sets_num, "reps": reps_num}

        try:
            if self.username not in self.data:
                self.data[self.username] = {"password": "", "workouts": {}}
            if "workouts" not in self.data[self.username]:
                self.data[self.username]["workouts"] = {}
            if workout_name not in self.data[self.username]["workouts"]:
                self.data[self.username]["workouts"][workout_name] = []

            self.data[self.username]["workouts"][workout_name].append(log_entry)
            data_handler.save_data(self.data)

            messagebox.showinfo("Saved", f"{workout_name} log saved!", parent=popup_window)
            popup_window.destroy()

        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save log: {e}", parent=popup_window)

    def _validate_and_get_set_rep(self, sets_str, reps_str, parent_window):
        sets_num = None
        reps_num = None

        if sets_str:
            try:
                sets_num = int(sets_str)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Sets value '{sets_str}' must be a whole number.", parent=parent_window)
                return None, None

        if reps_str:
            try:
                reps_num = int(reps_str)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Reps value '{reps_str}' must be a whole number.", parent=parent_window)
                return None, None

        return sets_num, reps_num

    def _create_graph_popup(self, title):
        graph_window = Toplevel(self.root)
        graph_window.title(title)
        graph_window.geometry("800x600")

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, graph_window)
        toolbar.update()

        return graph_window, fig, ax

    def _get_workout_history(self, workout_name):
        try:
            return self.data[self.username]["workouts"][workout_name]
        except KeyError:
            return []

    def show_workout_graph(self, workout_name):
        history = self._get_workout_history(workout_name)
        if not history:
            messagebox.showinfo("No Data", f"No history for {workout_name}.", parent=self.root)
            return

        dates, sets_data, reps_data = [], [], []
        valid_sets_dates, valid_sets_values = [], []
        valid_reps_dates, valid_reps_values = [], []

        for entry in history:
            dt = None
            try:
                dt = datetime.fromisoformat(entry.get("date", ""))
            except ValueError:
                continue

            if dt:
                try:
                    sets_val = float(entry.get("sets")) if entry.get("sets") is not None else None
                except (ValueError, TypeError):
                    sets_val = None
                try:
                    reps_val = float(entry.get("reps")) if entry.get("reps") is not None else None
                except (ValueError, TypeError):
                    reps_val = None

                if sets_val is not None:
                    valid_sets_dates.append(dt)
                    valid_sets_values.append(sets_val)
                if reps_val is not None:
                    valid_reps_dates.append(dt)
                    valid_reps_values.append(reps_val)

        if not valid_sets_dates and not valid_reps_dates:
            messagebox.showinfo("Insufficient Data", f"No numeric data to plot for {workout_name}.", parent=self.root)
            return

        graph_window, fig, ax = self._create_graph_popup(f"Progress: {workout_name}")

        if valid_sets_dates:
            ax.plot(valid_sets_dates, valid_sets_values, marker='o', linestyle='-', label='Sets')
        if valid_reps_dates:
            ax.plot(valid_reps_dates, valid_reps_values, marker='x', linestyle='--', label='Reps')

        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.set_title(f"{workout_name} Progress")
        if valid_sets_dates or valid_reps_dates:
            ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()

        fig.canvas.draw_idle()
        graph_window.protocol("WM_DELETE_WINDOW", lambda fig=fig, win=graph_window: (plt.close(fig), win.destroy()))

    def show_overall_graph(self):
        all_workouts = self.data.get(self.username, {}).get("workouts", {})
        if not all_workouts:
            messagebox.showinfo("No Data", "No workout data available.", parent=self.root)
            return

        daily_data = {}
        for workout_name, history in all_workouts.items():
            for entry in history:
                dt, date_key = None, None
                try:
                    dt = datetime.fromisoformat(entry.get("date", ""))
                    date_key = dt.date()
                except ValueError:
                    continue

                if date_key:
                    if date_key not in daily_data:
                        daily_data[date_key] = {'sets_sum': 0.0, 'sets_count': 0, 'reps_sum': 0.0, 'reps_count': 0}
                    try:
                        sets_val = float(entry.get("sets")) if entry.get("sets") is not None else None
                    except (ValueError, TypeError):
                        sets_val = None
                    try:
                        reps_val = float(entry.get("reps")) if entry.get("reps") is not None else None
                    except (ValueError, TypeError):
                        reps_val = None

                    if sets_val is not None:
                        daily_data[date_key]['sets_sum'] += sets_val
                        daily_data[date_key]['sets_count'] += 1
                    if reps_val is not None:
                        daily_data[date_key]['reps_sum'] += reps_val
                        daily_data[date_key]['reps_count'] += 1

        if not daily_data or all(d['sets_count'] == 0 and d['reps_count'] == 0 for d in daily_data.values()):
            messagebox.showinfo("No Data", "No numeric data found to calculate averages.", parent=self.root)
            return

        plot_dates, avg_sets, avg_reps = [], [], []
        for date_key in sorted(daily_data.keys()):
            data = daily_data[date_key]
            set_avg = data['sets_sum'] / data['sets_count'] if data['sets_count'] > 0 else None
            rep_avg = data['reps_sum'] / data['reps_count'] if data['reps_count'] > 0 else None
            plot_dates.append(date_key)
            avg_sets.append(set_avg)
            avg_reps.append(rep_avg)

        final_dates_sets, final_vals_sets = zip(*[(d, v) for d, v in zip(plot_dates, avg_sets) if v is not None]) if any(v is not None for v in avg_sets) else ([], [])
        final_dates_reps, final_vals_reps = zip(*[(d, v) for d, v in zip(plot_dates, avg_reps) if v is not None]) if any(v is not None for v in avg_reps) else ([], [])

        if not final_dates_sets and not final_dates_reps:
            messagebox.showinfo("Calculation Error", "Could not calculate valid averages.", parent=self.root)
            return

        graph_window, fig, ax = self._create_graph_popup("Overall Average Progress")

        if final_dates_sets:
            ax.plot(final_dates_sets, final_vals_sets, marker='o', linestyle='-', label='Avg Sets')
        if final_dates_reps:
            ax.plot(final_dates_reps, final_vals_reps, marker='x', linestyle='--', label='Avg Reps')

        ax.set_xlabel("Date")
        ax.set_ylabel("Average Count")
        ax.set_title("Overall Daily Averages")
        if final_dates_sets or final_dates_reps:
            ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()

        fig.canvas.draw_idle()
        graph_window.protocol("WM_DELETE_WINDOW", lambda fig=fig, win=graph_window: (plt.close(fig), win.destroy()))