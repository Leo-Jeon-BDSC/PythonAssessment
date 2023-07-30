from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
import json
import os


#headings for the data table tree
status_options = ["borrowed", "returned", "lost"]

#opens the json file Items and reads the saved list inside and deserializes to recognize the information as a list format
with open("library/Version 3/Users.json", "r") as pp:
    User_list = json.load(pp)
    pp.close()

#creating the root window
root = Tk()
root.title("Resource Manager")
root.geometry("840x450")

#creating objects
class User:
    def __init__(self, username, password, email, status_config):
        self.username = username
        self.password = password
        self.email = email
        self.status_config = status_config


    def new_user(self):
        global User_list
        with open("library/Version 3/Users.json", "r") as User_list:
            User_add = json.load(User_list)

        User_add[self.username] = [self.password, self.email, self.status_config]

        with open("library/Version 3/Users.json", "w") as User_list:
            json.dump(User_add, User_list)
        
    def new_user_list(self):
        global User_list
        new_list = open(f"library/Version 3/{self.username}.json", "x")
        new_list.write("[]")
        new_list.close()

        with open("library/Version 3/Users.json", "r") as pp:
            User_list = json.load(pp)
            



#creating functions
#functions used to switch between frames by raising them ontop of each other
def switch_add_frame():
    add_resource_lbl.config(text="Add")
    add_resource_frame.tkraise()
    add_resource_bottom_frame.tkraise()

def switch_center_Frame():
    resource_frame.tkraise()
    resource_btm_frame.tkraise()
    access_frame.tkraise()
    status_select.set("")     
    resource_entry.delete(0, END)     #deletes text in entry from start to end of characters   
    description_txt.delete("1.0", "end-1c")     #deletes text in entry from start to end of characters
    date_day_entry.set("") 
    date_month_entry.set("")   
    date_year_entry.delete(0, END)

def clear_resource_entries():
    status_select.set("")     
    resource_entry.delete(0, END)     #deletes text in entry from start to end of characters   
    description_txt.delete("1.0", "end-1c")     #deletes text in entry from start to end of characters
    date_day_entry.set("") 
    date_month_entry.set("")   
    date_year_entry.delete(0, END)


def switch_edit_frame():
    global edit_item
    global selected_item
    try:
        selected_item = data_table.focus()
        edit_item = data_table.selection()[0]
        add_resource_lbl.config(text="Edit")
        chosen_row = data_table.item(selected_item)["values"]
        #enters the selected rows data into entries
        resource_entry.insert(END, chosen_row[0])
        description_txt.insert(END ,chosen_row[1])
        chosen_date = chosen_row[2]
        date_day_entry.set(chosen_date[0:2])
        date_month_entry.set(chosen_date[3:6])
        date_year_entry.insert(END, chosen_date[7:len(chosen_date)])
        status_select.set(chosen_row[3])
        #Raises the frames
        edit_resource_frame.tkraise()
        add_resource_frame.tkraise()
    except IndexError:
        messagebox.showerror("error", "please add or select a row")

#function to create lists
def open_user_lst():
    global lst
    with open(f"library/Version 3/{user_username}.json", "r") as pp:
        lst = json.load(pp)

#checking variables to sign in
def signin():
    global lst
    global user_username
    global status_options     

    with open("library/Version 3/Users.json", "r") as pp:
        User_list = json.load(pp)
        pp.close()

    if not username_entry.get():
        messagebox.showerror("error", "please enter a username or create a new account")
        return  #returns to the if statement above
    else:
        user_username = username_entry.get()
        user_username = user_username.lower().strip()

    if not password_entry.get():
        messagebox.showerror("error", "please enter the password")
        return
    else:
        user_password = password_entry.get() 

    if user_username in User_list:
        user_info = User_list[user_username]
        password1 = user_info[0]
        status_options = user_info[2]
        if user_password ==  password1:
            with open(f"library/Version 3/{user_username}.json", "r") as fp:
                lst = json.load(fp)
            reload_data_table()
            switch_center_Frame()
            username_entry.delete(0, END)
            password_entry.delete(0, END)
        else:
            messagebox.showerror("error", "password does not match with username")
            password_entry.delete(0, END)
            return
    else:
        messagebox.showerror("error", "username was not found in the database")
        return

