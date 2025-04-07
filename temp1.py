from tkinter import *
import sqlite3 

root = Tk()
root.title('Contact Info App')
root.geometry("400x550")
#################### Create the Data Base ###########################

#Create the connector
dataConnector = sqlite3.connect('ListData.db')

#Create Cursor
cursor = dataConnector.cursor()

#Create a table 

cursor.execute(""" CREATE TABLE IF NOT EXISTS lists (

			list_name text PRIMARY KEY
)""")


cursor.execute(""" CREATE TABLE IF NOT EXISTS tasks (

			task_name text PRIMARY KEY, list_name text, due_date text, Assigned_to text, completed boolean, description text, FOREIGN KEY(list_name) REFERENCES lists(list_name)
)""")

#################### Create Functions ###########################

def submit():
	dataConnector = sqlite3.connect('ListData.db')
	cursor = dataConnector.cursor()

	cursor.execute("INSERT INTO lists (list_name) VALUES (:list_name)",
                   {'list_name': list_name.get()})
    
	dataConnector.commit()
	dataConnector.close()

	list_name.delete(0,END)
def submittask():
    # Get the values from the input fields
    dataConnector = sqlite3.connect('ListData.db')
    cursor = dataConnector.cursor()
    
    task_name_value = task_name_entry.get()  # Example for task name
    list_name_value = list_name_entry.get()  # Example for list name
    selected_list_index = list_listbox.curselection()
    if not selected_list_index:
       print("No list selected!")
       return  # Prevent adding a task without a selected list
   
    list_name_value = list_listbox.get(selected_list_index)
    due_date_value = due_date_entry.get()    # Example for due date
    assigned_to_value = assigned_to_entry.get()  # Example for assigned person
    completed_value = completed_var.get()  # Boolean value (True/False)
    description_value = description_entry.get()  # Example for description

    # Open the database connection and create a cursor

    # Insert the task into the tasks table
    cursor.execute("""
        INSERT INTO tasks (task_name, list_name, due_date, Assigned_to, completed, description) 
        VALUES (:task_name, :list_name, :due_date, :Assigned_to, :completed, :description)
    """, {
        'task_name': task_name_value,
        'list_name': list_name_value,
        'due_date': due_date_value,
        'Assigned_to': assigned_to_value,
        'completed': completed_value,
        'description': description_value
    })

    # Commit the transaction and close the connection
    dataConnector.commit()
    dataConnector.close()

    # Clear the input fields after submission
    task_name_entry.delete(0, END)
    list_name_entry.delete(0, END)
    due_date_entry.delete(0, END)
    assigned_to_entry.delete(0, END)
    description_entry.delete(0, END)
    # Reset completed checkbox (if applicable)
    completed_var.set(False)
    
def show_lists():
    # Open the database connection and create a cursor
    dataConnector = sqlite3.connect('ListData.db')
    cursor = dataConnector.cursor()

    # Fetch all the contacts from the database
    cursor.execute("SELECT list_name FROM lists")
    contacts = cursor.fetchall()

    # Clear the listbox before displaying new data
    list_listbox.delete(0, END)

    # Insert each contact into the listbox
    for list_name in contacts:
        list_listbox.insert(END, list_name[0])  # contact[0] contains the list_name
    dataConnector.close()

def show_tasks():
    # Open the database connection and create a cursor
    dataConnector = sqlite3.connect('ListData.db')
    cursor = dataConnector.cursor()
    
    selected_list_index = list_listbox.curselection()
    
    if not selected_list_index:  # Check if no list is selected
      print("No list selected!")
      return  # Exit the function if no list is selected
    
    selected_list = list_listbox.get(list_listbox.curselection())
    # Fetch all the contacts from the database
    cursor.execute("SELECT task_name FROM tasks WHERE list_name = ?", (selected_list,))
    tasks = cursor.fetchall()

    # Clear the listbox before displaying new data
    task_listbox.delete(0, END)

    # Insert each contact into the listbox
    for task in tasks:
        task_listbox.insert(END, task[0])  # contact[0] contains the list_nam
    else:
       print("No tasks found for the selected list.")
    # Close the connection
    dataConnector.close()
    
