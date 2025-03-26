#python code will be implemented here
from tkinter import *

root = Tk()
root.geometry("400x400")

tasks = []

def add_task():
    task = task_entry.get()
    if task:
        tasks.append(task)
        task_listbox.insert(END, task)
        task_entry.delete(0, END)

task_entry = Entry(root, width=40)
task_entry.pack()

add_button = Button(root, text="Add Task", command=add_task)
add_button.pack()

task_listbox = Listbox(root, width=50, height=10)
task_listbox.pack()

root.mainloop()