def create_user():
    if not add_username_entry.get():
        messagebox.showerror("error", "please enter a username")
        return  #returns to the if statement above
    else:
        add_username = add_username_entry.get()
        add_username = add_username.lower().strip()

    if not add_password_entry.get():
        messagebox.showerror("error", "please enter the password")
        return
    else:
        if len(add_password_entry.get()) >= 7:
            add_password = add_password_entry.get()
        else:
            messagebox.showerror("error", "please enter a password at least 7 characters long")
            return
        
    if not conpassword_entry.get():
        messagebox.showerror("error", "please confirm your password")
        return
    else:
        conpassword = conpassword_entry.get()
        if conpassword == add_password:
            pass
        else:
            messagebox.showerror("error", "The passwords do not match")
            return
        pass 

    if not add_email_entry.get():
        messagebox.showerror("error", "please enter a email")
        return
    else:
        add_email = add_email_entry.get()

    if add_username in User_list:
        messagebox.showerror("error", "This username has already been taken")
        add_username_entry.delete(0, END)
        add_password_entry.delete(0, END)
        conpassword_entry.delete(0, END)
        add_email_entry.delete(0,END)
    else:
        default_status_config = ["borrowed", "returned", "lost"]
        new_user = User(add_username, add_password, add_email, default_status_config)
        new_user.new_user()
        new_user.new_user_list()
        login_frame.tkraise()

def update_user():
    global user_username
    if not settings_email_entry.get():
        messagebox.showerror("error", "please enter a username")
        return  #returns to the if statement above
    else:
        new_email = settings_email_entry.get()

    if not settings_username_entry.get():
        messagebox.showerror("error", "please enter the password")
        return
    else:
        if settings_username_entry.get() == user_username:
            messagebox.showerror("error", "this is your current username")
            return
        else:
            new_username = settings_username_entry.get()

    if not settings_password_entry.get():
        messagebox.showerror("error", "please enter the password")
        return
    else:
        if len(settings_password_entry.get()) >= 7:
            new_password = settings_password_entry.get()
        else:
            messagebox.showerror("error", "please enter a password at least 7 characters long")
            return

    if not settings_con_password_entry.get():
        messagebox.showerror("error", "please confirm your password")
        return
    else:
        new_conpassword = settings_con_password_entry.get()
        if new_conpassword == new_password:
            pass
        else:
            messagebox.showerror("error", "The passwords do not match")
            return
        pass 

    if new_username in User_list:
        messagebox.showerror("error", "This username has already been taken")
        return
    else:
        confirm = askyesno(title, "Do you confirm saving changes?")
        if confirm is True:
            new_status_config = ["borrowed", "returned", "lost"]
            os.rename(f"library/Version 3/{user_username}.json", f"library/Version 3/{new_username}.json")
            del User_list[user_username]
            with open(f"library/Version 3/Users.json", "w") as fp:
                fp.seek(0)  # rewind
                json.dump(User_list, fp)  #dumps the list into the external file
                fp.truncate()   #updates the file
            new_user = User(new_username, new_password, new_email, new_status_config)
            new_user.new_user()
            user_username = new_username
            reload_data_table()
            switch_center_Frame()
            settings_username_entry.delete(0, END)
            settings_password_entry.delete(0, END)
            settings_con_password_entry.delete(0, END)
            settings_email_entry.delete(0,END)
        else:
            return

def get_data():
    global add_resource, add_description, add_date, add_status, add_day_date, add_month_date, add_year_date
    description_entry = description_txt.get("1.0",'end-1c')
    #the if statement is used to check if the user has enetered anything
    if not resource_entry.get():
        messagebox.showerror("error", "please enter the resource name")
        return  #returns to the if statement above
    else:
        add_resource = resource_entry.get()

    if not description_entry:
        messagebox.showerror("error", "please enter the description of the resource")
        return
    else:
        add_description = description_entry

    if not date_day_entry.get():
        messagebox.showerror("error", "please enter todays day")
        return
    else:
        add_day_date = date_day_entry.get()

    if not date_month_entry.get():
        messagebox.showerror("error", "please enter todays month")
        return
    else:
        add_month_date = date_month_entry.get()
        
    if not date_year_entry.get():
        messagebox.showerror("error", "please enter todays year")
        return
    else:
        add_year_date = date_year_entry.get()

    if not status_select.get():
        messagebox.showerror("error", "please enter the current status of the resource")
        return
    else:
        add_status = status_select.get()

    #formats the add_date variable with the corresponding dates entered
    add_date = (f"{add_day_date}/{add_month_date}/{add_year_date}")

