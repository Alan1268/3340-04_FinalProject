import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
def init_db():
    dataConnector = sqlite3.connect('ListData.db')
    cursor = dataConnector.cursor()
    
    # Create tables
    cursor.execute(""" CREATE TABLE IF NOT EXISTS lists (
                list_name TEXT PRIMARY KEY
    )""")

    cursor.execute(""" CREATE TABLE IF NOT EXISTS tasks (
                task_name TEXT PRIMARY KEY,
                list_name TEXT,
                due_date TEXT,
                assigned_to TEXT,
                completed BOOLEAN,
                description TEXT,
                FOREIGN KEY(list_name) REFERENCES lists(list_name)
    )""")

    dataConnector.commit()
    dataConnector.close()
    
class ToDoApp:
    def __init__(self, root, user_role):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("900x650")
        self.user_role = user_role  

        init_db()  # Ensure database is initialized

        # GUI Components
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

        self.load_lists_to_listbox()
        self.apply_role_restrictions()
        
        self.edit_button = tk.Button(root, text="Edit Selected Task", command=self.edit_task)
        self.edit_button.pack()

    def apply_role_restrictions(self):
        if self.user_role == "Assignee":
            self.add_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)
            self.new_list_button.config(state=tk.DISABLED)
            self.remove_list_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)

    def create_new_list(self):
        new_list_name = simpledialog.askstring("New List", "Enter new list name:")
        if new_list_name:
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            cursor.execute("INSERT INTO lists (list_name) VALUES (?)", (new_list_name,))
            dataConnector.commit()
            dataConnector.close()
            self.load_lists_to_listbox()

    def load_lists_to_listbox(self):
        dataConnector = sqlite3.connect('ListData.db')
        cursor = dataConnector.cursor()

        # Fetch all the contacts from the database
        cursor.execute("SELECT list_name FROM lists")
        contacts = cursor.fetchall()

        # Clear the listbox before displaying new data
        self.listbox.delete(0, tk.END)

        # Insert each contact into the listbox
        for list_name in contacts:
            self.listbox.insert(tk.END, list_name[0])  # contact[0] contains the list_name
        dataConnector.close()
        
    def remove_list(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            list_name = self.listbox.get(index)

        if messagebox.askyesno("Delete List", f"Are you sure you want to delete '{list_name}'?"):
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()

            # Remove tasks associated with the list first (to avoid foreign key constraint issues)
            cursor.execute("DELETE FROM tasks WHERE list_name = ?", (list_name,))

            # Now remove the list itself
            cursor.execute("DELETE FROM lists WHERE list_name = ?", (list_name,))

            dataConnector.commit()
            dataConnector.close()

            self.current_list_name = None
            self.load_lists_to_listbox()  # Refresh listbox
            self.update_task_listbox()  # Clear task listbox

    def select_list(self, event):
        selected = self.listbox.curselection()
        if selected:
            self.current_list_name = self.listbox.get(selected[0])
            self.list_label.config(text=f"Current List: {self.current_list_name}")
            self.update_task_listbox()

    def add_task(self):
        if not self.current_list_name:
            messagebox.showerror("Error", "Please select or create a list first.")
            return
        task_window = tk.Toplevel(self.root)
        task_window.title("Add New Task")
        task_window.geometry("400x400")

        tk.Label(task_window, text="Task Name:").pack(pady=5)
        task_entry = tk.Entry(task_window, width=40)
        task_entry.pack()

        tk.Label(task_window, text="Due Date:").pack(pady=5)
        due_date_entry = tk.Entry(task_window, width=40)
        due_date_entry.pack()

        tk.Label(task_window, text="Assigned To:").pack(pady=5)
        assigned_entry = tk.Entry(task_window, width=40)
        assigned_entry.pack()

        tk.Label(task_window, text="Description:").pack(pady=5)
        description_text = tk.Text(task_window, height=5, width=40)
        description_text.pack()
        def save_task():
            task = task_entry.get()
            due_date = due_date_entry.get()
            assigned = assigned_entry.get()
            description = description_text.get("1.0", tk.END).strip()

            if not task:
                messagebox.showerror("Error", "Task name is required.")
                return

            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            try:
                cursor.execute("""INSERT INTO tasks (task_name, list_name, due_date, assigned_to, completed, description) 
                                  VALUES (?, ?, ?, ?, ?, ?)""",
                               (task, self.current_list_name, due_date, assigned, False, description))
                dataConnector.commit()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Task with this name already exists.")
            finally:
                dataConnector.close()
                self.update_task_listbox()
                task_window.destroy()
        save_button = tk.Button(task_window, text="Save Task", command=save_task)
        save_button.pack(pady=10)

    def mark_as_done(self):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
        
        # Get the task name from the task listbox
        task_text = self.task_listbox.get(index)
        task_name = task_text.split(" (")[0]  # Get task name from formatted string
        
        dataConnector = sqlite3.connect('ListData.db')
        cursor = dataConnector.cursor()

        # Update the 'completed' status of the task in the database
        cursor.execute("UPDATE tasks SET completed = ? WHERE task_name = ? AND list_name = ?", 
                       (True, task_name, self.current_list_name))
        dataConnector.commit()
        dataConnector.close()

        self.update_task_listbox()
        
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        if self.current_list_name:
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            cursor.execute("SELECT task_name, due_date, assigned_to, completed FROM tasks WHERE list_name = ?", 
                           (self.current_list_name,))
            for task_name, due_date, assigned_to, completed in cursor.fetchall():
                task_text = f"{task_name} (Due: {due_date}, Assigned: {assigned_to})"
                if completed:
                    task_text += " ✔"
                self.task_listbox.insert(tk.END, task_text)
            dataConnector.close()
    def edit_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        task_name = self.task_listbox.get(selected[0]).split(" (")[0]

        dataConnector = sqlite3.connect('ListData.db')
        cursor = dataConnector.cursor()
        cursor.execute("""SELECT due_date, assigned_to, description 
                      FROM tasks WHERE task_name = ? AND list_name = ?""",
                   (task_name, self.current_list_name))
        result = cursor.fetchone()
        dataConnector.close()

        if not result:
            messagebox.showerror("Error", "Task not found in database.")
            return

        due_date, assigned_to, description = result

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x400")

        tk.Label(edit_window, text="Task Name:").pack(pady=5)
        task_entry = tk.Entry(edit_window, width=40)
        task_entry.insert(0, task_name)
        task_entry.pack()

        tk.Label(edit_window, text="Due Date:").pack(pady=5)
        due_date_entry = tk.Entry(edit_window, width=40)
        due_date_entry.insert(0, due_date)
        due_date_entry.pack()

        tk.Label(edit_window, text="Assigned To:").pack(pady=5)
        assigned_entry = tk.Entry(edit_window, width=40)
        assigned_entry.insert(0, assigned_to)
        assigned_entry.pack()

        tk.Label(edit_window, text="Description:").pack(pady=5)
        description_text = tk.Text(edit_window, height=5, width=40)
        description_text.insert("1.0", description)
        description_text.pack()

        def save_edits():
            new_task_name = task_entry.get()
            new_due_date = due_date_entry.get()
            new_assigned_to = assigned_entry.get()
            new_description = description_text.get("1.0", tk.END).strip()

            if not new_task_name:
                messagebox.showerror("Error", "Task name cannot be empty.")
                return

            try:
                conn = sqlite3.connect('ListData.db')
                cursor = conn.cursor()

            # If task name changed, ensure no name conflict
                if new_task_name != task_name:
                    cursor.execute("SELECT task_name FROM tasks WHERE task_name = ?", (new_task_name,))
                    if cursor.fetchone():
                        messagebox.showerror("Error", "A task with the new name already exists.")
                        return

            # Update task
                cursor.execute("""UPDATE tasks 
                              SET task_name = ?, due_date = ?, assigned_to = ?, description = ?
                              WHERE task_name = ? AND list_name = ?""",
                           (new_task_name, new_due_date, new_assigned_to, new_description,
                            task_name, self.current_list_name))
                conn.commit()
            finally:
                conn.close()
                self.update_task_listbox()
                edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save Changes", command=save_edits)
        save_button.pack(pady=10)
    def remove_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_name = self.task_listbox.get(selected[0]).split(" (")[0]
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_name = ?", (task_name,))
            dataConnector.commit()
            dataConnector.close()
            self.update_task_listbox()

    def mark_as_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_name = self.task_listbox.get(selected[0]).split(" (")[0]
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            cursor.execute("UPDATE tasks SET completed = ? WHERE task_name = ?", (True, task_name))
            dataConnector.commit()
            dataConnector.close()
            self.update_task_listbox()
            
    def show_description(self, event):
        selected = self.task_listbox.curselection()
        if selected and self.current_list_name:
            index = selected[0]
            task_name = self.task_listbox.get(index).split(" (")[0]
        
            dataConnector = sqlite3.connect('ListData.db')
            cursor = dataConnector.cursor()
            cursor.execute("SELECT description FROM tasks WHERE task_name = ? AND list_name = ?", 
                       (task_name, self.current_list_name))
            result = cursor.fetchone()
            dataConnector.close()

            description = result[0] if result else "No description available."
            messagebox.showinfo("Task Description", f"Task: {task_name}\n\nDescription:\n{description}")


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Enter your username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()
    
    def login(self):
        username = self.username_entry.get()

        # If username is provided, fetch the role from the database
        if username:
            user_role = self.get_user_role(username)
            if user_role:
                self.root.destroy()
                main_app = tk.Tk()
                app = ToDoApp(main_app, user_role)
                main_app.mainloop()
            else:
                messagebox.showerror("Error", "User not found or incorrect username.")
        else:
            messagebox.showerror("Error", "Please enter your username.")

    def get_user_role(self, username):
        """Fetch the role of the user from the database."""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Query the database for the user's role
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # Return the role if found
        return None  # Return None if no user is found with that username


if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()
