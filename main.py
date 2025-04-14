import subprocess
import os
from tkinter import *

#Widget is a object with specific information or function

#Creating the main window widget
root = Tk()
root.geometry("400x400")

###### Methods ####################
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

def on_click():
	#label = Label(root, text="Click, Click, Click")
	label = Label(root, text=pie)
	label.grid(row=0,column=0,columnspan = 2, padx = 20)

def run_Task():
    if drop_var.get() == "Sign In":
        script_path = "worker.py"
        if os.path.exists(script_path):
            print(f"Running {script_path}...")
            subprocess.run(["python", script_path])
    else:
        if drop_var.get() == "Sign Up":
            script_path = "worker.py"
            if os.path.exists(script_path):
                print(f"Running {script_path}...")
                subprocess.run(["python", script_path])

def show_fields(*args):
    """ Show the Admin and Password fields when a role is selected. """
    role = drop_var.get()
    if drop_var.get() in ["Sign In"]:  # If a valid role is selected
        root.geometry("400x400")
        email_label.grid_remove()
        item_repassword.grid_remove()
        reconfirm_password_label.grid_remove()
        admin_label.config(text=role)
        admin_label.grid(row=3, column=0, columnspan=2, pady=5)  # Show "Admin"
        username_label.grid(row=4, column=0, pady=5, padx=0)  # Show username label
        password_label.grid(row=6, column=0, pady=5, padx=0)  # Show password label
        item_user.grid(row=5, column=0, columnspan=2, padx =20)  # Show password entry
        item_password.grid(row=7, column=0, columnspan=2, padx =20)  # Show password entry
        enter_button = Button(root, text="Enter", command=run_Task)
        enter_button.grid(row=12, column=0, columnspan=2, pady=10)
        drop_menu.grid(row=13,column=0,columnspan = 2, padx = 20, pady = 60)
    if drop_var.get() in ["Sign Up"]:
        root.geometry("400x450")
        admin_label.config(text=role)
        admin_label.grid(row=3, column=0, columnspan=2, pady=5)
        email_label.grid(row = 4, column = 0, pady = 5, padx = 0)
        reconfirm_password_label.grid(row =10, column = 0, pady = 5, padx = 0)
        item_repassword.grid(row=11, column=0, columnspan=2, padx =20)
        item_email.grid(row=5, column=0, columnspan = 2, padx = 20)
        username_label.grid(row=6, column=0, pady=5, padx=0)  # Show username label
        password_label.grid(row=8, column=0, pady=5, padx=0)  # Show password label
        item_user.grid(row=7, column=0, columnspan=2, padx =20)  # Show password entry
        item_password.grid(row=9, column=0, columnspan=2, padx =20)  # Show password entry
        enter1_button = Button(root, text="Enter")
        enter1_button.grid(row=12, column=0, columnspan=2, pady=10)
        drop_menu.grid(row=13,column=0,columnspan = 2, padx = 20, pady = 60)
        


###### Widgets ####################

label = Label(root, text="Welcome").grid(row=1,column=0,columnspan = 2, padx = 20, pady= 20)

button = Button(root, text="Click Here", command=on_click)

# Admin Label 

admin_label = Label(root, text="Log In")
admin_label.grid(row=3, column=0, columnspan=2, pady=5)
admin_label.grid_remove()  # Hide it at the start

# Labels for Username and Password (Hidden initially)
username_label = Label(root, text="Enter Username:")
username_label.grid_remove()  # Hide initially

password_label = Label(root, text="Enter Password: ")
password_label.grid_remove()  # Hide initially

reconfirm_password_label = Label(root, text="     Confirm Password:")
reconfirm_password_label.grid_remove()  # Hide initially

email_label = Label(root, text="Enter Email:        ")
email_label.grid_remove()  # Hide initially


#Email Entry
item_email = Entry(root)
item_email.insert(0, "")
item_email.grid(row=3, column=0, columnspan=2, sticky="ew")
item_email.grid_remove()  # Hide it at the start
#Username Entry
item_user = Entry(root)
item_user.insert(0, "")
item_user.grid(row=4, column=0, columnspan=2, sticky="ew")
item_user.grid_remove()  # Hide it at the start

# Password Entry
item_password = Entry(root)
item_password.insert(0, "")
item_password.grid(row=5, column=0, columnspan=2, sticky="ew")
item_password.grid_remove()  # Hide it at the start

item_repassword = Entry(root)
item_repassword.insert(0, "")
item_repassword.grid(row=5, column=0, columnspan=2, sticky="ew")
item_repassword.grid_remove()

#Drop Menu Setup
drop_var = StringVar()
drop_var.set("Log In")
drop_menu = OptionMenu(root,drop_var,"Sign In","Sign Up")
drop_menu.grid(row=4,column=0,columnspan = 2, padx = 20)
drop_var.trace_add("write", show_fields)



#Call the main loop for displaying the root window
root.mainloop()