#the function used to append the used inputs in the entries into the viewtree widget
def append_add():
    try:
        int(date_year_entry.get())
    except ValueError:
        messagebox.showerror("error", "please enter a valid year")
        return
    
    if int(date_year_entry.get()) in range(1940, 2024):
        get_data()
    else:
        messagebox.showerror("error", "please enter a year between 1940 and 2024")
        return
    
    #appends the gathered variables to the external file
    lst.append([add_resource, add_description, add_date, add_status])

    #opens up the json file to write and read
    with open(f"library/Version 3/{user_username}.json", "r+") as fp:
        json.dump(lst, fp)      #uses the dump function to add the new data
    
    reload_data_table()     #reloads the viewtree widget datatable with the added information
    switch_center_Frame()

def edit_row():
    try:
        int(date_year_entry.get())
    except ValueError:
        messagebox.showerror("error", "please enter a valid year")
        return
    
    if int(date_year_entry.get()) in range(1940, 2024):
        get_data()
    else:
        messagebox.showerror("error", "please enter a year between 1940 and 2024")
        return
    confirm = askyesno(title, "Do you confirm saving changes?")
    if confirm is True:
        chosen_row = data_table.item(selected_item)["values"]      #retrieves the values from the selected row
        #checks through all the rows in the list and finds the number associate with the selected row
        
        for i in range(len(lst)):
            if lst[i] == chosen_row:
                lst[i] = [add_resource, add_description, add_date, add_status]     #replaces variable from the list
                break
            else:
                pass
            data_table.item(edit_item, values=(add_resource, add_description, add_date, add_status))

        #opens the json file to write as fp
        with open(f"library/Version 3/{user_username}.json", "w") as fp:
            fp.seek(0)  # rewind
            json.dump(lst, fp)  #dumps the list into the external file
            fp.truncate()   #updates the file
        add_resource_lbl.config(text="Add")
        switch_center_Frame()
    else:
        return

    

def delete_row():
    confirm = askyesno(title, "Do you confirm saving changes?")
    if confirm is True:
        try:
            #turns the selected row in the viewtree and retrieves the values
            selected_item = data_table.focus()      #the current selected row
            choosen_row = data_table.item(selected_item)["values"]      #retrieves the values from the selected row
            
            #checks through all the rows in the list and finds the number associate with the selected row
            for i in range(len(lst)):
                if lst[i] == choosen_row:
                    lst.pop(i)      #removes variable from the list
                    break
                else:
                    pass
            
            #opens the json file to write as fp
            with open(f"library/Version 3/{user_username}.json", "w") as fp:
                fp.seek(0)  # rewind
                json.dump(lst, fp)  #dumps the list into the external file
                fp.truncate()   #updates the file
            
            #deletes the selected row in the GUI for the user
            selected_row = data_table.selection()[0] 
            data_table.delete(selected_row)
        except IndexError:
            messagebox.showerror("error", "please add or select a row")
    else:
        return

def view_description():
    try:
        selected_item = data_table.focus()
        add_resource_lbl.config(text="Edit")
        chosen_row = data_table.item(selected_item)["values"]
        messagebox.showinfo("showinfo",f'description: {chosen_row[1]}')
    except IndexError:
        messagebox.showerror("error", "please add or select a row")

#hides password
def show_hide_password1():
    if password_entry['show'] == '*':
        password_entry['show'] = ''
    else:
        password_entry['show'] = '*'

#hides password
def show_hide_password2():
    if add_password_entry['show'] == '*':
        add_password_entry['show'] = ''
    else:
        add_password_entry['show'] = '*'

    if conpassword_entry['show'] == '*':
        conpassword_entry['show'] = ''
    else:
        conpassword_entry['show'] = '*'
        


