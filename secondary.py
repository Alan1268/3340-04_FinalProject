import tkinter as tk
from tkcalendar import Calendar

# Initialize the main application window
root = tk.Tk()
root.geometry("400x500")  # Set the window size

# Dictionary to store tasks with dates
tasks = {}

#Adds a task to the selected date in the dictionary and updates the task list
def add_task():
    task = task_entry.get()  # Get the task from the entry field
    date = cal.get_date()  # Get the selected date from the calendar
    if task:  
        if date not in tasks:
            tasks[date] = []  # Create a list for the date if it doesn't exist
        tasks[date].append(task)  # Add the task to the list
        update_task_list(date)  # Update the displayed task list
        task_entry.delete(0, tk.END)  # Clear the entry field

def update_task_list(date):
    #Updates the task list display for the selected date
    task_listbox.delete(0, tk.END)  # Clear the listbox
    if date in tasks:
        for task in tasks[date]:  # Add tasks to the listbox
            task_listbox.insert(tk.END, task)

#Handles the date selection event and updates the task list.
def on_date_select(event):
    selected_date = cal.get_date()
    update_task_list(selected_date)

# Create and configure the calendar widget
cal = Calendar(root, selectmode='day')
cal.pack(pady=10)
cal.bind("<<CalendarSelected>>", on_date_select)  # Bind date selection event

# Create task entry field
task_entry = tk.Entry(root, width=40)
task_entry.pack()

# Create "Add Task" button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

# Create task list display area
task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack()

# Run the application event loop
root.mainloop()
