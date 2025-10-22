from traceback import clear_frames
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import customtkinter as ct
import re
import matplotlib.pyplot as plt
from numpy import pad
import pandas as pd
import sqlite3 as sql
import tkinter as tk
from tkinter import Label
from datetime import datetime as dt
from streamlit import image
realusername = None
""" # Function to update the time
def update_time():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)  # Update the time every second

# Create the main window
root = tk.Tk()
root.title("Live Clock")

# Create a label to display the time
clock_label = Label(root, font=("Helvetica", 48), bg="black", fg="white")
clock_label.pack(pady=20)

# Call the update_time function to initialize the clock
update_time()

# Run the Tkinter event loop
root.mainloop() """

conn = sql.connect('task.db')
cursor = conn.cursor()
count = []

def popup(master,message,textcolor,duration=4000):
    """
    Create a popup window to display a message.
    duration default is 4 seconds
    """
    pop = ctk.CTkToplevel(master)
    pop.title("MESSAGE")
    pop.geometry("250x100+400+300")
    pop.resizable(False,False)
    pop.configure(bg="#285a3d")
    pop.overrideredirect(True)
    poplabel = ctk.CTkLabel(pop,
                        text=message,
                        font=("Arial",12,"bold"),
                        fg_color="#008cff",
                        bg_color="#75a1ce",
                        padx=20,
                        pady=20,
                        text_color=textcolor
                        )
    poplabel.pack()
    pop.lift()
    pop.after(duration,pop.destroy)
def isdigit(number):
    try:
        num = int(number)
        return num
    except Exception :
        return "invalid"
def login_to_database(username,password):
            global realerusername
            username = username.lower()
            try:
                    cursor.execute("select * from users where username=:h",{"h": f"{username}"})
                    data = cursor.fetchone()
                    if data[1] == password:
                        realusername:str = data[0]
                        realerusername = realusername
                        return data[0]
                    else :
                        return "invalid login credentials"
            except Exception as e:
                return "user does not exist"
def switch_to_login():
        root2.destroy()
        loginpage()
def logoutfunction():
    decidetologout=  messagebox.askyesno("LOG OUT","DO YOU WANT TO LOG OUT",icon="question")
    if decidetologout:
        home.destroy()
        loginpage()

def collectinfo(text,titile):
    popmenu = ctk.CTkInputDialog(
                                title=titile,
                                text=text)
    answer = popmenu.get_input()
    try:
        if answer.strip():
            anslist = []
            anslist.append(answer.strip())
            return anslist
    except Exception as e:
        popmenu.destroy()
def getrealtime():
    CURRENTDATE = dt.now()
    year = CURRENTDATE.year()
    week = CURRENTDATE.weekday()
    month = CURRENTDATE.month()
    day = CURRENTDATE.day()
    hour = CURRENTDATE.hour()
    minute = CURRENTDATE.minute()
    second = CURRENTDATE.second()
    return list(year,month,week,day,hour,minute,second)
def collectinfoasstring(text,titile):

    popmenu = ctk.CTk(
                                title=titile,
                                text=text)
    answer = popmenu.get_input()
    if answer.strip():
        return answer.strip()
def add_to_task(tasks:list,name:str,isdone:list):
    index = 0
    for i in tasks:
        cursor.execute(f"insert into task (name,tasks,isdone) values (?,?,?)",(name,i,isdone[index]))
        index+=1
    return "done"
def viewtasks(name:str):
    allii = cursor.execute(f"select * from task where name=:n",{"n":f"{name}"})
    alili = allii.fetchall()
    print(alili)
    lali = len(alili)
    lalist = []
    if lali != 0:
        for i in alili:
            print(i)
            la = list((i[1],i[2]))
            print(la)
            lalist.append(la)
            print(lalist)
    return lalist
def updatepassword(old:str,new:str,name:str,tkmaster):
    conn = sql.connect('task.db')
    cursor = conn.cursor()
    try:
        title = "PASSWORD CHANGE"
        if new.strip() and old.strip():
            if len(new.strip()) <6 or len(new.strip())>24:
                messagebox.showerror(title,"MAKE SURE PASSWORD IS BETWEEN 6 AND 24 CHARACTERS!!!")
                tkmaster.lift()
            elif len(re.findall(r'\s+',new.strip())) >0:
                messagebox.showerror(title,"PASSWORD CANNOT HAVE SPACES IN BETWEEN")
                tkmaster.lift()
            elif not ((len(re.findall(r'\d+',new.strip())) !=0 or len(re.findall(r'[^a-zA-Z0-9]',new.strip()))!=0) and len(re.findall(r'\w+',new.strip()))!=0):
                messagebox.showerror(title,"PASSWORD MUST CONTAIN AT LEAST A SPECIAL CHARACTER, OR A NUMBER AND LETTERS",icon="warning")
                tkmaster.lift()
            else:
                cursor.execute("select * from users where username=:h",{"h": f"{name}"})
                data = cursor.fetchone()
                if data[1] == old:
                    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new, name))
                    conn.commit()
                    time.sleep(2)
                    tkmaster.destroy()
                    messagebox.showinfo("PASSWORD CHANGE","Successfully updated password")
                else:
                    messagebox.showerror("PASSWORD CHANGE","Incorrect password")
                    tkmaster.lift()
        else:
            messagebox.showerror(title,"PLEASE FILL ALL SPACES")
            tkmaster.lift()
        
    except Exception as identifier:
        messagebox.showwarning("PASSWORD CHANGE",f"An error occured  {identifier}")
        tkmaster.destroy()