#creating the main frames
login_frame = Frame(root, width=800, height=400, pady=20)
add_user_frame = Frame(root, width=800, height=400, pady=20)
top_frame = Frame(root, width=800, height=100, pady=3)
access_frame = Frame(root, width=800, height=130)
resource_frame = Frame(root, width=800, height=225)
settings_frame = Frame(root, width=800, height=275, pady=20)
resource_btm_frame = Frame(root, width=800, height=50, pady=10)
add_resource_frame = Frame(root, width=800, height=50, pady=20)
add_resource_bottom_frame = Frame(root, width=800, height=50, pady=10)
edit_resource_frame = Frame(root, width=800, height=50, pady=10)

#formatting the containers/frames into grids
root.grid_rowconfigure((0,1,2,3,4), weight=1)
root.grid_columnconfigure((0), weight=1)

login_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
login_frame.grid_columnconfigure((0,1), weight=1)

add_user_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
add_user_frame.grid_columnconfigure((0,1), weight=1)

top_frame.grid_rowconfigure((0), weight=1)
top_frame.grid_columnconfigure((0,1,2), weight=1)

access_frame.grid_rowconfigure(0, weight=1)
access_frame.grid_columnconfigure((0,1,2), weight=1)

resource_frame.grid_rowconfigure(0, weight=1)
resource_frame.grid_columnconfigure((0,1), weight=1)

settings_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)
settings_frame.grid_columnconfigure((0,1), weight=1)

resource_btm_frame.grid_rowconfigure(0, weight=1)
resource_btm_frame.grid_columnconfigure((0,1,2,3), weight=1)

add_resource_frame.grid_rowconfigure((0,1,2,3,4,6,7,8), weight=1)
add_resource_frame.grid_columnconfigure((0), weight=5)
add_resource_frame.grid_columnconfigure((1), weight=1)
add_resource_frame.grid_columnconfigure((2), weight=5)

add_resource_bottom_frame.grid_rowconfigure(1, weight=1)
add_resource_bottom_frame.grid_columnconfigure((0,1), weight=1)

edit_resource_frame.grid_rowconfigure(0, weight=1)
edit_resource_frame.grid_columnconfigure((0,1), weight=1)

top_frame.grid(row=0, sticky="nsew")
login_frame.grid(row=1, sticky="nsew", rowspan=4)
add_user_frame.grid(row=1, sticky="nsew", rowspan=4)
access_frame.grid(row=1, sticky="nsew")
resource_frame.grid(row=2, sticky="nsew", rowspan=2)
settings_frame.grid(row=2, sticky="nsew", rowspan=3)
resource_btm_frame.grid(row=4, sticky="nsew")
add_resource_frame.grid(row=2, sticky="nsew", rowspan=2)
add_resource_bottom_frame.grid(row=4, sticky="nsew")
edit_resource_frame.grid(row=4, sticky="nsew")

#creating widgets for the login frame
#Labels
login_lbl = Label(login_frame, text="Login:", font=("verdana 12 bold"))
username_lbl = Label(login_frame, text="Username:")
password_lbl = Label(login_frame, text="password:")

#entries
username_entry = Entry(login_frame)
password_entry = Entry(login_frame, show="*")

#buttons
signin_button = Button(login_frame, text="login", command=signin, width=10)
new_user_button = Button(login_frame, text="create new account" ,command=lambda: add_user_frame.tkraise())
hide_password = Checkbutton(login_frame, text="show password", command= show_hide_password1)

#formatting the widgets for the login frame
#Labels
login_lbl.grid(row=0, column=0, sticky="s", columnspan=2)
username_lbl.grid(row=1,column=0,sticky="se")
password_lbl.grid(row=2,column=0,sticky="e")

#entries
username_entry.grid(row=1,column=1,sticky="sw")
password_entry.grid(row=2,column=1,sticky="w")

#buttons
signin_button.grid(row=4,column=0, columnspan=2, sticky="n")
new_user_button.grid(row=5, column=0, columnspan=2)
hide_password.grid(row=2, column=0, sticky="s", columnspan=2)

#creating widgets for add user frame
#labels
add_user_lbl = Label(add_user_frame, text="Create new account", font=("verdana 12 bold"))
add_username_lbl = Label(add_user_frame, text="Username:")
add_password_lbl = Label(add_user_frame, text="password:")
conpassword_lbl = Label(add_user_frame, text="confirm password:")
add_email_lbl = Label(add_user_frame, text="email:")


