from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter.messagebox import showinfo
import json

#headings for the data table tree
data_table_headings = ("Resource","Description","Date loaned","status")

#opens the json file Items and reads the saved list inside and deserializes to recognize the information as a list format
with open("library/Version 1/Users.json", "r") as pp:
    User_list = json.load(pp)
    pp.close()

#creating the root window
root = Tk()
root.title("Resource Manager")
root.geometry("840x380")

#creating objects
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def new_list(self):
        global User_list
        with open("library/Version 1/Users.json", "r") as User_list:
            User_add = json.load(User_list)

        User_add[self.username] = self.password

        with open("library/Version 1/Users.json", "w") as User_list:
            json.dump(User_add, User_list)
        
            
        new_list = open(f"library/Version 1/{self.username}.json", "x")
        new_list.write("[]")
        new_list.close()

        with open("library/Version 1/Users.json", "r") as pp:
            User_list = json.load(pp)
            pp.close()


#creating functions
#functions used to switch between frames by raising them ontop of each other
def switch_add_frame():
    add_frame.tkraise()
    add_bottom_frame.tkraise()

def switch_center_Frame():
    center_frame.tkraise()
    bottom_frame.tkraise()
    access_frame.tkraise()

#function to create lists
def open_user_lst():
    global lst
    with open(f"library/Version 1/{user_username}.json", "r") as fp:
        lst = json.load(fp)
        fp.close()

#checking variables to sign in
def signin():
    global lst
    global user_username
    if not username_entry.get():
        errors_lbl.config(text="please enter a username or create a new account")
        return  #returns to the if statement above
    else:
        user_username = username_entry.get()
        user_username = user_username.lower().strip()

    if not password_entry.get():
        errors_lbl.config(text="please enter the password")
        return
    else:
        user_password = password_entry.get()

    if user_username in User_list:
        if user_password == User_list[user_username]:
            with open(f"library/Version 1/{user_username}.json", "r") as fp:
                lst = json.load(fp)
            reload_data_table()
            switch_center_Frame()
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            errors_lbl.config(text="...")
        else:
            errors_lbl.config(text="password does not match with username")
            password_entry.delete(0, END)
    else:
        errors_lbl.config(text="username was not found in the database")

def create_user():
    if not add_username_entry.get():
        add_errors_lbl.config(text="please enter a username")
        return  #returns to the if statement above
    else:
        add_username = add_username_entry.get()
        add_username = add_username.lower().strip()     #makes all lowercase and strips off the spaces off the ends

    if not add_password_entry.get():
        add_errors_lbl.config(text="please enter the password")
        return
    else:
        add_password = add_password_entry.get()

    if add_username in User_list:
        add_errors_lbl.config(text="This username has already been taken")
        add_username_entry.delete(0, END)
        add_password_entry.delete(0, END)
    else:
        new_user = User(add_username, add_password)
        new_user.new_list()
        login_frame.tkraise()


def get_data():
    global add_resource, add_description, add_date, add_status, add_day_date, add_month_date, add_year_date
    description_entry = description_txt.get("1.0",'end-1c')
    #the if statement is used to check if the user has enetered anything
    if not resource_entry.get():
        messagebox.showerror("error", "please enter the resource name")
        return  #returns to the if statement above
    else:
        add_resource = resource_entry.get()
        resource_entry.delete(0, END)     #deletes text in entry from start to end of characters

    if not description_entry:
        messagebox.showerror("error", "please enter the description of the resource")
        return
    else:
        add_description = description_entry
        description_txt.delete("1.0", "end-1c")     #deletes text in entry from start to end of characters

    if not date_day_entry.get():
        messagebox.showerror("error", "please enter todays day")
        return
    else:
        add_day_date = date_day_entry.get()
        date_day_entry.delete(0, END)     #deletes text in entry from start to end of characters

    if not date_month_entry.get():
        messagebox.showerror("error", "please enter todays month")
        return
    else:
        add_month_date = date_month_entry.get()
        date_month_entry.delete(0, END)     #deletes text in entry from start to end of characters
        
    if not date_year_entry.get():
        messagebox.showerror("error", "please enter todays year")
        return
    else:
        add_year_date = date_year_entry.get()
        date_year_entry.delete(0, END)     #deletes text in entry from start to end of characters

    if not status_select.get():
        messagebox.showerror("error", "please enter the current status of the resource")
        return
    else:
        add_status = status_select.get()
        status_select.delete(0, END)     #deletes text in entry from start to end of characters
    #formats the add_date variable with the corresponding dates entered
    add_date = (f"{add_day_date}/{add_month_date}/{add_year_date}")

