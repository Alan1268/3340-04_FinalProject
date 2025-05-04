import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class ToDoApp:
    def __init__(self, root, user_role):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("900x650")  
        self.user_role = user_role  # Store user role

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

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()
        
        self.remove_button = tk.Button(root, text="Remove Selected Task", command=self.remove_task)
        self.remove_button.pack()
        
        self.complete_button = tk.Button(root, text="Mark as Done", command=self.mark_as_done)
        self.complete_button.pack()

        self.new_list_button = tk.Button(root, text="Create New List", command=self.create_new_list)
        self.new_list_button.pack()

        self.remove_list_button = tk.Button(root, text="Remove Selected List", command=self.remove_list)
        self.remove_list_button.pack()

        self.save_button = tk.Button(root, text="Save Lists", command=self.save_lists)
        self.save_button.pack()

        self.load_lists_to_listbox()  

        self.apply_role_restrictions()
    
    def apply_role_restrictions(self):
        if self.user_role == "Assignee":
            self.add_button.pack_forget()
            self.remove_button.pack_forget()
            self.new_list_button.pack_forget()
            self.remove_list_button.pack_forget()
            self.save_button.pack_forget()


    def add_task(self):
        if not self.current_list_name:
            messagebox.showerror("Error", "Please select or create a list first.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Add New Task")
        popup.geometry("400x400")

        tk.Label(popup, text="Task Name:").pack()
        task_entry = tk.Entry(popup)
        task_entry.pack()

        tk.Label(popup, text="Due Date:").pack()
        due_date_entry = tk.Entry(popup)
        due_date_entry.pack()

        tk.Label(popup, text="Priority (Low, Medium, High):").pack()
        priority_entry = tk.Entry(popup)
        priority_entry.pack()

        tk.Label(popup, text="Assigned To:").pack()
        assigned_entry = tk.Entry(popup)
        assigned_entry.pack()

        tk.Label(popup, text="Description:").pack()
        description_text = tk.Text(popup, height=5, width=30)
        description_text.pack()

        def save_task():
            task = task_entry.get()
            due_date = due_date_entry.get()
            priority = priority_entry.get()
            assigned = assigned_entry.get()
            description = description_text.get("1.0", tk.END).strip()

            if task:
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
                popup.destroy()
            else:
                messagebox.showerror("Error", "Task name cannot be empty.")

        tk.Button(popup, text="Save Task", command=save_task).pack(pady=10)

    
    def mark_as_done(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            self.lists[self.current_list_name][index]["completed"] = True
            self.update_task_listbox()
            self.save_lists()

    def remove_task(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            del self.lists[self.current_list_name][index]
            self.update_task_listbox()
            self.save_lists()

    def mark_as_done(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            self.lists[self.current_list_name][index]["completed"] = True
            self.update_task_listbox()
            self.save_lists()

    def update_description(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            new_desc = simpledialog.askstring("Update Description", "Enter new description:")
            if new_desc:
                self.lists[self.current_list_name][index]["description"] = new_desc
                self.save_lists()

    def show_description(self, event):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            task_info = self.lists[self.current_list_name][index]
            description = task_info.get("description", "No description available.")
            messagebox.showinfo("Task Description", f"Task: {task_info['task']}\n\nDescription:\n{description}")

    def create_new_list(self):
        new_list_name = simpledialog.askstring("New List", "Enter new list name:")
        if new_list_name and new_list_name not in self.lists:
            self.lists[new_list_name] = []
            self.load_lists_to_listbox()
            self.save_lists()

    def remove_list(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            list_name = self.listbox.get(index)

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
    
    def show_description(self, event):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            task_info = self.lists[self.current_list_name][index]
            description = task_info.get("description", "No description available.")
            messagebox.showinfo("Task Description", f"Task: {task_info['task']}\n\nDescription:\n{description}")
    
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
                task_text = f"{task_info['task']} (Due: {task_info['due_date']}, Assigned: {task_info['assigned']})"
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

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x250")

        tk.Label(root, text="Enter your email:").pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        tk.Label(root, text="Enter your password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(root, text="Register New User", command=self.open_register_window)
        self.register_button.pack(pady=5)

        self.load_users()

    def load_users(self):
        try:
            with open("user_list.json", "r") as file:
                content = file.read().strip()
                if not content:
                    self.users = {}
                else:
                    self.users = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}


    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        user_info = self.users.get(email)
        if user_info and user_info["password"] == password:
            role = user_info["role"]
            self.root.destroy()
            main_app = tk.Tk()
            app = ToDoApp(main_app, role)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New User")
        register_window.geometry("400x450")

        tk.Label(register_window, text="Enter your email:").pack()
        email_entry = tk.Entry(register_window)
        email_entry.pack()

        tk.Label(register_window, text="Enter password:").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()

        tk.Label(register_window, text="Confirm password:").pack()
        confirm_password_entry = tk.Entry(register_window, show="*")
        confirm_password_entry.pack()

        tk.Label(register_window, text="Select Role:").pack()
        role_var = tk.StringVar(value="Assignee")
        tk.Radiobutton(register_window, text="Assigner", variable=role_var, value="Assigner").pack()
        tk.Radiobutton(register_window, text="Assignee", variable=role_var, value="Assignee").pack()

        def register_user():
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            role = role_var.get()

            if not email or not password or not confirm_password:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            if email in self.users:
                messagebox.showerror("Error", "User already exists.")
                return

            self.users[email] = {
                "password": password,
                "role": role
            }
            with open("user_list.json", "w") as file:
                json.dump(self.users, file)

            messagebox.showinfo("Success", "User registered successfully!")
            register_window.destroy()

        tk.Button(register_window, text="Register", command=register_user).pack(pady=10)

    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        user_info = self.users.get(email)
        if user_info and user_info["password"] == password:
            role = user_info["role"]
            self.root.destroy()
            main_app = tk.Tk()
            app = ToDoApp(main_app, role)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid email or password.")


if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()