def addinfototask():
    return None
def popcollectchangedpassword(master,title:str):
    """
    Create a popup window for changing the user's password.
    """
    popit = ct.CTkToplevel(master)
    popit.title(title)
    popit.overrideredirect(True)
    labe1 = ct.CTkLabel(popit,
                        text_color="white",
                        text="Your former password")
    labe1.pack(pady=5)
    oldpassword = ct.CTkEntry(popit,placeholder_text="Your former password",
                            text_color="#0f232b",
                            placeholder_text_color="#358daf",
                            fg_color="wheat",
                            border_color="#358daf")
    oldpassword.pack(pady=1)
    labe2 = ct.CTkLabel(popit,
                        text_color="white",
                        text="Your new password")
    labe2.pack(pady=5)
    newpassword = ct.CTkEntry(popit,placeholder_text="Your new password",
                            text_color="#0f232b",
                            placeholder_text_color="#358daf",
                            border_color="#358daf",
                            fg_color="wheat")
    newpassword.pack(pady=1)
    deleteframe = ctk.CTkFrame(popit, fg_color="gray", bg_color="white")
    deleteframe.pack(pady=5)
    changebtn = ct.CTkButton(deleteframe,
                            text="CHANGE",
                            fg_color="#1cb91c",
                            hover_color="#7bff7b",
                            command=lambda: updatepassword(oldpassword.get(),newpassword.get(),realerusername,popit),
                            corner_radius=0)
    changebtn.grid(row=1,column=0)
    cancelbtn = ct.CTkButton(deleteframe, text="Cancel",
                            command=lambda: popit.destroy(),
                            corner_radius=0)
    cancelbtn.grid(row=1,column=1)