#the function used to append the used inputs in the entries into the viewtree widget
def append_add():
    get_data()
    #appends the gathered variables to the external file
    lst.append([add_resource, add_description, add_date, add_status])

    #opens up the json file to write and read
    with open(f"library/Version 1/{user_username}.json", "r+") as fp:
        json.dump(lst, fp)      #uses the dump function to add the new data
    
    reload_data_table()     #reloads the viewtree widget datatable with the added information
    switch_center_Frame()

#creating the main frames
login_frame = Frame(root, width=800, height=400, pady=20)
add_user_frame = Frame(root, width=800, height=400, pady=20)
top_frame = Frame(root, width=800, height=100, pady=3)
access_frame = Frame(root, width=800, height=130)
center_frame = Frame(root, width=800, height=225)
bottom_frame = Frame(root, width=800, height=50, pady=10)
add_frame = Frame(root, width=800, height=225, pady=20)
add_bottom_frame = Frame(root, width=800, height=50, pady=10)

#formatting the containers/frames into grids
root.grid_rowconfigure((0,1,2,3,4), weight=1)
root.grid_columnconfigure(1, weight=1)

login_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
login_frame.grid_columnconfigure((0,1), weight=1)

add_user_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
add_user_frame.grid_columnconfigure((0,1), weight=1)

top_frame.grid_rowconfigure(1, weight=1)
top_frame.grid_columnconfigure(1, weight=1)

access_frame.grid_rowconfigure(0, weight=1)
access_frame.grid_columnconfigure((0,1), weight=1)

center_frame.grid_rowconfigure(0, weight=1)
center_frame.grid_columnconfigure((0,1), weight=1)

bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_columnconfigure((0,1,2), weight=1)

add_frame.grid_rowconfigure((0,1,2,3,4,6,7), weight=1)
add_frame.grid_columnconfigure((0,1,2), weight=1)

add_bottom_frame.grid_rowconfigure(1, weight=1)
add_bottom_frame.grid_columnconfigure((0,1), weight=1)

top_frame.grid(row=0, sticky="ew")
login_frame.grid(row=1, sticky="nsew", rowspan=4, columnspan=2)
add_user_frame.grid(row=1, sticky="nsew", rowspan=4, columnspan=2)
access_frame.grid(row=1, sticky="ew")
center_frame.grid(row=2, sticky="nsew")
bottom_frame.grid(row=4, sticky="nsew")
add_frame.grid(row=2, sticky="nsew")
add_bottom_frame.grid(row=4, sticky="nsew")

#creating widgets for the login frame
#Labels
username_lbl = Label(login_frame, text="Username:")
password_lbl = Label(login_frame, text="password:")
errors_lbl = Label(login_frame, text="")

#entries
username_entry = Entry(login_frame)
password_entry = Entry(login_frame)

#buttons
signin_button = Button(login_frame, text="login", command=signin, width=10)
new_user_button = Button(login_frame, text="create new account" ,command=lambda: add_user_frame.tkraise())

#formatting the widgets for the login frame
#Labels
username_lbl.grid(row=0,column=0,sticky="se")
password_lbl.grid(row=1,column=0,sticky="e")
errors_lbl.grid(row=2, column=0, columnspan=2, pady=10, sticky="s")

#entries
username_entry.grid(row=0,column=1,sticky="sw")
password_entry.grid(row=1,column=1,sticky="w")

#buttons
signin_button.grid(row=3,column=0, columnspan=2, sticky="n")
new_user_button.grid(row=4, column=0, columnspan=2)

#creating widgets for add user frame
#labels
add_user_lbl = Label(add_user_frame, text="Create new account")
add_username_lbl = Label(add_user_frame, text="Username:")
add_password_lbl = Label(add_user_frame, text="password:")
conpassword_lbl = Label(add_user_frame, text="confirm password:")
add_errors_lbl = Label(add_user_frame, text="")


#entries
add_username_entry = Entry(add_user_frame)
add_password_entry = Entry(add_user_frame)
conpassword_entry = Entry(add_user_frame)

#buttons
create_user_button = Button(add_user_frame, text="create user", command=create_user)
return_btn = Button(add_user_frame, text="go back", command=lambda: login_frame.tkraise())

