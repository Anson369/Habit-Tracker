import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import pickle
import os
class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("500x400")
        self.root.configure(bg="#E0F7FA")
        self.user_id = None
        while not self.user_id or len(self.user_id) < 5:
            self.user_id = simpledialog.askstring("User ID", "Enter your user ID (min 5 characters):")
            if self.user_id is None:
                self.root.destroy()
                return
            if len(self.user_id) < 5:
                messagebox.showerror("Error", "User ID must be at least 5 characters long!")
        self.filename = f"{self.user_id}.pkl"
        if os.path.exists(self.filename):
            messagebox.showinfo("Welcome", "Welcome back!")
        else:
            messagebox.showinfo("Welcome", "User ID not found. Initializing a new profile.")
        self.habits = self.load_from_file()
        self.suggested_habits = [
            "Exercise",
            "Drink water",
            "Read a book",
            "Meditate",
            "Write in a journal",
            "Eat healthy",
            "Sleep early",
            "Practice gratitude"
        ]
        self.create_widgets()
    def create_widgets(self):
        tk.Label(self.root, text="Habit Tracker", font=("Helvetica", 18, "bold"), bg="#00796B", fg="white",
                 pady=10).pack(fill=tk.X)
        self.listbox = tk.Listbox(self.root, width=50, height=10, bg="#B2DFDB")
        self.listbox.pack(pady=10)
        self.update_listbox()
        btn_frame = tk.Frame(self.root, bg="#E0F7FA")
        btn_frame.pack()
        tk.Button(btn_frame, text="Add Habit", command=self.add_habit, bg="#388E3C", fg="white").grid(row=0, column=0,padx=5, pady=5)
        tk.Button(btn_frame, text="Mark Habit", command=self.mark_habit, bg="#1976D2", fg="white").grid(row=0, column=1,padx=5, pady=5)
        tk.Button(btn_frame, text="Delete Habit", command=self.delete_habit, bg="#D32F2F", fg="white").grid(row=0,column=2,padx=5,pady=5)
        tk.Button(btn_frame, text="Show Habits", command=self.show_habits, bg="#FBC02D", fg="black").grid(row=0,column=3,padx=5,pady=5)
        tk.Button(self.root, text="Save & Exit", command=self.save_and_exit, bg="#455A64", fg="white").pack(pady=10)
    def add_habit(self):
        def on_select_suggested_habit(event):
            habit_name = event.widget.get(event.widget.curselection())
            self.add_custom_habit(habit_name)
        suggest_window = tk.Toplevel(self.root)
        suggest_window.title("Choose a Habit")
        listbox = tk.Listbox(suggest_window, width=40, height=10, bg="#B2DFDB")
        listbox.pack(pady=10)
        for habit in self.suggested_habits:
            listbox.insert(tk.END, habit)
        listbox.bind("<Double-1>", on_select_suggested_habit)
        def on_manual_entry():
            habit_name = simpledialog.askstring("Enter Habit", "Enter a custom habit:")
            if habit_name:
                self.add_custom_habit(habit_name)
        manual_button = tk.Button(suggest_window, text="Enter Custom Habit", command=on_manual_entry, bg="#388E3C",fg="white")
        manual_button.pack(pady=10)
    def add_custom_habit(self, name):
        frequency = simpledialog.askstring("Frequency", "Enter frequency (daily/weekly):")
        if name and frequency:
            if name in self.habits:
                messagebox.showerror("Error", "Habit already exists!")
            else:
                self.habits[name] = {"frequency": frequency, "completed_days": []}
                self.update_listbox()
                messagebox.showinfo("Success", f"Habit '{name}' added successfully.")
    def mark_habit(self):
        name = simpledialog.askstring("Mark Habit", "Enter habit name:")
        date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD) or leave blank for today:")
        if not date:
            date = datetime.date.today().isoformat()
        if name in self.habits:
            if date in self.habits[name]["completed_days"]:
                messagebox.showwarning("Warning", f"Habit '{name}' already marked for {date}.")
            else:
                self.habits[name]["completed_days"].append(date)
                self.update_listbox()
                messagebox.showinfo("Success", f"Habit '{name}' marked as completed for {date}.")
        else:
            messagebox.showerror("Error", "Habit not found!")
    def delete_habit(self):
        name = simpledialog.askstring("Delete Habit", "Enter habit name to delete:")
        if name in self.habits:
            del self.habits[name]
            self.update_listbox()
            messagebox.showinfo("Success", f"Habit '{name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Habit not found!")
    def show_habits(self):
        habits_list = "\n".join(
            [f"{name} ({details['frequency']}): {len(details['completed_days'])} completions, completed dates = {details['completed_days']}"for name, details in self.habits.items()])
        if habits_list:
            messagebox.showinfo("Your Habits", habits_list)
        else:
            messagebox.showinfo("Your Habits", "No habits to show.")
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for name, details in self.habits.items():
            self.listbox.insert(tk.END,
                                f"{name} ({details['frequency']}): {len(details['completed_days'])} completions")
    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.habits, file)
        messagebox.showinfo("Success", "Habits saved successfully.")
    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as file:
                return pickle.load(file)
        return {}
    def save_and_exit(self):
        self.save_to_file()
        self.root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()