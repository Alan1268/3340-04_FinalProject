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


def show_fields(*args):
    """ Show the Admin and Password fields when a role is selected. """
    if drop_var.get() in ["Admin", "Worker"]:  # If a valid role is selected
        admin_label.grid(row=3, column=0, columnspan=2, pady=5)  # Show "Admin"
        username_label.grid(row=4, column=0, pady=5, padx=0)  # Show username label
        password_label.grid(row=6, column=0, pady=5, padx=0)  # Show password label
        item_user.grid(row=5, column=0, columnspan=2, padx =20)  # Show password entry
        item_password.grid(row=7, column=0, columnspan=2, padx =20)  # Show password entry
        enter_button = Button(root, text="Enter")
        enter_button.grid(row=8, column=0, columnspan=2, pady=10)
        drop_menu.grid(row=10,column=0,columnspan = 2, padx = 20, pady = 60)


###### Widgets ####################

label = Label(root, text="Welcome").grid(row=1,column=0,columnspan = 2, padx = 20, pady= 20)

button = Button(root, text="Click Here", command=on_click)

# Admin Label 
admin_label = Label(root, text="Admin")
admin_label.grid(row=3, column=0, columnspan=2, pady=5)
admin_label.grid_remove()  # Hide it at the start

# Labels for Username and Password (Hidden initially)
username_label = Label(root, text="Enter Username:")
username_label.grid_remove()  # Hide initially

password_label = Label(root, text="Enter Password:")
password_label.grid_remove()  # Hide initially
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


#Drop Menu Setup
drop_var = StringVar()
drop_var.set("Choose Your Role")
drop_menu = OptionMenu(root,drop_var,"Admin","Worker")
drop_menu.grid(row=4,column=0,columnspan = 2, padx = 20)
drop_var.trace_add("write", show_fields)



#Call the main loop for displaying the root window
root.mainloop()