#entries
add_username_entry = Entry(add_user_frame)
add_password_entry = Entry(add_user_frame, show="*")
conpassword_entry = Entry(add_user_frame, show="*")
add_email_entry = Entry(add_user_frame)

#buttons
create_user_button = Button(add_user_frame, text="create user", command=create_user)
return_btn = Button(add_user_frame, text="go back", command=lambda: login_frame.tkraise())
add_hide_password = Checkbutton(add_user_frame, text="show password", command= show_hide_password2)

#formating widgets for add user frame
#labels
add_user_lbl.grid(row=0, column=0, columnspan=2)
add_username_lbl.grid(row=2,column=0, sticky="e")
add_password_lbl.grid(row=3,column=0, sticky="e")
conpassword_lbl.grid(row=4, column=0, sticky="e")
add_email_lbl.grid(row=1, column=0, sticky="e")

#entries
add_username_entry.grid(row=2,column=1, sticky="w")
add_password_entry.grid(row=3,column=1, sticky="w")
conpassword_entry.grid(row=4,column=1, sticky="w")
add_email_entry.grid(row=1,column=1, sticky="w")

#buttons
create_user_button.grid(row=7, column=0, columnspan=2)
return_btn.grid(row=8, column=0, columnspan=2)
add_hide_password.grid(row=5, column=0, columnspan=2, sticky="n")

#creating widgets for the top frame
title = Label(top_frame, text="Resource Manager", font = ("arial",18))

#inserting image
logo_img = PhotoImage(file="library/logo.png")
logo = Label(top_frame, image = logo_img, font = ("arial",10))

credit = Label(top_frame, text ="by Leo Jeon", font = ("arial",10))


#formatting the widgets for the top frame
title.grid(row=0, column=1, sticky="ns")
logo.grid(row=0, column=0, sticky="ns")
credit.grid(row=0, column=2, sticky="ns")

#creaing widgets for access frame
home_button = Button(access_frame, text = "Home", font = ("arial",14), borderwidth=0, command=switch_center_Frame)
settings_button = Button(access_frame, text = "settings", font = ("arial",14), borderwidth=0, command=lambda: settings_frame.tkraise())
sign_out_button = Button(access_frame, text = "sign out", font = ("arial",14), borderwidth=0, command=lambda: login_frame.tkraise())

#formatting the widgets for the access frame
home_button.grid(row=0, column=0, padx = 20)
settings_button.grid(row=0, column=1, padx = 20)
sign_out_button.grid(row=0, column=2, padx = 20)

#creaing widgets for center frame
#setting up the widget tree and assigning headings
def reload_data_table():        #reason for in a function is to reload added data
    global data_table
    global status_select
    data_table_headings = ("Resource","Description","Date loaned","status")
    data_table = ttk.Treeview(resource_frame, columns=data_table_headings, show="headings")
    data_table_scroll = ttk.Scrollbar(resource_frame, orient=VERTICAL, command=data_table.yview)

    #creating headings for the data_table
    data_table.heading("Resource", text="Resource") 
    data_table.heading("Description", text="Description")
    data_table.heading("Date loaned", text="Date loaned")
    data_table.heading("status", text="status")

    #inserting the values into the viewtree
    for resource in lst:
        data_table .insert("", END, values=resource)

    #formatting the widgets for the center frame
    data_table.configure(yscroll=data_table_scroll.set)
    data_table_scroll.grid(row=0, column=1, sticky="nesw")
    data_table.grid(row=0, column=0, sticky="nes", padx=(20,0))

#creaing widgets for bottom frame
add_resource = Button(resource_btm_frame, text = "add data", command=switch_add_frame)
delete_resource = Button(resource_btm_frame, text = "delete data", command=delete_row)
edit_resource = Button(resource_btm_frame, text = "edit data", command=switch_edit_frame)
view_resource = Button(resource_btm_frame, text = "view data", command=view_description)

#formatting the widgets for the bottom frame
add_resource.grid(row=0, column=1)
delete_resource.grid(row=0, column=2)
edit_resource.grid(row=0, column=0)
view_resource.grid(row=0, column=3)

