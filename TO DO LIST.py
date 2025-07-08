import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

import json
import datetime
import os

TASK_FILE = "gui_todo_data.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do PRO - GUI Version")
        self.root.geometry("700x550")

        self.tasks = self.load_tasks()

        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        title = tk.Label(self.root, text="To-Do List (Hinglish Style)", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        self.task_entry = tk.Entry(self.root, font=("Arial", 14), width=40)
        self.task_entry.pack(pady=5)

        category_label = tk.Label(self.root, text="Select Category:", font=("Arial", 12))
        category_label.pack(pady=2)

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category_var, state="readonly", font=("Arial", 12))
        self.category_combo['values'] = ("Important", "Medium", "Less Important", "Personal")
        self.category_combo.current(0)
        self.category_combo.pack(pady=5)

        time_label = tk.Label(self.root, text="Select Deadline (24hr HH:MM):", font=("Arial", 12))
        time_label.pack(pady=2)

        self.deadline_entry = ttk.Entry(self.root, font=("Arial", 12), width=20)
        self.deadline_entry.insert(0, "14:00")
        self.deadline_entry.pack(pady=5)

        add_btn = tk.Button(self.root, text="Add Task", command=self.add_task, font=("Arial", 12), bg="#4CAF50", fg="white")
        add_btn.pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Task", "Category", "Deadline", "Status"), show='headings')
        self.tree.heading("Task", text="Task")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Mark Done", command=self.mark_done, bg="#2196F3", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Show Stats", command=self.show_stats, bg="#9C27B0", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Missed Tasks Taunt", command=self.taunt, bg="#FF9800", fg="black").grid(row=0, column=3, padx=5)

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(TASK_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        task = self.task_entry.get()
        category = self.category_var.get()
        deadline = self.deadline_entry.get()

        if not task:
            messagebox.showerror("Error", "Task cannot be empty!")
            return

        self.tasks.append({"task": task, "category": category, "deadline": deadline, "done": False})
        self.save_tasks()
        self.refresh_list()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Added", "Task added successfully! Bhai kamaal ka kaam kiya hai!")

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.tasks:
            status = "Done" if t["done"] else "Pending"
            self.tree.insert('', tk.END, values=(t["task"], t["category"], t["deadline"], status))

    def mark_done(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Select a task first!")
            return

        task_text = self.tree.item(selected)['values'][0]
        for t in self.tasks:
            if t["task"] == task_text:
                t["done"] = True
                break
        self.save_tasks()
        self.refresh_list()
        messagebox.showinfo("Shabaash!", "Task completed! Zindagi mein aage badhne ke liye yahi toh chahiye!")

    def delete_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Select a task to delete!")
            return

        task_text = self.tree.item(selected)['values'][0]
        self.tasks = [t for t in self.tasks if t["task"] != task_text]
        self.save_tasks()
        self.refresh_list()
        messagebox.showinfo("Deleted", "Task removed. Kya kaam ka kaam hata diya! 😎")

    def show_stats(self):
        total = len(self.tasks)
        done = sum(t['done'] for t in self.tasks)
        pending = total - done
        messagebox.showinfo("Stats", f"Total: {total}\nDone: {done}\nPending: {pending}")

    def taunt(self):
        now = datetime.datetime.now().strftime("%H:%M")
        taunts = []
        for t in self.tasks:
            if not t['done'] and t['deadline'] <= now:
                taunts.append(f"😤 '{t['task']}' reh gaya bhai! Mummy daantengi ab!")
        if taunts:
            messagebox.showwarning("Taunts Incoming!", "\n".join(taunts))
        else:
            messagebox.showinfo("Good Going!", "Sare kaam time se! Tum toh boss nikle! 😎")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
