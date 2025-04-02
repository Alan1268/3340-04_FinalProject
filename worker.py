
import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("900x650")  

        self.lists = {}  
        self.current_list_name = None
        self.load_lists()  

        self.list_label = tk.Label(root, text="Select a List", font=("Arial", 14))
        self.list_label.pack()

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack()
        self.listbox.bind("<ButtonRelease-1>", self.select_list)  

        self.task_listbox = tk.Listbox(root, width=80, height=15)
        self.task_listbox.pack()
        self.task_listbox.bind("<Double-Button-1>", self.show_description)  


        self.complete_button = tk.Button(root, text="Mark as Done", command=self.mark_as_done)
        self.complete_button.pack()


        self.save_button = tk.Button(root, text="Save Lists", command=self.save_lists)
        self.save_button.pack()

        self.load_lists_to_listbox()  

    def add_task(self):
        if not self.current_list_name:
            messagebox.showerror("Error", "Please select or create a list first.")
            return

        task = simpledialog.askstring("Task Name", "Enter task name:")
        if task:
            due_date = simpledialog.askstring("Due Date", "Enter due date:")
            priority = simpledialog.askstring("Priority", "Enter priority (Low, Medium, High):")
            assigned = simpledialog.askstring("Assigned to", "Enter assigned names:")
            description = simpledialog.askstring("Task Description", "Enter task description:")

            task_info = {
                "task": task,
                "due_date": due_date,
                "priority": priority,
                "assigned": assigned,
                "description": description,
                "completed": False
            }

            self.lists[self.current_list_name].append(task_info)
            self.update_task_listbox()
            self.save_lists()


    def mark_as_done(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            self.lists[self.current_list_name][index]["completed"] = True
            self.update_task_listbox()
            self.save_lists()



    def show_description(self, event):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            task_info = self.lists[self.current_list_name][index]
            description = task_info.get("description", "No description available.")
            messagebox.showinfo("Task Description", f"Task: {task_info['task']}\n\nDescription:\n{description}")


            if messagebox.askyesno("Delete List", f"Are you sure you want to delete '{list_name}'?"):
                del self.lists[list_name]
                self.current_list_name = None
                self.load_lists_to_listbox()
                self.update_task_listbox()
                self.save_lists()

    def select_list(self, event):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.current_list_name = self.listbox.get(index)
            self.list_label.config(text=f"Current List: {self.current_list_name}")
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        if self.current_list_name:
            for task_info in self.lists[self.current_list_name]:
                task_text = f"{task_info['task']} (Due: {task_info['due_date']}, Priority: {task_info['priority']}, Assigned: {task_info['assigned']})"
                if task_info["completed"]:
                    task_text += " ✔"
                self.task_listbox.insert(tk.END, task_text)

    def load_lists_to_listbox(self):
        self.listbox.delete(0, tk.END)
        for list_name in self.lists.keys():
            self.listbox.insert(tk.END, list_name)

    def save_lists(self):
        with open("todo_lists.json", "w") as file:
            json.dump(self.lists, file)

    def load_lists(self):
        try:
            with open("todo_lists.json", "r") as file:
                self.lists = json.load(file)
        except FileNotFoundError:
            self.lists = {} 


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()