#################################  MAIN HOMEPAGE  #####################################
def mainhomepage():
    # Appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    global home
    # Main Home Window
    home = ctk.CTk()
    home.title("Task Manager - Home")
    home.iconbitmap("m.jpeg")
    home.geometry("950x600")

    # Load background image
    bg_image = Image.open("m.jpeg") 
    newbgimage = Image.open("The Galaxy!.jpeg")
    newbgimage = newbgimage.resize((950, 600))
    bg_photo = ImageTk.PhotoImage(newbgimage)
    pf_image = bg_image.resize((100, 100))
    pf_image = ImageTk.PhotoImage(pf_image)

    # Background Label
    bg_label = ctk.CTkLabel(home, image=bg_photo, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Sidebar 
    sidebar = ctk.CTkFrame(home, width=200, corner_radius=0, fg_color="black", bg_color="transparent")
    sidebar.pack(side="left", fill="y")

    title = ctk.CTkLabel(sidebar, text="📌 TaskMaster", font=("Arial", 22, "bold"))
    title.pack(pady=20)

    btn_dashboard = ctk.CTkButton(sidebar, text="🏠 Dashboard", width=180,command=lambda:main_frame.tkraise())
    btn_dashboard.pack(pady=10)
    btn_add = ctk.CTkButton(sidebar, text="➕ Add Task", width=180)
    btn_add.pack(pady=10)
    btn_settings = ctk.CTkButton(sidebar, text="⚙️ Settings", width=180,command=lambda:settingsframe.tkraise())
    btn_settings.pack(pady=10)

    logout = ctk.CTkButton(
        sidebar, text="🚪 Logout", fg_color="red", hover_color="#b91c1c", width=180,
        command=logoutfunction)
    logout.pack(side="bottom", pady=20)

    realframe = ctk.CTkFrame(home, corner_radius=15, fg_color="black", bg_color="transparent")
    realframe.pack(side="right", expand=True, fill="both", padx=20, pady=20)
    # Main Content Area (transparent so background shows)
    main_frame = ctk.CTkFrame(realframe, corner_radius=15, fg_color="black", bg_color="transparent")
    main_frame.place(relwidth=1, relheight=1)


    #Use the time play fess
    #new frame for play (take am play fess)
    time_frame = ctk.CTkFrame(main_frame, corner_radius=15,height=50,width=200, fg_color="black", bg_color="blue")
    time_frame.pack(pady=5)
    def update_time():
        current_time = time.strftime("%I:%M:%S:%p")
        timelabel.configure(text=f"welcome {realerusername.upper()}:  {current_time}")
        timelabel.after(1000, update_time)
    timelabel = ctk.CTkLabel(time_frame, font=("Arial", 24, "bold"),text_color="gold")
    timelabel.pack(pady=1)
    update_time()

    profilepi = ctk.CTkLabel(main_frame,
                                text=" ",
                                bg_color="transparent",
                                height=100,
                                width=100,
                                fg_color="grey",
                                text_color="black",
                                font=("Arial", 30),
                                image=pf_image
                                )
    profilepi.pack(pady=5)

    header = ctk.CTkLabel(main_frame, text="✅ Your Tasks", font=("Arial", 24, "bold"))
    header.pack(pady=10)

    # Scrollable Task List
    task_frame = ctk.CTkScrollableFrame(main_frame, label_text="Tasks", fg_color="transparent")
    task_frame.pack(fill="both", expand=True, padx=10, pady=10)
    checkbox_vars = {}
    checkbox_widgets = {}
    # Example tasks (later connect to SQLite omorrr e choke)
    def addtoframe(task:str,ticked:bool=False):
        var = ctk.BooleanVar(value=ticked)
        task_item = ctk.CTkCheckBox(task_frame, text=task, font=("Arial", 16),variable=var,command=updatelistindatabase)
        task_item.pack(anchor="w", pady=5, padx=10)
        checkbox_vars[task] = var
        checkbox_widgets[task] = task_item
    def deletetask(tasktobedeltedlist):
        for task in tasktobedeltedlist:
            checkbox_widgets[task].destroy()
            del checkbox_vars[task]
            del checkbox_widgets[task]
            cursor.execute("DELETE FROM task WHERE tasks =:h",{"h":task})
            conn.commit()
    def popupdelete(master):
        task_to_be_deleted = []
        tasklisttodelete:list = viewtasks(realerusername.lower())
        for t in tasklisttodelete:
            task_to_be_deleted.append(t[0])
        def delete(tasklist:list,checkbox_vars,checkbox_widgets):
                tasks_to_delete = [task for task, var in checkbox_vars.items() if var.get()]
                for task in tasks_to_delete:
                        checkbox_widgets[task].destroy()
                        del checkbox_vars[task]
                        del checkbox_widgets[task]
                        tasklist.remove(task)
                deletetask(tasks_to_delete)
        popmenu = ct.CTkToplevel(master)
        popmenu.title("Testing...")
        popmenu.overrideredirect(True)
        task_frame = ct.CTkScrollableFrame(popmenu, label_text="Tasks", fg_color="transparent")
        task_frame.pack(fill="both", expand=True, padx=10, pady=10)
        checkbox_vars = {}
        checkbox_widgets = {}
        
        for task in task_to_be_deleted:
                var = ct.BooleanVar(value=False)
                task_item = ct.CTkCheckBox(task_frame, text=task, font=("Arial", 16),variable=var)
                task_item.pack(anchor="w", pady=5, padx=10)
                checkbox_vars[task] = var
                checkbox_widgets[task] = task_item
        deleteframe = ctk.CTkFrame(popmenu, corner_radius=15,height=50,width=200, fg_color="gray", bg_color="white")
        deleteframe.pack(pady=5)
        delete_task_btn = ct.CTkButton(deleteframe, text="➖ Delete",
                                        width=200,corner_radius=0,
                                        height=40,
                                        command=lambda: delete(task_to_be_deleted,checkbox_vars,checkbox_widgets),
                                        fg_color="red",
                                        hover_color="#b91c1c"
                                        )
        delete_task_btn.grid(row=1,column=0)
        cancelbtn = ct.CTkButton(deleteframe, text="Cancel",
                                        width=200,corner_radius=0,
                                        height=40,
                                        command=lambda: popmenu.destroy(),
        )
        cancelbtn.grid(row=1,column=1)
        tasks_to_delete_list = [task for task, var in checkbox_vars.items() if var.get()]
        return tasks_to_delete_list
    
    def updatelistindatabase():
        for task, var in checkbox_vars.items():
            isdone = "True" if var.get() else "False"
            cursor.execute("UPDATE task SET isdone = ? WHERE tasks = ?", (isdone, task))
        conn.commit()
    # Function to add task to both frame and database
    def addtotheframeanddatabase(task:list,isdone:list):
        if add_to_task(task,name=realerusername.lower(),isdone=isdone) =="done":
            addtoframe(task[0])
        
    
    #add task to my scrollable frame
    tasks = viewtasks(realerusername.lower())
    for task in tasks:
        addtoframe(task[0],task[1])
    #add frame
    addframe = ctk.CTkFrame(main_frame, corner_radius=15,height=50,width=200, fg_color="gray", bg_color="white")
    addframe.pack(pady=5)
    # Add Task Button
    add_task_btn = ctk.CTkButton(addframe, text="➕ Add New Task",
                                    width=200,corner_radius=0,
                                    height=40,
                                    command=lambda: addtotheframeanddatabase(collectinfo("Enter your task","New Task"),["False"]),
                                    )
    add_task_btn.grid(row=1, column=0)
    # Delete Task Button
    delete_task_btn = ctk.CTkButton(addframe, text="➖ Delete Task", 
                                    width=200,corner_radius=0,
                                    height=40,
                                    command=lambda:popupdelete(task_frame),
                                    fg_color="red",
                                    hover_color="#b91c1c")
    delete_task_btn.grid(row=1, column=1)

    # Footer
    footer = ctk.CTkLabel(main_frame, text="© 2025 BoiBoi", font=("Arial", 12), text_color="gray")
    footer.pack(side="bottom", pady=5)

    #################### settings page #######################
    #settings frame
    settingsframe = ctk.CTkFrame(realframe, corner_radius=15, fg_color="black", bg_color="transparent")
    settingsframe.place(relwidth=1, relheight=1)

    set1 = ctk.CTkButton(settingsframe,
                        text="🏠 Change password",
                        width=800,
                        fg_color="grey",
                        height=30,
                        corner_radius=0)
    set1.pack(pady=1)
    set2 = ctk.CTkButton(settingsframe,
                        text=" Change theme",
                        width=800,
                        fg_color="grey",
                        height=30,
                        corner_radius=0)
    set2.pack(pady=10)
    def deleteaccount():
        """Delete user account and all associated data."""
        ASK = messagebox.askyesnocancel("DELETE ACCOUNT?","DO YOU REALLY WANT TO DELETE YOUR ACCOUNT (ALL INFORMATION WOULD BE LOST).")
        if ASK:
            try:
                cursor.execute("DELETE FROM users WHERE username =:h",{"h":realerusername.lower()})
                cursor.execute("DELETE FROM task WHERE name =:h",{"h":realerusername.lower()})
                conn.commit()
                messagebox.showinfo("DELETE ACCOUNT","Successfully deleted account")
                home.destroy()
                loginpage()
            except Exception as e:
                messagebox.showwarning("DELETE ACCOUNT",f"An error occured  {e}")
    set3 = ctk.CTkButton(settingsframe,
                        text="delete account",
                        width=800,
                        fg_color="grey",
                        height=30,
                        corner_radius=0,
                        command=deleteaccount)
    set3.pack(pady=1)
    def updateusername():
        """Update the user's username."""
        newname =collectinfo("ENTER YOUR NEW NAME YOU WANT TO USE","CHANGE NAME?")
        if newname:
            try:
                cursor.execute("UPDATE users SET username = ? WHERE username = ?", (newname[0].strip().lower(), realerusername.lower()))
                conn.commit()
                messagebox.showinfo("CHANGE NAME","Successfully changed name")
            except Exception as e:
                messagebox.showwarning("CHANGE NAME",f"An error occured  {e}")
    set4 = ctk.CTkButton(settingsframe,
                        text=" Change UserName",
                        width=800,
                        fg_color="grey",
                        height=30,
                        corner_radius=0,
                        command=updateusername)
    set4.pack(pady=10)
    set5 = ctk.CTkButton(settingsframe,
                        text="⚡ Change Password",
                        width=800,
                        fg_color="grey",
                        corner_radius=0,
                        height=30,
                        command=lambda: popcollectchangedpassword(settingsframe,"CHANGE PASSWORD"))
    set5.pack(pady=1)
    def raisethemetoblack():
        ctk.set_appearance_mode("Dark")
        settolight.tkraise()
    def raisethemetolight():
        ctk.set_appearance_mode("light")
        settodark.tkraise()
    changethemeframe = ctk.CTkFrame(settingsframe,height=30,width=800, fg_color="gray", bg_color="white")
    changethemeframe.pack(pady=10)
    settodark = ctk.CTkButton(changethemeframe,
                        text=" Change theme to dark",
                        width=800,
                        fg_color="grey",
                        corner_radius=0,
                        command=raisethemetoblack)
    settodark.place(relwidth=1,relheight=1)
    settolight = ctk.CTkButton(changethemeframe,
                        text=" Change theme to light",
                        width=800,
                        fg_color="grey",
                        corner_radius=0,
                        command=raisethemetolight)
    settolight.place(relwidth=1,relheight=1)
    main_frame.tkraise()
    home.mainloop()



#################################  REGISTRATION PAGE  #####################################


    
#registration page
def register():
        """
        Open the registration page.
        """
        #Function to add user's name to database
        def add_to_database(username,password,age):
            username = username.strip().lower()
            password = password.strip()
            age = int(age)
            allis =cursor.execute("select * from users where username=:u",{"u":f"{username}"})
            lallis = len(allis.fetchall())
            if lallis ==0:
                cursor.execute("INSERT INTO users (username,password,age) VALUES (?,?,?)",(username,password,age))
                conn.commit()
                return "Successful"
            else:
                    return "User already exist"
        def registerfunction():
            if regisname.get().strip() and regispassword.get().strip() and regisage.get().strip():
                if len(regispassword.get()) <6 or len(regispassword.get())>24:
                    messagebox.showerror("REGISTRATION ERROR","MAKE SURE PASSWORD IS BETWEEN 6 AND 24 CHARACTERS!!!")
                elif len(re.findall(r'\s+',regispassword.get().strip())) >0:
                    messagebox.showerror("REGISTRATION ERROR","PASSWORD CANNOT HAVE SPACES IN BETWEEN")
                elif not ((len(re.findall(r'\d+',regispassword.get().strip())) !=0 or len(re.findall(r'[^a-zA-Z0-9]',regispassword.get().strip()))!=0) and len(re.findall(r'\w+',regispassword.get().strip()))!=0):
                    messagebox.showerror("REGISTRATON ERROR","PASSWORD MUST CONTAIN AT LEAST A SPECIAL CHARACTER, OR A NUMBER AND LETTERS",icon="warning")
                elif len(re.findall(r'[^a-zA-Z0-9_@\s]',regisname.get().strip())) >0:
                    messagebox.showerror("REGISTRATION ERROR","PLEASE USE A VALID USERNAME")
                elif isdigit(regisage.get().strip()) == "invalid":
                    messagebox.showerror("REGISTRAION ERROR","PLEASE AGE CAN ONLY BE NUMBERS")
                elif add_to_database(regisname.get(),regispassword.get(),regisage.get()) == "Successful":
                    messagebox.showinfo("REGISTRATION SUCCESS",'''Successfully Registered
                                                        You can now LOGIN''')
                    root2.destroy()
                    loginpage()
                else:
                    messagebox.showerror("REGISTRATION ERROR","SORRY USER ALREADY EXIST",icon="error")
            else:
                messagebox.showwarning("REGISTRATION ERROR","PLEASE 🙏🙏🙏 FILL ALL SPACES",icon="warning")
        time.sleep(.5)
        root.destroy()
        global root2
        global regisname
        global regisage
        global regispassword
        root2 = ct.CTk()
        bg_image = Image.open("laptop.jpg")
        bg_image = bg_image.resize((1045, 660))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(root2, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        ct.set_appearance_mode("system")
        ct.set_default_color_theme("dark-blue")
        root2.title("Task Manager")
        root2.geometry("1045x660")

        dormlabel = ct.CTkLabel(root2,
                                text="Welcome  to  Task  Manager",
                                text_color="wheat",
                                font=("Arial", 60,"bold"),
                                fg_color="#1852C4",
                                bg_color="wheat",
                                width=1000,
                                height=200)
        dormlabel.pack(pady=20)
        nameframe= ctk.CTkFrame(root2,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        nameframe.pack(pady=30)
        namelabel = ct.CTkLabel(nameframe,
                        text="👤 USERNAME",
                        text_color="wheat",
                        font=("Arial", 12,"bold"))
        namelabel.grid(row=0, column=0)
        regisname = ct.CTkEntry(nameframe,
                        width=500,
                        height=40,
                        corner_radius=3,
                        text_color="wheat",
                        placeholder_text="Your name please",
                        border_color="#697BD1",
                        placeholder_text_color="wheat")
        regisname.grid(row=0, column=1,padx=5)
        def clearbox(entry):
            """
            clear the whole entry box
            """
            entry.delete(0,ctk.END)
            pass
        regisnameclear = ct.CTkButton(
            nameframe,
            text="🗑️clear",
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            font=("Heveltica", 10),
            fg_color="#C21616",
            hover_color="#E54B4B",
            border_width=1,
            border_color="wheat",
            command=lambda:clearbox(regisname)
        )
        regisnameclear.grid(row=0, column=2,padx=5)
        passwordframe= ctk.CTkFrame(root2,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        passwordframe.pack(pady=1)
        passwordlabel = ct.CTkLabel(passwordframe,
                        text="🔒 PASSWORD",
                        text_color="wheat",
                        font=("Arial", 12,"bold"))
        passwordlabel.grid(row=0, column=0)
        regispassword = ct.CTkEntry(passwordframe,
                        width=500,
                        height=40,
                        corner_radius=3,
                        text_color="wheat",
                        placeholder_text="Your pass please",
                        border_color="#697BD1",
                        placeholder_text_color="wheat",
                        show="*"
                        )
        regispassword.grid(row=0, column=1,padx=5)
        def showpassword():
            regispassword.configure(show="")
            regishidepassword.tkraise()
        def hidepassword():
            regispassword.configure(show="*")
            regishowpassword.tkraise()
        regishidepassword = ct.CTkButton(
            passwordframe,
            text="👁️hide",
            command=hidepassword,
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            fg_color="#C21616",
            font=("Heveltica", 10),
            hover_color="#E54B4B",
            border_width=1,
            border_color="wheat"
        )
        regishidepassword.grid(row=0, column=2,padx=5)
        
        regishowpassword = ct.CTkButton(
            passwordframe,
            text="👁️show",
            command=showpassword,
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            fg_color="#1852C4",
            font=("Heveltica", 10),
            hover_color="#697BD1",
            border_width=1,
            border_color="wheat"
        )
        regishowpassword.grid(row=0, column=2,padx=5)
        ageframe= ctk.CTkFrame(root2,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        ageframe.pack(pady=30)
        agelabel = ct.CTkLabel(ageframe,
                        text="🔞YOUR AGE  ",
                        text_color="wheat",
                        font=("Arial", 12,"bold"))
        agelabel.grid(row=0, column=0)
        regisage = ct.CTkEntry(ageframe,
                        width=500,
                        height=40,
                        corner_radius=3,
                        text_color="wheat",
                        placeholder_text="Your age please...",
                        border_color="#697BD1",
                        placeholder_text_color="wheat")
        regisage.grid(row=0, column=1,padx=5)
        
        regisageclear = ct.CTkButton(
            ageframe,
            text="🗑️clear",
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            font=("Heveltica", 10),
            fg_color="#C21616",
            hover_color="#E54B4B",
            border_width=1,
            border_color="wheat",
            command=lambda:clearbox(regisage)
        )
        regisageclear.grid(row=0, column=2,padx=5)
        button1  = ct.CTkButton(
                root2,
                text="R E G I S T E R",
                height=40,
                width=500,
                corner_radius=20,
                text_color="wheat",
                fg_color="#1852c4",
                font=("Heveltica", 30),
                hover_color="#4276df",
                command=registerfunction
                                )
        button1.pack(pady=20)
        label_reg = ct.CTkLabel(root2,
                        text="Already have an account?",
                        )
        label_reg.pack()
        button2 = ct.CTkButton(root2,
                        width=280,
                        text="login here",
                        fg_color="#1852c4",
                        hover_color="#4276df",
                        command=switch_to_login)
        button2.pack()
        root2.mainloop()



#################################  LOGIN PAGE  #####################################
def loginpage():
        #root = tk.Tk("My first")
        #POPUP
        global root
        global entry1
        global entry2
        root = ct.CTk()
        #Function to verify a username and password
        def login_to_database(username,password):
            global realerusername
            username = username.lower()
            try:
                    cursor.execute("select * from users where username=:h",{"h": f"{username}"})
                    data = cursor.fetchone()
                    if data[1] == password:
                        messagebox.showinfo(title="LOGIN DETAILS",message="LOGGING IN ")
                        realusername:str = data[0]
                        realerusername = realusername
                        return data[0]
                    else :
                        return "invalid login credentials"
            except Exception as e:
                return "user does not exist"
        def login():
            if entry1.get().strip() and entry2.get().strip():
                if login_to_database(entry1.get().strip(),entry2.get().strip()) == entry1.get().lower():
                        time.sleep(2)
                        root.destroy()
                        mainhomepage()
                elif login_to_database(entry1.get(),entry2.get()) =="user does not exist":
                    messagebox.showwarning("LOGIN ERROR","USER DOES NOT EXIST PLEASE REGISTER")
                else:
                    count.append("f")
                    if len(count)<5:
                        messagebox.showerror("LOG IN",f'INCORRECT PASSWORD YOU HAVE {abs(len(count)-5)} NUMBER OF ATTEMPTS LEFT')
                        
                    else:
                        popup(root,''' SORRY,
                                YOU ARE OUT OF CHANCES''',
                                    5000)
                        
                        
            else:
                messagebox.showerror("LOGIN ERROR","PLEASE FILL ALL SPACES",icon="warning")
        ct.set_appearance_mode("system")
        ct.set_default_color_theme("dark-blue")
        root.title("Task Manager")
        root.geometry("1045x660")
        bg_image = Image.open("laptop.jpg")
        bg_image = bg_image.resize((1045, 660))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        dormlabel = ct.CTkLabel(root,
                                text="Welcome  to  Task  Manager",
                                text_color="wheat",
                                font=("Arial", 60,"bold"),
                                fg_color="#1852C4",
                                bg_color="wheat",
                                width=1000,
                                height=200)
        dormlabel.pack(pady=20)
        entry1frame= ctk.CTkFrame(root,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        entry1frame.pack(pady=40)
        entry1label = ct.CTkLabel(entry1frame,
                        text="👤 USERNAME",
                        text_color="wheat",
                        font=("Arial", 12,"bold"))
        entry1label.grid(row=0, column=0)
        entry1 = ct.CTkEntry(entry1frame,
                        width=500,
                        height=40,
                        corner_radius=3,
                        text_color="wheat",
                        placeholder_text="Your name please",
                        border_color="#697BD1",
                        placeholder_text_color="wheat")
        entry1.grid(row=0, column=1,padx=5)
        def clear():
            """
            clear the whole entry box
            """
            entry1.delete(0,ctk.END)
            pass
        entry1showpassword = ct.CTkButton(
            entry1frame,
            text="🗑️clear",
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            font=("Heveltica", 10),
            fg_color="#C21616",
            hover_color="#E54B4B",
            border_width=1,
            border_color="wheat",
            command=clear
        )
        entry1showpassword.grid(row=0, column=2,padx=5)
        entry2frame= ctk.CTkFrame(root,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        entry2frame.pack(pady=1)
        entry2label = ct.CTkLabel(entry2frame,
                        text="🔒 PASSWORD",
                        text_color="wheat",
                        font=("Arial", 12,"bold"))
        entry2label.grid(row=0, column=0)
        entry2 = ct.CTkEntry(entry2frame,
                        width=500,
                        height=40,
                        corner_radius=3,
                        text_color="wheat",
                        placeholder_text="Your pass please",
                        border_color="#697BD1",
                        placeholder_text_color="wheat",
                        show="*"
                        )
        entry2.grid(row=0, column=1,padx=5)
        def showpassword():
            entry2.configure(show="")
            entry2hidepassword.tkraise()
        def hidepassword():
            entry2.configure(show="*")
            entry2showpassword.tkraise()
        entry2hidepassword = ct.CTkButton(
            entry2frame,
            text="👁️hide",
            command=hidepassword,
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            fg_color="#C21616",
            font=("Heveltica", 10),
            hover_color="#E54B4B",
            border_width=1,
            border_color="wheat"
        )
        entry2hidepassword.grid(row=0, column=2,padx=5)
        
        entry2showpassword = ct.CTkButton(
            entry2frame,
            text="👁️show",
            command=showpassword,
            width=10,
            height=10,
            corner_radius=10,
            text_color="wheat",
            fg_color="#1852C4",
            font=("Heveltica", 10),
            hover_color="#697BD1",
            border_width=1,
            border_color="wheat"
        )
        entry2showpassword.grid(row=0, column=2,padx=5)
        
        button1  = ct.CTkButton(
                root,
                text="L O G I N",
                height=40,
                width=500,
                corner_radius=20,
                text_color="wheat",
                fg_color="#1852C4",
                font=("Heveltica", 30),
                hover_color="#697BD1",
                command=login,
                bg_color="transparent"
                                )
        button1.pack(pady=20)
        forgotpasswordframe= ctk.CTkFrame(root,height=40,width=800, 
                                fg_color="#1852C4",
                                bg_color="transparent",
                                corner_radius=0)
        forgotpasswordframe.pack(pady=10)
        label_reg = ct.CTkLabel(forgotpasswordframe,
                        text="Forgot password?",
                        )
        label_reg.grid(row=0,column=0,padx=1)
        def forgotpassword(MASTER:ct.CTkToplevel,age,newpassword,username):
            try:
                cursor.execute("SELECT * FROM users where username=:n",{"n":f"{username.lower().strip()}"})
                data =cursor.fetchone()
                if isdigit(age) != "invalid":
                    if int(data[2]) == int(age):
                        if newpassword.strip() :
                            if len(newpassword.strip()) <6 or len(newpassword.strip())>24:
                                messagebox.showerror("PASSWORD CHANGE","MAKE SURE PASSWORD IS BETWEEN 6 AND 24 CHARACTERS!!!")
                                MASTER.lift()
                            elif len(re.findall(r'\s+',newpassword.strip())) >0:
                                messagebox.showerror("PASSWORD CHANGE","PASSWORD CANNOT HAVE SPACES IN BETWEEN")
                                MASTER.lift()
                            elif not ((len(re.findall(r'\d+',newpassword.strip())) !=0 or len(re.findall(r'[^a-zA-Z0-9]',newpassword.strip()))!=0) and len(re.findall(r'\w+',newpassword.strip()))!=0):
                                messagebox.showerror("PASSWORD CHANGE","PASSWORD MUST CONTAIN AT LEAST A SPECIAL CHARACTER, OR A NUMBER AND LETTERS",icon="warning")
                                MASTER.lift()
                            else:
                                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (newpassword, username.lower().strip()))
                                conn.commit()
                                messagebox.showinfo("PASSWORD CHANGE","PASSWORD CHANGED SUCCESSFULLY")
                                MASTER.destroy()
                    else:
                        messagebox.showerror("PASSWORD CHANGE","WRONG CREDENTIALS")
                        MASTER.lift()
                else:
                    messagebox.showerror("PASSWORD CHANGE","PLEASE MAKE SURE AGE IS AN INTEGER")
                    MASTER.lift()
            except Exception as e:
                messagebox.showerror("PASSWORD CHANGE",f"An error occured {e}")
                MASTER.lift()
        def popcollectforgotpassword(master,title:str):
            """
            Create a popup window for changing the user's password.
            """
            popit = ct.CTkToplevel(master)
            popit.title(title)
            popit.overrideredirect(True)
            label = ct.CTkLabel(popit,
                                text_color="white",
                                text="Your name")
            label.pack(pady=5)
            name  = ct.CTkEntry(popit,placeholder_text="Your name ....",
                                    text_color="#0f232b",
                                    placeholder_text_color="#358daf",
                                    fg_color="wheat",
                                    border_color="#358daf")
            name.pack(pady=1)
            labe1 = ct.CTkLabel(popit,
                                text_color="white",
                                text="Your age")
            labe1.pack(pady=5)
            age = ct.CTkEntry(popit,placeholder_text="Your age....",
                                    text_color="#0f232b",
                                    placeholder_text_color="#358daf",
                                    fg_color="wheat",
                                    border_color="#358daf")
            age.pack(pady=1)
            labe2 = ct.CTkLabel(popit,
                                text_color="white",
                                text="Your new password")
            labe2.pack(pady=5)
            newpassword = ct.CTkEntry(popit,placeholder_text="Your new password",
                                    text_color="#0f232b",
                                    placeholder_text_color="#358daf",
                                    border_color="#358daf",
                                    fg_color="wheat")
            newpassword.pack(pady=1)
            deleteframe = ctk.CTkFrame(popit, fg_color="gray", bg_color="white")
            deleteframe.pack(pady=5)
            changebtn = ct.CTkButton(deleteframe,
                                    text="CHANGE",
                                    fg_color="#1cb91c",
                                    hover_color="#7bff7b",
                                    command=lambda: forgotpassword(popit,age.get(),newpassword.get(),name.get()),
                                    corner_radius=0)
            changebtn.grid(row=1,column=0)
            cancelbtn = ct.CTkButton(deleteframe, text="Cancel",
                                    command=lambda: popit.destroy(),
                                    corner_radius=0)
            cancelbtn.grid(row=1,column=1)

        forgotbtn= ct.CTkButton(
            forgotpasswordframe,
            text="click here",
            height=10,
            width=10,
            corner_radius=7,
            text_color="wheat",
            fg_color="#C43718",
            font=("Heveltica", 10),
            hover_color="#D17569",
            bg_color="transparent",
            border_color="white",
            command=lambda: popcollectforgotpassword(forgotpasswordframe,"FORGOT PASSWORD")
                            )
        forgotbtn.grid(row=0,column=1,padx=10)
        button2 = ct.CTkButton(root,
                        width=280,
                        text="register ➕ here",
                        command=register,
                        text_color="wheat",
                        fg_color="#1852C4",
                        font=("Heveltica", 10),
                        hover_color="#697BD1",
                        bg_color="transparent"
                        )
        button2.pack()
        root.mainloop()
        
        
        """Label(root,text="O ye olorun")
        label1.grid(column=24)
        input1 = tk.CEntry(root,bg="magenta",width=100,border=2 )
        input1.grid(column=70)
        tk.Frame(root,bg="blue",border=4).grid() """
        
loginpage()




#################################  DATABASE  #####################################

#cursor.execute("""CREATE TABLE users(
#                    username text,
#                    password text,
#                    age integer
#                    )
#        """)
conn.commit()

#cursor.execute("""create table task (
#                    name text,
#                    tasks text,
#                    isdone text
#                    )
#            """)
conn.commit()
    


""" def add_to_database(username,password,age):
    username = username.strip().lower()
    password = password.strip()
    age = int(age)
    allis =cursor.execute("select * from users where username=:u",{"u":f"{username}"})
    lallis = len(allis.fetchall())
    if lallis ==0:
        cursor.execute("INSERT INTO users (username,password,age) VALUES (?,?,?)",(username,password,age))
        conn.commit()
        return "Successful"
    else:
            return "User already exist" """
    
    
    
def login_to_database(username,password):
    username = username.lower()
    try:
            cursor.execute("select * from users where username=:h",{"h": f"{username}"})
            data = cursor.fetchone()
            print(data[0])
            if data[1] == password:
                messagebox.showinfo(title="LOGIN DETAILS",message="LOGGING IN ")
                return data[0]
            else :
                return "invalid login credentials"
    except Exception as e:
        messagebox.showinfo( e,"USER DOES NOT EXIST",icon="error")
def getit():
    global rename
    global repass
    global reage
    global loginname
    global loginpass
    rename = regisname.get().lower()
    repass = regispassword.get()
    reage = int(regisage.get())
    loginname = entry1.get()
    loginpass = entry2.get()

""" def login():
        if login_to_database(loginname.lower(),loginpass) == loginname.lower():
                time.sleep(2)
                root.destroy()
                mainhomepage() """


''' def registerfunction():
        if add_to_database(rename,repass,reage) == "Successful":
            messagebox.showinfo("Registration","""Successfully Registered
                                                You can now LOGIN""")
            root2.destroy()
            loginpage() '''