#formating widgets for add user frame
#labels
add_user_lbl.grid(row=0, column=0, columnspan=2)
add_username_lbl.grid(row=1,column=0, sticky="e")
add_password_lbl.grid(row=2,column=0, sticky="e")
add_errors_lbl.grid(row=3, column=0, columnspan=2)

#entries
add_username_entry.grid(row=1,column=1, sticky="w")
add_password_entry.grid(row=2,column=1, sticky="w")

#buttons
create_user_button.grid(row=4, column=0, columnspan=2)
return_btn.grid(row=5, column=0, columnspan=2)

#creating widgets for the top frame
title = Label(top_frame, text="Resource Manager", font = ("arial",18))
logo = Label(top_frame, text ="logo go\n here", font = ("arial",10))
credit = Label(top_frame, text ="by Leo Jeon", font = ("arial",10))


#formatting the widgets for the top frame
title.grid(row=0, column=1, sticky="NESW")
logo.grid(row=0, column=1, sticky="W")
credit.grid(row=0, column=1, sticky="E")

#creaing widgets for access frame
home_button = Button(access_frame, text = "Home", font = ("arial",14), borderwidth=0, command=switch_center_Frame)
sign_out_button = Button(access_frame, text = "sign out", font = ("arial",14), borderwidth=0, command=lambda: login_frame.tkraise())

#formatting the widgets for the access frame
home_button.grid(row=0, column=0, padx = 20)
sign_out_button.grid(row=0, column=1, padx = 20)

#creaing widgets for center frame
#setting up the widget tree and assigning headings
def reload_data_table():        #reason for in a function is to reload added data
    global data_table
    data_table = ttk.Treeview(center_frame, columns=data_table_headings, show="headings")
    center_frame_scrollbar = ttk.Scrollbar(center_frame, orient=VERTICAL, command=data_table.yview)

    #creating headings for the data_table
    data_table.heading("Resource", text="Resource") 
    data_table.heading("Description", text="Description")
    data_table.heading("Date loaned", text="Date loaned")
    data_table.heading("status", text="status")

    #inserting the values into the viewtree
    for resource in lst:
        data_table .insert("", END, values=resource)

    #formatting the widgets for the center frame
    data_table.configure(yscroll=center_frame_scrollbar.set)
    center_frame_scrollbar.grid(row=0, column=1, sticky="nesw")
    data_table.grid(row=0, column=0, sticky="nesw", padx=(20,0))

#creaing widgets for bottom frame
add_data = Button(bottom_frame, text = "add data", command=switch_add_frame)

#formatting the widgets for the bottom frame
add_data.grid(row=0, column=1, padx = (10,10))

#creating widgets for add frame
#labels
resource_entry_lbl = Label(add_frame, text="resource name:")
description_entry_lbl = Label(add_frame, text="description of resource:")
date_entry_lbl = Label(add_frame, text="date: (dd/mm/yyyy)")
status_select_lbl = Label(add_frame, text="status:")

#entries
resource_entry = Entry(add_frame)
description_txt = Text(add_frame, width = 30, height = 4, font=("arial", 10))
date_day_entry = Entry(add_frame, width = 3)
date_month_entry = Entry(add_frame, width = 3)
date_year_entry = Entry(add_frame, width = 6)

#combobox
status_options = ["borrowed", "returned", "lost"]
statusVar = StringVar()

status_select = Combobox(add_frame, state="readonly", values = status_options, textvariable= statusVar)


#formatting the widgets for the add frame
#labels
resource_entry_lbl.grid(row=0, column=1, pady=(10,0))
description_entry_lbl.grid(row=2, column=1)
date_entry_lbl.grid(row=4, column=1)
status_select_lbl.grid(row=6, column=1)

#entries
resource_entry.grid(row=1, column=1)
description_txt.grid(row=3, column=1)
date_day_entry.grid(row=5, column=1, padx=(0,60))
date_month_entry.grid(row=5, column=1, padx=5)
date_year_entry.grid(row=5, column=1, padx=(80,0))
status_select.grid(row=7, column=1)

#creating widgets for add bottom frame
#button
return_to_center_btn = Button(add_bottom_frame, text = "Go back", command=switch_center_Frame)
add_btn = Button(add_bottom_frame, text = "Add to library", command=append_add)

#formatting the widgets for the add bottom frame
#button
return_to_center_btn.grid(row=0, column=0, sticky="e", padx = 30)
add_btn.grid(row=0, column=1, sticky="w", padx = 30)

#calling functions
login_frame.tkraise()
root.mainloop() 
