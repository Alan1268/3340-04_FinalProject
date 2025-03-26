# Import the required module from tkinter for GUI
from tkinter import *

# Create the main application window
root = Tk()
root.geometry("400x400")

# Initialize an empty list to store tasks
tasks = []

# Function to add a task to the list
def add_task():
    task = task_entry.get()
    if task:
        tasks.append(task)
        task_listbox.insert(END, task)
        task_entry.delete(0, END)
        
# Create an entry widget for user input
task_entry = Entry(root, width=40)
task_entry.pack()

# Create a button to add tasks to the list
add_button = Button(root, text="Add Task", command=add_task)
add_button.pack()

# Create a listbox to display added tasks
task_listbox = Listbox(root, width=50, height=10)
task_listbox.pack()

root.mainloop()
