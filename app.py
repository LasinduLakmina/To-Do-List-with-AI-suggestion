import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import datetime

# Create or connect to the database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    priority INTEGER,
    deadline TEXT,
    status TEXT
)
''')
conn.commit()

# Function to refresh the task list
def refresh_tasks():
    listbox_pending.delete(0, tk.END)
    listbox_completed.delete(0, tk.END)
    
    # Fetch pending tasks
    cursor.execute("SELECT * FROM tasks WHERE status = 'Pending' ORDER BY priority DESC, deadline ASC")
    tasks = cursor.fetchall()
    for task in tasks:
        task_str = f"{task[0]}. {task[1]} - Priority: {task[2]} - Deadline: {task[3]}"
        add_task_to_listbox(listbox_pending, task_str, task[2], task[3])  # Add to pending with color priority
    
    # Fetch completed tasks
    cursor.execute("SELECT * FROM tasks WHERE status = 'Completed' ORDER BY priority DESC, deadline ASC")
    tasks = cursor.fetchall()
    for task in tasks:
        task_str = f"{task[0]}. {task[1]} - Priority: {task[2]} - Deadline: {task[3]}"
        add_task_to_listbox(listbox_completed, task_str, task[2], task[3])  # Add to completed with color priority
    
    # Get AI suggestions
    get_ai_suggestions()

# Function to add task to listbox with color based on priority
def add_task_to_listbox(listbox, task_str, priority, deadline):
    if priority <= 3:
        listbox.insert(tk.END, task_str)
        listbox.itemconfig(tk.END, {'bg': 'red'})
    elif priority <= 7:
        listbox.insert(tk.END, task_str)
        listbox.itemconfig(tk.END, {'bg': 'yellow'})
    else:
        listbox.insert(tk.END, task_str)
        listbox.itemconfig(tk.END, {'bg': 'green'})

# Function to calculate task urgency score (AI recommendation)
def get_ai_suggestions():
    today = datetime.date.today()
    
    # Fetch all pending tasks
    cursor.execute("SELECT * FROM tasks WHERE status = 'Pending'")
    tasks = cursor.fetchall()

    suggestions = []
    
    for task in tasks:
        task_id, title, priority, deadline, status = task
        deadline_date = datetime.datetime.strptime(deadline, "%m/%d/%y").date()
        days_left = (deadline_date - today).days
        urgency_score = priority * 10 + days_left  # Simple score based on priority and deadline
        
        suggestions.append((task_id, title, urgency_score, days_left, priority))

    # Sort suggestions by urgency score (lower score = more urgent)
    suggestions.sort(key=lambda x: x[2])

    # Display AI suggestions in the label
    suggestion_text = "AI Suggested Tasks:\n"
    for suggestion in suggestions[:5]:  # Show top 5 suggestions
        suggestion_text += f"{suggestion[1]} - Priority: {suggestion[4]} - Deadline in {suggestion[3]} days\n"
    
    label_ai_suggestions.config(text=suggestion_text)

# Function to add task
def add_task():
    title = entry_title.get()
    priority = entry_priority.get()
    deadline = entry_deadline.get_date()

    if not title or not priority or not deadline:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    try:
        priority = int(priority)
        if priority < 1 or priority > 10:
            messagebox.showwarning("Priority Error", "Priority must be between 1 and 10!")
            return
    except ValueError:
        messagebox.showwarning("Priority Error", "Priority must be an integer (1-10)!")
        return

    cursor.execute("INSERT INTO tasks (title, priority, deadline, status) VALUES (?, ?, ?, ?)", 
                   (title, priority, deadline.strftime("%m/%d/%y"), "Pending"))
    conn.commit()
    
    entry_title.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_deadline.set_date(None)  # Clear the date picker to None

    refresh_tasks()

# Function to edit a task
def edit_task():
    selected_task = listbox_pending.curselection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task to edit!")
        return

    task_id = listbox_pending.get(selected_task).split(".")[0]

    cursor.execute("SELECT title, priority, deadline FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if task:
        title, priority, deadline = task
        entry_title.delete(0, tk.END)
        entry_title.insert(0, title)
        entry_priority.delete(0, tk.END)
        entry_priority.insert(0, priority)
        entry_deadline.set_date(deadline)

        def update_task():
            new_title = entry_title.get()
            new_priority = entry_priority.get()
            new_deadline = entry_deadline.get_date()

            if not new_title or not new_priority or not new_deadline:
                messagebox.showwarning("Input Error", "Please fill all fields!")
                return

            try:
                new_priority = int(new_priority)
                if new_priority < 1 or new_priority > 10:
                    messagebox.showwarning("Priority Error", "Priority must be between 1 and 10!")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Priority must be an integer (1-10)!")
                return

            cursor.execute("UPDATE tasks SET title = ?, priority = ?, deadline = ? WHERE id = ?",
                           (new_title, new_priority, new_deadline.strftime("%m/%d/%y"), task_id))
            conn.commit()
            refresh_tasks()
            update_btn.destroy()

        update_btn = ttk.Button(root, text="Update Task", command=update_task, style="TButton")
        update_btn.grid(row=5, column=1, pady=10)

# Function to mark a task as completed
def complete_task():
    selected_task = listbox_pending.curselection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task to complete!")
        return

    task_id = listbox_pending.get(selected_task).split(".")[0]
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

# Function to delete a task
def delete_task():
    selected_task = listbox_pending.curselection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task to delete!")
        return

    task_id = listbox_pending.get(selected_task).split(".")[0]
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

# Create the main window
root = tk.Tk()
root.title("To-Do List with AI Recommendations")
root.geometry("800x600")
root.config(bg="#f0f0f0")  # Light background color

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10, width=20)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12), padding=5)
style.configure("TFrame", background="#f0f0f0")

# Create the UI elements with modern look
frame_input = ttk.Frame(root)
frame_input.pack(pady=20)

entry_title = ttk.Entry(frame_input, width=30, font=("Helvetica", 12))
entry_title.grid(row=0, column=1, padx=10, pady=5)
entry_priority = ttk.Entry(frame_input, width=10, font=("Helvetica", 12))
entry_priority.grid(row=1, column=1, padx=10, pady=5)

label_title = ttk.Label(frame_input, text="Task Title:")
label_title.grid(row=0, column=0, padx=10, pady=5)
label_priority = ttk.Label(frame_input, text="Priority (1-10):")
label_priority.grid(row=1, column=0, padx=10, pady=5)

label_deadline = ttk.Label(frame_input, text="Deadline:")
label_deadline.grid(row=2, column=0, padx=10, pady=5)

# DateEntry widget for the deadline
entry_deadline = DateEntry(frame_input, width=12, background='darkblue', foreground='white', font=('Helvetica', 12))
entry_deadline.grid(row=2, column=1, padx=10, pady=5)

button_add = ttk.Button(root, text="Add Task", command=add_task, style="TButton")
button_add.pack(pady=10)

frame_listbox = ttk.Frame(root)
frame_listbox.pack(pady=10)

listbox_pending = tk.Listbox(frame_listbox, height=8, width=50, font=("Helvetica", 12), selectmode=tk.SINGLE)
listbox_pending.grid(row=0, column=0, padx=10, pady=5)

listbox_completed = tk.Listbox(frame_listbox, height=8, width=50, font=("Helvetica", 12), selectmode=tk.SINGLE)
listbox_completed.grid(row=0, column=1, padx=10, pady=5)

# Buttons for additional actions
button_edit = ttk.Button(root, text="Edit Task", command=edit_task, style="TButton")
button_edit.pack(pady=5)

button_complete = ttk.Button(root, text="Complete Task", command=complete_task, style="TButton")
button_complete.pack(pady=5)

button_delete = ttk.Button(root, text="Delete Task", command=delete_task, style="TButton")
button_delete.pack(pady=5)

# AI suggestions label
label_ai_suggestions = ttk.Label(root, text="AI Suggested Tasks:\n", style="TLabel")
label_ai_suggestions.pack(pady=10)

# Refresh the task list initially
refresh_tasks()

root.mainloop()