#creating widgets for add frame
#labels
add_resource_lbl = Label(add_resource_frame, text="Add resource",  font="verdana 12 bold")
resource_entry_lbl = Label(add_resource_frame, text="resource name:")
description_entry_lbl = Label(add_resource_frame, text="description of resource:")
date_entry_lbl = Label(add_resource_frame, text="date: (dd/mm/yyyy)")
status_select_lbl = Label(add_resource_frame, text="status:")

#entries
resource_entry = Entry(add_resource_frame)
description_txt = Text(add_resource_frame, width = 30, height = 4, font=("arial", 10))
date_year_entry = Entry(add_resource_frame, width = 9)

#combobox
day_options = [str(i).rjust(2, "0") for i in range(1, 32)]
month_options = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

date_day_entry = Combobox(add_resource_frame, state="readonly", values = day_options, textvariable= StringVar(), width="4")
date_month_entry = Combobox(add_resource_frame, state="readonly", values = month_options, textvariable= StringVar(), width="4")
status_select = Combobox(add_resource_frame, state="readonly", values = status_options, textvariable= StringVar())


#formatting the widgets for the add frame
#labels
add_resource_lbl.grid(row=0, column=0, pady=(10,0), sticky="ns", columnspan=3)
resource_entry_lbl.grid(row=1, column=0, pady=(10,0), columnspan=3)
description_entry_lbl.grid(row=3, column=0, columnspan=3)
date_entry_lbl.grid(row=5, column=0, columnspan=3)
status_select_lbl.grid(row=7, column=0, columnspan=3)
status_select.grid(row=8, column=0, columnspan=3)

#entries
resource_entry.grid(row=2, column=0, columnspan=3)
description_txt.grid(row=4, column=0, columnspan=3)
date_day_entry.grid(row=6, column=0, sticky="e")
date_month_entry.grid(row=6, column=1)
date_year_entry.grid(row=6, column=2, sticky="w")

#creating widgets for add bottom frame
#button
return_main_btn = Button(add_resource_bottom_frame, text = "Go back", command=switch_center_Frame)
add_btn = Button(add_resource_bottom_frame, text = "Add to library", command=append_add)

#formatting the widgets for the add bottom frame
#button
return_main_btn.grid(row=0, column=0, sticky="e", padx = 30)
add_btn.grid(row=0, column=1, sticky="w", padx = 30)

#creating widgets for add bottom frame
#button
return_main_btn = Button(edit_resource_frame, text = "Go back", command=switch_center_Frame)
edit_btn = Button(edit_resource_frame, text = "save changes", command=edit_row)

#formatting the widgets for the add bottom frame
#button
return_main_btn.grid(row=0, column=0, sticky="e", padx = 30)
edit_btn.grid(row=0, column=1, sticky="w", padx = 30)

#setting up widgets for settings frame
#labels
settings_title_lbl = Label(settings_frame, text="Settings")
settings_description_lbl = Label(settings_frame, text="Update the settings to your account")
settings_email_lbl = Label(settings_frame, text="Email: ")
settings_username_lbl = Label(settings_frame, text="Username: ")
settings_password_lbl = Label(settings_frame, text="Password: ")
settings_con_password_lbl = Label(settings_frame, text="Confirm password: ")

#entries
settings_email_entry = Entry(settings_frame)
settings_username_entry = Entry(settings_frame)
settings_password_entry = Entry(settings_frame)
settings_con_password_entry = Entry(settings_frame)

#Button
settings_exe_btn = Button(settings_frame, text="Update", command=update_user)

#formating widgets for settings frame
#labels
settings_title_lbl.grid(row=0, column=0, columnspan=2, sticky="ns")
settings_description_lbl.grid(row=1, column=0, columnspan=2)
settings_email_lbl.grid(row=2, column=0, sticky="e")
settings_username_lbl.grid(row=3, column=0, sticky="e")
settings_password_lbl.grid(row=4, column=0, sticky="e")
settings_con_password_lbl.grid(row=5, column=0, sticky="e")

#entries
settings_email_entry.grid(row=2, column=1, sticky="w")
settings_username_entry.grid(row=3, column=1, sticky="w")
settings_password_entry.grid(row=4, column=1, sticky="w")
settings_con_password_entry.grid(row=5, column=1, sticky="w")

#Button
settings_exe_btn.grid(row=7, column=0, columnspan=2)

#calling functions
login_frame.tkraise()
root.mainloop()