def on_task_select(event):
    selected_task_index = task_listbox.curselection()  #Get the index of the selected task
    if selected_task_index:
       selected_task_name = task_listbox.get(selected_task_index)  # Get the task name
       print(f"Selected Task: {selected_task_name}")  # You can use this for further operations

       # Enable the edit button
       edit_button.config(state=NORMAL)

       # Fetch and display the details of the selected task
       dataConnector = sqlite3.connect('ListData.db')
       cursor = dataConnector.cursor()

       cursor.execute("SELECT * FROM tasks WHERE task_name = ?", (selected_task_name,))
       task_details = cursor.fetchone()  # Fetch the task details

       if task_details:
           # Display the task details
           task_name_label.config(text=f"Task Name: {task_details[0]}")
           due_date_label.config(text=f"Due Date: {task_details[2]}")
           assigned_to_label.config(text=f"Assigned To: {task_details[3]}")
           completed_label.config(text=f"Completed: {task_details[4]}")
           description_label.config(text=f"Description: {task_details[5]}")

       dataConnector.close()

def completetask():
    selected_task_index = task_listbox.curselection()  # Get the index of the selected task
    if selected_task_index:
        selected_task_name = task_listbox.get(selected_task_index)  # Get the task name
        print(f"Task to mark as completed: {selected_task_name}")

        # Connect to the database and update the 'completed' field for the selected task
        dataConnector = sqlite3.connect('ListData.db')
        cursor = dataConnector.cursor()

        try:
            cursor.execute("""
                UPDATE tasks 
                SET completed = 1 
                WHERE task_name = ?
            """, (selected_task_name,))
            dataConnector.commit()  # Commit the transaction
            print(f"Task '{selected_task_name}' marked as completed.")

            # Optionally, update the displayed task details to reflect the change
            show_tasks()

        except sqlite3.Error as e:
            print(f"Error updating task: {e}")

        finally:
            dataConnector.close()
#################### Create GUI ###########################

#### Create widgets
list_name = Entry(root, width = 50)

task_name_entry = Entry(root, width=50)
list_name_entry = Entry(root, width=50, state = DISABLED)
list_name_entry.grid(row = 1, column = 5)
due_date_entry = Entry(root, width=50)
assigned_to_entry = Entry(root, width=50)
description_entry = Entry(root, width=50)
completed_var = BooleanVar()
completed_checkbox = Checkbutton(root, text="Completed", variable=completed_var)
title_label = Label(root, text = "Lists")

list_listbox = Listbox(root, width=50, height=10)
task_listbox = Listbox(root, width=50, height=10)
task_listbox.grid(row=9, column=0, columnspan=2)
show_button = Button(root, text="Show All Lists", command=show_lists)
edit_button = Button(root, text="Show All Task", command = show_tasks)
edit_button.grid(row=2, column=4)
complete_task = Button(root, text = "Complete Task", command = completetask)
complete_task.grid(row = 9, column = 4)
# Create a label to show confirmation after adding a contact
confirmation_label = Label(root, text="", fg="green")
task_listbox.bind("<<ListboxSelect>>", on_task_select)
# Call Widgets
'''Add_label.grid(row = 8, column = 0)'''
title_label.grid(row = 0, column = 0, columnspan = 2)
list_name.grid(row=4, column=1)
'''list_label.grid(row=5, column=0)'''
confirmation_label.grid(row=2, column=0, columnspan=2)
show_button.grid(row=1, column=4)
list_listbox.grid(row=1, column=0, columnspan=2)
task_name_label = Label(root, text="Task Name:")
due_date_label = Label(root, text = "Due Date:")
assigned_to_label = Label(root, text = "Assigned to:")
completed_label = Label(root, text = "Completion status:")
description_label = Label(root, text = "Description:")
task_name_label.grid(row = 10, column = 0, columnspan =2)
due_date_label.grid(row = 11, column = 0, columnspan =2)
assigned_to_label.grid(row = 12, column = 0, columnspan =2)
completed_label.grid(row = 13, column = 0, columnspan =2)
description_label.grid(row = 14, column = 0, columnspan =2)

root.mainloop()
