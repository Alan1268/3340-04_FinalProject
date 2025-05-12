import subprocess
import os
import sqlite3
from tkinter import *
from tkinter import messagebox



# Connect to SQLite3 database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT,
        password TEXT,
        role TEXT
    )
''')
conn.commit()

# Creating the main window widget
root = Tk()
root.geometry("500x500")  # Adjusted window size

# Configure grid columns to center content
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)

###### Methods ####################

def log_in():
    username = item_user.get()
    password = item_password.get()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login successful!")
        run_Task2()
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def run_Task2():
    if drop_var.get() == "Sign In":
        script_path = "worker.py"
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])

def sign_up():
    username = item_user.get()
    password = item_password.get()
    confirm = item_repassword.get()
    email = item_email.get()
    role = role_var.get()

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, password, role))
        conn.commit()
        messagebox.showinfo("Success", "Signup successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def run_Task():
    if drop_var.get() == "Sign In":
        log_in()
    elif drop_var.get() == "Sign Up":
        sign_up()

def show_fields(*args):

    selected_role = role_var.get()

    if drop_var.get() == "Sign In":
        root.geometry("400x400")
        
        # Hide Sign Up fields
        email_label.grid_remove()
        item_email.grid_remove()
        item_repassword.grid_remove()
        reconfirm_password_label.grid_remove()
        role_label.grid_remove()
        role_menu.grid_remove()
        enter1_button.grid_remove()  # <--- Hide Sign Up's button

        # Show Sign In fields
        admin_label.config(text="Log In")
        admin_label.grid(row=3, column=1, pady=5)
        username_label.grid(row=4, column=1, pady=5, padx=20, sticky="w")
        item_user.grid(row=5, column=1, padx=20, sticky="ew")
        password_label.grid(row=6, column=1, pady=5, padx=20, sticky="w")
        item_password.grid(row=7, column=1, padx=20, sticky="ew")

        enter_button.grid(row=12, column=1, pady=10, sticky="ew")
        drop_menu.grid(row=13, column=1, padx=20, pady=60)

    elif drop_var.get() == "Sign Up":
        root.geometry("400x500")
        
        # Hide Sign In fields
        enter_button.grid_remove()  # <--- Hide Sign In's button

        # Show Sign Up fields
        admin_label.config(text=selected_role)
        admin_label.grid(row=3, column=1, pady=5)
        email_label.grid(row=4, column=1, pady=5, padx=20, sticky="w")
        item_email.grid(row=5, column=1, padx=20, sticky="ew")
        username_label.grid(row=6, column=1, pady=5, padx=20, sticky="w")
        item_user.grid(row=7, column=1, padx=20, sticky="ew")
        password_label.grid(row=8, column=1, pady=5, padx=20, sticky="w")
        item_password.grid(row=9, column=1, padx=20, sticky="ew")
        reconfirm_password_label.grid(row=10, column=1, pady=5, padx=20, sticky="w")
        item_repassword.grid(row=11, column=1, padx=20, sticky="ew")

        role_label.grid(row=12, column=1, pady=5, padx=20, sticky="w")
        role_menu.grid(row=13, column=1, padx=20, pady=5, sticky="ew")

        enter1_button.grid(row=14, column=1, pady=10, sticky="ew")
        drop_menu.grid(row=15, column=1, padx=20, pady=20)
###### Widgets ####################

Label(root, text="Welcome").grid(row=1, column=1, padx=20, pady=20)

# Admin Label
admin_label = Label(root, text="Log In")
admin_label.grid_remove()

username_label = Label(root, text="Enter Username:")
username_label.grid_remove()

password_label = Label(root, text="Enter Password:")
password_label.grid_remove()

reconfirm_password_label = Label(root, text="Confirm Password:")
reconfirm_password_label.grid_remove()

email_label = Label(root, text="Enter Email:")
email_label.grid_remove()

item_email = Entry(root)
item_email.grid_remove()

item_user = Entry(root)
item_user.grid_remove()

item_password = Entry(root, show="*")
item_password.grid_remove()

item_repassword = Entry(root, show="*")
item_repassword.grid_remove()

# Role Label and Dropdown
role_label = Label(root, text="Select Role:")
role_label.grid_remove()

role_var = StringVar()
role_var.set("Sign Up")
role_menu = OptionMenu(root, role_var, "Assigner", "Assignee")
role_menu.grid_remove()

# Enter buttons
enter_button = Button(root, text="Enter", command=run_Task)
enter1_button = Button(root, text="Enter", command=run_Task)
# Initially hidden; shown by `show_fields`

# Drop Menu Setup
drop_var = StringVar()
drop_var.set("Log In")
drop_menu = OptionMenu(root, drop_var, "Sign In", "Sign Up")
drop_menu.grid(row=4, column=1, padx=20)
drop_var.trace_add("write", show_fields)


root.mainloop()
