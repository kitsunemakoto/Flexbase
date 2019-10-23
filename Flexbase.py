from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from os import path
from configparser import ConfigParser
import pymysql
import tkinter as tk
import threading
import hashlib


class SecurityWindow_Class():
    def __init__(self, master):
        self.master = master
        width = 320
        height = 100
        self.x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry("320x120+%d+%d" % (self.x, self.y))
        self.master.resizable(False, False)
        self.master.title("Flexbase - SECURITY")

        frame = tk.Frame(self.master)
        frame.pack(side=TOP, anchor=CENTER)

        tk.Button(frame, text="USER", width=22, command=self.GoTo_USERWINDOW).grid(row=0, column=0, sticky=NSEW)
        tk.Button(frame, text="PROFILE", width=22, command=self.GoTo_PROFILEWINDOW).grid(row=1, column=0, sticky=NSEW)
        tk.Button(frame, text="USERPROFILE", width=22, command=self.GoTo_USERPROFILEWINDOW).grid(row=2, column=0, sticky=NSEW)
        tk.Button(frame, text="ADD USERS TO PROFILE", width=22, command=self.GoTo_ADDUSERSTOPROFWINDOW).grid(row=3, column=0, sticky=NSEW)


    def GoTo_USERWINDOW(self):
        root2 = tk.Toplevel(self.master)
        UserWindow_Class(root2)


    def GoTo_PROFILEWINDOW(self):
        root3 = tk.Toplevel(self.master)
        ProfileWindow_Class(root3)


    def GoTo_USERPROFILEWINDOW(self):
        root4 = tk.Toplevel(self.master)
        UserProfileWindow_Class(root4)


    def GoTo_ADDUSERSTOPROFWINDOW(self):
        root5 = tk.Toplevel(self.master)
        AddUsersToProfileWindow_Class(root5)


class UserWindow_Class():
    def __init__(self, master):
        self.master = master
        width = 320
        height = 100
        self.x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry("+%d+%d" % (self.x, self.y))
        self.master.minsize(width=540, height=280)
        self.master.maxsize(width=820, height=540)
        self.master.title("Flexbase - USER")

        self.DatabaseUpdatedInfo_StringVariable = tk.StringVar()
        self.DatabaseUpdatedInfo_StringVariable.set("")

        # ---------- CREATE WIDGETS TO INITIALIZE ---------
        # ------- LABELS -------
        tk.Label(self.master, text="UserID: ", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)  # Create label
        tk.Label(self.master, text="First Name: ", fg="black", font="Arial 8 bold").grid(row=1, column=0, sticky=W)
        tk.Label(self.master, text="Surname: ", fg="black", font="Arial 8 bold").grid(row=2, column=0, sticky=W)
        tk.Label(self.master, text="E-Mail Address: ", fg="black", font="Arial 8 bold").grid(row=3, column=0, sticky=W)
        tk.Label(self.master, text="Username: ", fg="black", font="Arial 8 bold").grid(row=4, column=0, sticky=W)
        tk.Label(self.master, text="Password: ", fg="black", font="Arial 8 bold").grid(row=5, column=0, sticky=W)

        # ------- TEXTBOXES -------
        self.UserID_TextBox = tk.Entry(self.master, width=7, bg="white")
        self.UserID_TextBox.grid(row=0, column=1, sticky=W)
        self.FirstName_TextBox = tk.Entry(self.master, width=60, bg="white")
        self.FirstName_TextBox.grid(row=1, column=1, sticky=W)
        self.Surname_TextBox = tk.Entry(self.master, width=60, bg="white")
        self.Surname_TextBox.grid(row=2, column=1, sticky=W)
        self.Email_TextBox = tk.Entry(self.master, width=60, bg="white")
        self.Email_TextBox.grid(row=3, column=1, sticky=W)
        self.Username_TextBox = tk.Entry(self.master, width=20, bg="white")
        self.Username_TextBox.grid(row=4, column=1, sticky=W)
        self.Password_TextBox = tk.Entry(self.master, show="*", width=20, bg="white")
        self.Password_TextBox.grid(row=5, column=1, sticky=W)

        self.UserID_TextBox.bind('<Return>', lambda e: self.FetchRow())  # Listens for the Enter key only if the UserID_TextBox is active and clicked on
        self.FirstName_TextBox.bind('<Return>', lambda e: self.Surname_TextBox.focus())
        self.Surname_TextBox.bind('<Return>', lambda e: self.Email_TextBox.focus())
        self.Email_TextBox.bind('<Return>', lambda e: self.Username_TextBox.focus())
        self.Username_TextBox.bind('<Return>', lambda e: self.Password_TextBox.focus())
        self.Password_TextBox.bind('<Return>', lambda e: self.SubmitInfo())

        self.a = tk.Entry()
        self.b = tk.Entry()
        self.c = tk.Entry()

        self.GetData_Frame = tk.Frame()
        self.GetData_Frame2 = tk.Frame()
        self.canvas = tk.Canvas()
        self.canvas_frame = None
        self.vsb = tk.Scrollbar()

        self.entries = []
        self.id_list = []

        # ------- BUTTONS -------
        tk.Button(self.master, text="Delete", width=8, command=self.DeleteEntry).grid(row=3, column=3, sticky=E)
        tk.Button(self.master, text="Clear", width=8, command=self.ClearEntry).grid(row=4, column=3, sticky=E)
        tk.Button(self.master, text="OK", width=6, height=2, command=self.SubmitInfo).grid(row=6, column=1, sticky=W)
        tk.Button(self.master, text="Cancel", width=6, height=2, command=self.Cancel).grid(row=6, column=0, columnspan=2)

        tk.Label(self.master, textvariable=self.DatabaseUpdatedInfo_StringVariable, fg="green", font="Arial 10 bold").grid(row=7, column=0, columnspan=5, sticky=W)  # Line for "Edit complete" with time.sleep()

        ttk.Separator(self.master, orient=HORIZONTAL).grid(row=8, column=0, columnspan=7, pady=15.0, sticky=NSEW)

        # ------- NOTEBOOK/TABS -------
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=9, column=0, columnspan=4, sticky=NSEW)
        self.page1 = tk.Frame(self.notebook)
        self.page2 = tk.Frame(self.notebook)
        self.notebook.add(self.page1, text="Mass Editing Mode")
        self.notebook.add(self.page2, text="Listbox Mode")
        self.FetchDataButton = tk.Button(self.page1, text="Fetch Data", width=16, height=2, command=self.GetData)
        self.FetchDataButton.grid(row=0, column=0, sticky=NSEW)


    def DeleteEntry(self):
        if self.UserID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "Do you really want to delete this entry from the database?\nWARNING: Deleted data cannot be recovered.", parent=self.master)
            if ConfirmationMessageBox == "yes":
                try:
                    ValidationCheck = cursor.execute("SELECT * FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get())) #Check if entry is valid based on UserID
                    if ValidationCheck == 1:
                        cursor.execute("DELETE FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get()))
                        db.commit()
                        self.DatabaseUpdatedInfo_StringVariable.set("Entry deleted successfully")
                        threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()

                        #Clear TextBoxes
                        self.UserID_TextBox.delete(0, END)
                        self.FirstName_TextBox.delete(0, END)
                        self.Surname_TextBox.delete(0, END)
                        self.Email_TextBox.delete(0, END)
                        self.Username_TextBox.delete(0, END)
                    else:
                        tk.messagebox.showerror("Flexbase", "This entry you tried to delete does not exist in the table of the database you are connected.\nEnsure all the information provided is correct.", parent=self.master)
                except:
                    self.DatabaseUpdatedInfo_StringVariable.set("Failed to delete entry")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()


    def ClearEntry(self):
        self.UserID_TextBox.delete(0, END)
        self.FirstName_TextBox.delete(0, END)
        self.Surname_TextBox.delete(0, END)
        self.Email_TextBox.delete(0, END)
        self.Username_TextBox.delete(0, END)
        self.Password_TextBox.delete(0, END)


    def Cancel(self):
        if (self.UserID_TextBox.get() and self.FirstName_TextBox.get()) or (self.FirstName_TextBox.get() and self.Surname_TextBox.get()) or self.UserID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "You have an unfinished entry and it will be lost if the window would exit now.\nDo you really want to exit?", parent=self.master)
            if ConfirmationMessageBox == "yes":
                self.master.destroy()
        elif len(self.entries) >= 3:
            ConfirmationMessageBox2 = tk.messagebox.askquestion("Flexbase", "You have made changes in the Mass Editing mode and they will be lost if the window would exit now.\nDo you really want to exit?", parent=self.master)
            if ConfirmationMessageBox2 == "yes":
                self.master.destroy()
        else:
            self.master.destroy()


    def ShiftEnter(self, currentpos):
        currentpos += 1
        try:
            newpos = self.GetData_Frame2.grid_slaves(currentpos, 0)
            newpos[0].focus()
        except:
            pass


    def onMouseWheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")


    def onFrameConfigure(self, event):
        canvas_width = event.width
        self.canvas.config(width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def GetData(self):
        self.FetchDataButton.destroy()
        cursor.execute("SELECT * FROM SEC_USER")
        results = cursor.fetchall()

        self.GetData_Frame.update_idletasks()

        self.GetData_Frame.destroy()
        self.GetData_Frame = tk.Frame(self.page1)
        self.GetData_Frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.GetData_Frame, highlightthickness=0)
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
        self.GetData_Frame2 = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self.GetData_Frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, rowspan=1000, column=7, sticky='ns')
        self.canvas.grid(row=0, column=0)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.GetData_Frame2, anchor='nw')

        tk.Label(self.GetData_Frame2, text=SQL_USERID, fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.GetData_Frame2, text=SQL_FIRSTNAME, fg="black", font="Arial 8 bold").grid(row=0, column=1, sticky=W)
        tk.Label(self.GetData_Frame2, text=SQL_SURNAME, fg="black", font="Arial 8 bold").grid(row=0, column=2, sticky=W)
        tk.Label(self.GetData_Frame2, text=SQL_USERNAME, fg="black", font="Arial 8 bold").grid(row=0, column=3, sticky=W)
        tk.Label(self.GetData_Frame2, text=SQL_EMAIL, fg="black", font="Arial 8 bold").grid(row=0, column=4, sticky=W)
        tk.Button(self.GetData_Frame2, text="Refresh", width=10, fg="red", font="Arial 8 bold", command=self.Refresh).grid(row=0, column=5, sticky=E)

        firstname_list = []
        surname_list = []
        username_list = []
        email_list = []

        self.id_list.clear()
        firstname_list.clear()
        surname_list.clear()
        username_list.clear()
        email_list.clear()
        self.entries.clear()

        RowCounter = 2
        ListCounter = 0

        for row in results:  # Page 1 TAB
            self.id_list.append(row[SQL_USERID])
            self.a = tk.Entry(self.GetData_Frame2, fg="black", font="Arial 8 bold")
            self.a.grid(row=RowCounter, column=0, sticky=W)
            self.a.insert(0, row[SQL_USERID])
            self.entries.append(self.a)
            firstname_list.append(row[SQL_FIRSTNAME])
            self.b = tk.Entry(self.GetData_Frame2, fg="black", font="Arial 8 bold")
            self.b.grid(row=RowCounter, column=1, sticky=W)
            self.b.insert(0, row[SQL_FIRSTNAME])
            self.entries.append(self.b)
            surname_list.append(row[SQL_SURNAME])
            self.c = tk.Entry(self.GetData_Frame2, fg="black", font="Arial 8 bold")
            self.c.grid(row=RowCounter, column=2, sticky=W)
            self.c.insert(0, row[SQL_SURNAME])
            self.entries.append(self.c)
            username_list.append(row[SQL_USERNAME])
            self.d = tk.Entry(self.GetData_Frame2, fg="black", font="Arial 8 bold")
            self.d.grid(row=RowCounter, column=3, sticky=W)
            self.d.insert(0, row[SQL_USERNAME])
            self.entries.append(self.d)
            email_list.append(row[SQL_EMAIL])
            self.e = tk.Entry(self.GetData_Frame2, width=35, fg="black", font="Arial 8 bold")
            self.e.grid(row=RowCounter, column=4, sticky=W)
            self.e.insert(0, row[SQL_EMAIL])
            self.e.bind("<Return>", lambda event, CurrentPos=self.e.grid_info(): self.ShiftEnter(CurrentPos['row']))
            self.entries.append(self.e)
            tk.Button(self.GetData_Frame2, text="Select Row", command=lambda CurrentValue=row: [self.SelectRow(CurrentValue[SQL_USERID], CurrentValue[SQL_FIRSTNAME], CurrentValue[SQL_SURNAME], CurrentValue[SQL_USERNAME], CurrentValue[SQL_EMAIL])]).grid(row=RowCounter, column=5, columnspan=6)

            for obj in (self.a, self.b, self.c, self.d, self.e):
                def double_click(ev, CurrentValue=row, RowCounter=RowCounter - 1):
                    print("selected row:", RowCounter)  # DEBUGGING PURPOSES
                    # Clear TextBoxes first
                    self.UserID_TextBox.delete(0, END)
                    self.FirstName_TextBox.delete(0, END)  # 0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
                    self.Surname_TextBox.delete(0, END)
                    self.Email_TextBox.delete(0, END)
                    self.Username_TextBox.delete(0, END)

                    # Then proceed to filling out the new user info
                    self.UserID_TextBox.insert(0, CurrentValue[SQL_USERID])
                    self.FirstName_TextBox.insert(0, CurrentValue[SQL_FIRSTNAME])
                    self.Surname_TextBox.insert(0, CurrentValue[SQL_SURNAME])
                    self.Username_TextBox.insert(0, CurrentValue[SQL_USERNAME])
                    self.Email_TextBox.insert(0, CurrentValue[SQL_EMAIL])

                obj.bind("<Double-Button>", double_click)

            RowCounter += 1
            ListCounter += 1

        tk.Button(self.GetData_Frame2, text="SUBMIT ENTRIES", command=self.SaveMassEdit).grid(row=RowCounter+2, column=2, columnspan=3)
        self.GetData_Frame2.bind("<Configure>", self.onFrameConfigure)

        tk.Label(self.page2, text=SQL_USERID, fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.page2, text=SQL_FIRSTNAME, fg="black", font="Arial 8 bold").grid(row=0, column=1, sticky=W)
        tk.Label(self.page2, text=SQL_SURNAME, fg="black", font="Arial 8 bold").grid(row=0, column=2, sticky=W)
        tk.Label(self.page2, text=SQL_USERNAME, fg="black", font="Arial 8 bold").grid(row=0, column=3, sticky=W)
        tk.Label(self.page2, text=SQL_EMAIL, fg="black", font="Arial 8 bold").grid(row=0, column=4, sticky=W)
        listbox1 = Listbox(self.page2, selectmode=SINGLE)
        listbox1.grid(row=1, column=0, sticky=NSEW)
        listbox2 = Listbox(self.page2, selectmode=SINGLE)
        listbox2.grid(row=1, column=1, sticky=NSEW)
        listbox3 = Listbox(self.page2, selectmode=SINGLE)
        listbox3.grid(row=1, column=2, sticky=NSEW)
        listbox4 = Listbox(self.page2, selectmode=SINGLE)
        listbox4.grid(row=1, column=3, sticky=NSEW)
        listbox5 = Listbox(self.page2, selectmode=SINGLE)
        listbox5.grid(row=1, column=4, sticky=NSEW)
        for row in self.id_list:
            listbox1.insert(END, row)
        for row in firstname_list:
            listbox2.insert(END, row)
        for row in surname_list:
            listbox3.insert(END, row)
        for row in username_list:
            listbox4.insert(END, row)
        for row in email_list:
            listbox5.insert(END, row)


    def SaveMassEdit(self):
        n = 5
        i = 0
        temp_list = []
        for index, value in enumerate(self.entries, 1):
            temp_list.append(value.get())
            if index % n == 0:
                #print("--- Seperator ---") #DEBUG
                #print("List: ", temp_list) #DEBUG
                #print("Currently on: ", self.userProfileID_list[i]) #DEBUG
                SQL_UPDATE = "UPDATE SEC_USER SET %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_USERID, temp_list[0], SQL_FIRSTNAME, temp_list[1], SQL_SURNAME, temp_list[2], SQL_USERNAME, temp_list[3], SQL_EMAIL, temp_list[4], SQL_USERID, self.id_list[i])
                try:
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    i += 1
                    temp_list.clear()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entries. Ensure all entries are in the correct format.", parent=self.master)
        self.DatabaseUpdatedInfo_StringVariable.set("Entries updated successfully")
        threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()


    def Refresh(self):
        self.GetData()


    def SelectRow(self, UserID, First_Name, Surname, Username, Email):
        # Clear TextBoxes first
        self.UserID_TextBox.delete(0,END)
        self.FirstName_TextBox.delete(0,END)  # 0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
        self.Surname_TextBox.delete(0, END)
        self.Email_TextBox.delete(0, END)
        self.Username_TextBox.delete(0, END)

        # Then proceed to filling out the new user info
        self.UserID_TextBox.insert(0, UserID)
        self.FirstName_TextBox.insert(0, First_Name)
        self.Surname_TextBox.insert(0, Surname)
        self.Username_TextBox.insert(0, Username)
        self.Email_TextBox.insert(0, Email)


    def FetchRow(self, event=None):
        if self.UserID_TextBox.get():
            try:
                int(self.UserID_TextBox.get()) #Checks if the user input is an integer
                try:
                    SQL_RETURNID = "SELECT %s FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, SQL_USERID, self.UserID_TextBox.get())
                    cursor.execute(SQL_RETURNID)
                    results = cursor.fetchone()
                    if results != None:
                        res = ",".join(("{} {}".format(*i) for i in results.items())) #Converts dictionary to string
                        del results
                        if self.UserID_TextBox.get() in res:
                            SQL_RETURNINFO = "SELECT * FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get())
                            cursor.execute(SQL_RETURNINFO)
                            RETURNINFO_Results = cursor.fetchall()
                            #print(str(RETURNINFO_Results)) # DEBUG PURPOSES ONLY
                            for row in RETURNINFO_Results:
                                #Clear TextBoxes first
                                self.FirstName_TextBox.delete(0, END) #0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
                                self.Surname_TextBox.delete(0, END)
                                self.Email_TextBox.delete(0, END)
                                self.Username_TextBox.delete(0, END)
                                self.Password_TextBox.delete(0, END)

                                #Then proceed to filling out the new user info
                                self.FirstName_TextBox.insert(0,row[SQL_FIRSTNAME])
                                self.Surname_TextBox.insert(0,row[SQL_SURNAME])
                                self.Email_TextBox.insert(0,row[SQL_EMAIL])
                                self.Username_TextBox.insert(0,row[SQL_USERNAME])
                    else:
                        self.FirstName_TextBox.delete(0, END)
                        self.Surname_TextBox.delete(0, END)
                        self.Email_TextBox.delete(0, END)
                        self.Username_TextBox.delete(0, END)
                        self.Password_TextBox.delete(0, END)

                        self.FirstName_TextBox.focus()
                except:
                    messagebox.showwarning("Flexbase", "Invalid input. Please make sure the value is correct.", parent=self.master)
            except:
                messagebox.showwarning("Flexbase", "You did not input a valid integer. Please make sure the value is correct.", parent=self.master)


    def SubmitInfo(self):
        SubmitInfo_Window = tk.Toplevel(self.master)
        SubmitInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        SubmitInfo_Window.title("Flexbase - USER | SUBMIT INFO OPTIONS")

        tk.Label(SubmitInfo_Window, text="Do you want to save your changes?", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save", command=lambda: self.SubmitInfo_Save(1, SubmitInfo_Window)).grid(row=1, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and Close", command=lambda: self.SubmitInfo_Save(2, SubmitInfo_Window)).grid(row=2, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and New", command=lambda: self.SubmitInfo_Save(3, SubmitInfo_Window)).grid(row=3, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Cancel", command=lambda: SubmitInfo_Window.destroy).grid(row=4, column=0, sticky=W)


    def SubmitInfo_Save(self, SaveEvent, SaveWindow):
        salt = b'\x124\x9e\xd3h\xb8h\x99t\xea\xbb\x1d\xaa\x9d\xa51' #TODO: Randomize this to defend from rainbow table attacks
        hex_password = hashlib.sha512(salt + bytes(self.Password_TextBox.get(), 'utf-8')).hexdigest()

        if SaveEvent == 1: # If Save clicked
            execute_command = "SELECT * FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_USER SET %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_FIRSTNAME, self.FirstName_TextBox.get(), SQL_SURNAME, self.Surname_TextBox.get(), SQL_USERNAME, self.Username_TextBox.get(), SQL_PASSWORD, hex_password, SQL_EMAIL, self.Email_TextBox.get(), SQL_USERID, self.UserID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USER (%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (SQL_USERID, SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME, SQL_PASSWORD, SQL_EMAIL, self.UserID_TextBox.get(), self.FirstName_TextBox.get(), self.Surname_TextBox.get(), self.Username_TextBox.get(), hex_password, self.Email_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 2: # If Save and Close clicked
            execute_command = "SELECT * FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_USER SET %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_FIRSTNAME, self.FirstName_TextBox.get(), SQL_SURNAME, self.Surname_TextBox.get(), SQL_USERNAME, self.Username_TextBox.get(), SQL_PASSWORD, hex_password, SQL_EMAIL, self.Email_TextBox.get(), SQL_USERID, self.UserID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USER (%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (SQL_USERID, SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME, SQL_PASSWORD, SQL_EMAIL, self.UserID_TextBox.get(), self.FirstName_TextBox.get(), self.Surname_TextBox.get(), self.Username_TextBox.get(), hex_password, self.Email_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    exit()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 3: # If Save and New clicked
            execute_command = "SELECT * FROM SEC_USER WHERE %s = '%s'" % (SQL_USERID, self.UserID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1: #If entry exists, update it
                try:
                    SQL_UPDATE = "UPDATE SEC_USER SET %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_FIRSTNAME, self.FirstName_TextBox.get(), SQL_SURNAME, self.Surname_TextBox.get(), SQL_USERNAME, self.Username_TextBox.get(), SQL_PASSWORD, hex_password, SQL_EMAIL, self.Email_TextBox.get(), SQL_USERID, self.UserID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    self.UserID_TextBox.delete(0, END)
                    self.FirstName_TextBox.delete(0, END)
                    self.Surname_TextBox.delete(0, END)
                    self.Email_TextBox.delete(0, END)
                    self.Username_TextBox.delete(0, END)
                    self.Password_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.UserID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else: #If entry does not exist, insert it
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USER (%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (SQL_USERID, SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME, SQL_PASSWORD, SQL_EMAIL, self.UserID_TextBox.get(), self.FirstName_TextBox.get(), self.Surname_TextBox.get(), self.Username_TextBox.get(), hex_password, self.Email_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    self.UserID_TextBox.delete(0, END)
                    self.FirstName_TextBox.delete(0, END)
                    self.Surname_TextBox.delete(0, END)
                    self.Email_TextBox.delete(0, END)
                    self.Username_TextBox.delete(0, END)
                    self.Password_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.UserID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)



class ProfileWindow_Class():
    def __init__(self, master):
        self.master = master
        width = 320
        height = 100
        self.x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry("+%d+%d" % (self.x, self.y))
        self.master.title("Flexbase - PROFILE")

        self.DatabaseUpdatedInfo_StringVariable = tk.StringVar()
        self.DatabaseUpdatedInfo_StringVariable.set("")

        # ---------- CREATE WIDGETS TO INITIALIZE ---------
        # ------- LABELS -------
        tk.Label(self.master, text="ProfileID: ", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.master, text="Profile Code: ", fg="black", font="Arial 8 bold").grid(row=1, column=0, sticky=W)
        tk.Label(self.master, text="Profile Description: ", fg="black", font="Arial 8 bold").grid(row=2, column=0, sticky=W)

        # ------- TEXTBOXES -------
        self.ProfileID_TextBox = tk.Entry(master, width=20, bg="white")
        self.ProfileID_TextBox.grid(row=0, column=1, sticky=W)
        self.ProfileCode_TextBox = tk.Entry(master, width=40, bg="white")
        self.ProfileCode_TextBox.grid(row=1, column=1, sticky=W)
        self.ProfileDescription_TextBox = tk.Entry(master, width=40, bg="white")
        self.ProfileDescription_TextBox.grid(row=2, column=1, sticky=W)

        self.ProfileID_TextBox.bind('<Return>', lambda e: self.FetchRow())  # Listens for the Enter key only if the UserID_TextBox is active and clicked on
        self.ProfileDescription_TextBox.bind('<Return>', lambda e: self.SubmitInfo())

        # ------- BUTTONS -------
        tk.Button(self.master, text="Delete", width=8, command=self.DeleteEntry).grid(row=1, column=2, sticky=E)
        tk.Button(self.master, text="Clear", width=8, command=self.ClearEntry).grid(row=2, column=2, sticky=E)
        tk.Label(self.master, textvariable=self.DatabaseUpdatedInfo_StringVariable, fg="green", font="Arial 10 bold").grid(row=4, column=0, columnspan=2, sticky=NSEW)
        tk.Button(self.master, text="OK", width=6, height=2, command=self.SubmitInfo).grid(row=3, column=1, sticky=W)
        tk.Button(self.master, text="Cancel", width=6, height=2, command=self.Cancel).grid(row=3, column=0, columnspan=3)

        ttk.Separator(self.master, orient=HORIZONTAL).grid(row=4, column=0, columnspan=7, pady=15.0, sticky=NSEW)

        # ------- NOTEBOOK/TABS -------
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=5, column=0, columnspan=4, sticky=NSEW)
        self.page1 = tk.Frame(self.notebook)
        self.page2 = tk.Frame(self.notebook)
        self.notebook.add(self.page1, text="Mass Editing Mode")
        self.notebook.add(self.page2, text="Listbox Mode")
        self.FetchDataButton = tk.Button(self.page1, text="Fetch Data", width=16, height=2, command=self.GetData)
        self.FetchDataButton.grid(row=0, column=0, sticky=NSEW)


    def DeleteEntry(self):
        if self.ProfileID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "Do you really want to delete this entry from the database?\nWARNING: Deleted data cannot be recovered.", parent=self.master)
            if ConfirmationMessageBox == "yes":
                try:
                    ValidationCheck = cursor.execute("SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())) #Check if entry is valid based on UserID
                    if ValidationCheck == 1:
                        cursor.execute("DELETE FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get()))
                        db.commit()
                        self.DatabaseUpdatedInfo_StringVariable.set("Entry deleted successfully")
                        threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()

                        #Clear TextBoxes
                        self.ProfileID_TextBox.delete(0, END)
                        self.ProfileCode_TextBox.delete(0, END)
                        self.ProfileDescription_TextBox.delete(0, END)
                    else:
                        tk.messagebox.showerror("Flexbase", "This entry you tried to delete does not exist in the table of the database you are connected.\nEnsure all the information provided is correct.", parent=self.master)
                except:
                    self.DatabaseUpdatedInfo_StringVariable.set("Failed to delete entry")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()


    def ClearEntry(self):
        self.ProfileID_TextBox.delete(0, END)
        self.ProfileCode_TextBox.delete(0, END)
        self.ProfileDescription_TextBox.delete(0, END)


    def Cancel(self):
        if (self.ProfileID_TextBox.get() and self.ProfileCode_TextBox.get()) or (self.ProfileID_TextBox.get() and self.ProfileDescription_TextBox.get()) or self.ProfileID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "You have an unfinished entry and it will be lost if the program would exit now.\nDo you really want to exit?", parent=self.master)
            if ConfirmationMessageBox == "yes":
                self.master.destroy()
            else:
                pass
        else:
            self.master.destroy()


    def GetData(self):
        self.FetchDataButton.destroy()
        cursor.execute("SELECT * FROM SEC_PROFILE")
        results = cursor.fetchall()

        tk.Label(self.page1, text=SQL_PROFILEID, fg="black", font="Arial 8 bold").grid(row=1, column=0, sticky=W)
        tk.Label(self.page1, text=SQL_PROFILECODE, fg="black", font="Arial 8 bold").grid(row=1, column=1, sticky=W)
        tk.Label(self.page1, text=SQL_PROFILEDESCRIPTION, fg="black", font="Arial 8 bold").grid(row=1, column=2, sticky=W)
        tk.Button(self.page1, text="Refresh", width=10, fg="red", font="Arial 8 bold", command=self.Refresh).grid(row=1, column=3, columnspan=5, sticky=E)


        profileID_list = []
        profileCode_list = []
        profileDescription_list = []

        RowCounter = 2
        ColumnCounter = -1
        ListCounter = 0
        RowListCounter = 0

        for row in results:  # Page 1 TAB
            ColumnCounter += 1
            profileID_list.append(row[SQL_PROFILEID])
            a = tk.Entry(self.page1, fg="black", font="Arial 8 bold")
            a.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            a.insert(0, row[SQL_PROFILEID])
            ColumnCounter += 1
            profileCode_list.append(row[SQL_PROFILECODE])
            b = tk.Entry(self.page1, fg="black", font="Arial 8 bold")
            b.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            b.insert(0, row[SQL_PROFILECODE])
            ColumnCounter += 1
            profileDescription_list.append(row[SQL_PROFILEDESCRIPTION])
            c = tk.Entry(self.page1, fg="black", font="Arial 8 bold")
            c.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            c.insert(0, row[SQL_PROFILEDESCRIPTION])
            tk.Button(self.page1, text="Select Row", command=lambda CurrentValue=row: [self.SelectRow(CurrentValue[SQL_PROFILEID], CurrentValue[SQL_PROFILECODE], CurrentValue[SQL_PROFILEDESCRIPTION])]).grid(row=RowCounter, column=ColumnCounter + 2, sticky=E)

            for obj in (a, b, c):
                def double_click(ev, CurrentValue=row, RowCounter=RowCounter - 1):
                    print("selected row:", RowCounter)  # DEBUGGING PURPOSES
                    # Clear TextBoxes first
                    self.ProfileID_TextBox.delete(0, END)
                    self.ProfileCode_TextBox.delete(0, END)  # 0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
                    self.ProfileDescription_TextBox.delete(0, END)

                    # Then proceed to filling out the new user info
                    self.ProfileID_TextBox.insert(0, CurrentValue[SQL_PROFILEID])
                    self.ProfileCode_TextBox.insert(0, CurrentValue[SQL_PROFILECODE])
                    self.ProfileDescription_TextBox.insert(0, CurrentValue[SQL_PROFILEDESCRIPTION])
                obj.bind("<Double-Button>", double_click)

            RowCounter += 1
            ColumnCounter = -1
            ListCounter += 1
            RowListCounter += 1

        RowCounter = 2 # RESET COUNTERS
        ColumnCounter = -1
        ListCounter = 0
        RowListCounter = 0

        tk.Label(self.page2, text="ProfileID", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.page2, text="Profile Code", fg="black", font="Arial 8 bold").grid(row=0, column=1, sticky=W)
        tk.Label(self.page2, text="Profile Description", fg="black", font="Arial 8 bold").grid(row=0, column=2, sticky=W)
        listbox1 = Listbox(self.page2, selectmode=SINGLE)
        listbox1.grid(row=1, column=0, sticky=NSEW)
        listbox2 = Listbox(self.page2, selectmode=SINGLE)
        listbox2.grid(row=1, column=1, sticky=NSEW)
        listbox3 = Listbox(self.page2, selectmode=SINGLE)
        listbox3.grid(row=1, column=2, sticky=NSEW)
        for row in profileID_list:
            listbox1.insert(END, row)
        for row in profileCode_list:
            listbox2.insert(END, row)
        for row in profileDescription_list:
            listbox3.insert(END, row)


    def Refresh(self):
        self.GetData()


    def SelectRow(self, ProfileID, ProfileCode, ProfileDescription):
        # Clear TextBoxes first
        self.ProfileID_TextBox.delete(0,END)
        self.ProfileCode_TextBox.delete(0,END)  # 0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
        self.ProfileDescription_TextBox.delete(0, END)

        # Then proceed to filling out the new user info
        self.ProfileID_TextBox.insert(0, ProfileID)
        self.ProfileCode_TextBox.insert(0, ProfileCode)
        self.ProfileDescription_TextBox.insert(0, ProfileDescription)


    def FetchRow(self, event=None):
        if self.ProfileID_TextBox.get():
            try:
                int(self.ProfileID_TextBox.get())  # Checks if the user input is an integer
                try:
                    int(self.ProfileID_TextBox.get()) #Checks if the user input is an integer
                    SQL_RETURNID = "SELECT %s FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, SQL_PROFILEID, self.ProfileID_TextBox.get())
                    cursor.execute(SQL_RETURNID)
                    results = cursor.fetchone()
                    res = ",".join(("{} {}".format(*i) for i in results.items())) #Converts dictionary to string
                    del results
                    if self.ProfileID_TextBox.get() in res:
                        SQL_RETURNINFO = "SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())
                        cursor.execute(SQL_RETURNINFO)
                        RETURNINFO_Results = cursor.fetchall()
                        #print(str(RETURNINFO_Results)) # DEBUG PURPOSES ONLY
                        for row in RETURNINFO_Results:
                            #Clear TextBoxes first
                            self.ProfileCode_TextBox.delete(0, END) #0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
                            self.ProfileDescription_TextBox.delete(0, END)

                            #Then proceed to filling out the new user info
                            self.ProfileCode_TextBox.insert(0,row[SQL_PROFILECODE])
                            self.ProfileDescription_TextBox.insert(0,row[SQL_PROFILEDESCRIPTION])
                except:
                    messagebox.showwarning("Flexbase", "Invalid input. Please make sure the value is correct.", parent=self.master)
            except:
                messagebox.showwarning("Flexbase", "You did not input a valid integer. Please make sure the value is correct.", parent=self.master)


    def SubmitInfo(self):
        SubmitInfo_Window = tk.Toplevel(self.master)
        SubmitInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        SubmitInfo_Window.title("Flexbase - PROFILE | SUBMIT INFO OPTIONS")

        tk.Label(SubmitInfo_Window, text="Do you want to save your changes?", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save", command=lambda: self.SubmitInfo_Save(1, SubmitInfo_Window)).grid(row=1, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and Close", command=lambda: self.SubmitInfo_Save(2, SubmitInfo_Window)).grid(row=2, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and New", command=lambda: self.SubmitInfo_Save(3, SubmitInfo_Window)).grid(row=3, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Cancel", command=lambda: SubmitInfo_Window.destroy).grid(row=4, column=0, sticky=W)


    def SubmitInfo_Save(self, SaveEvent, SaveWindow):
        if SaveEvent == 1: # If Save clicked
            execute_command = "SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_PROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get(), SQL_PROFILECODE, self.ProfileCode_TextBox.get(), SQL_PROFILEDESCRIPTION, self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_PROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_PROFILEID, SQL_PROFILECODE, SQL_PROFILEDESCRIPTION, self.ProfileID_TextBox.get(), self.ProfileCode_TextBox.get(), self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 2: # If Save and Close clicked
            execute_command = "SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_PROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get(), SQL_PROFILECODE, self.ProfileCode_TextBox.get(), SQL_PROFILEDESCRIPTION, self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_PROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_PROFILEID, SQL_PROFILECODE, SQL_PROFILEDESCRIPTION, self.ProfileID_TextBox.get(), self.ProfileCode_TextBox.get(), self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    exit()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 3: # If Save and New clicked
            execute_command = "SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1: #If entry exists, update it
                try:
                    SQL_UPDATE = "UPDATE SEC_PROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get(), SQL_PROFILECODE, self.ProfileCode_TextBox.get(), SQL_PROFILEDESCRIPTION, self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    self.ProfileID_TextBox.delete(0, END)
                    self.ProfileCode_TextBox.delete(0, END)
                    self.ProfileDescription_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.ProfileID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else: #If entry does not exist, insert it
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_PROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_PROFILEID, SQL_PROFILECODE, SQL_PROFILEDESCRIPTION, self.ProfileID_TextBox.get(), self.ProfileCode_TextBox.get(), self.ProfileDescription_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    self.ProfileID_TextBox.delete(0, END)
                    self.ProfileCode_TextBox.delete(0, END)
                    self.ProfileDescription_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.ProfileID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)



class UserProfileWindow_Class():
    def __init__(self, master):
        self.master = master
        width = 320
        height = 100
        self.x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry("+%d+%d" % (self.x, self.y))
        self.master.title("Flexbase - USERPROFILE")

        self.master.minsize(480, 180)
        self.master.maxsize(560, 720)

        self.DatabaseUpdatedInfo_StringVariable = tk.StringVar()
        self.DatabaseUpdatedInfo_StringVariable.set("")

        self.UpperFrame = tk.Frame(self.master)
        self.UpperFrame.grid(row=0, column=0)

        # ---------- CREATE WIDGETS TO INITIALIZE ---------
        # ------- LABELS -------
        tk.Label(self.UpperFrame, text="UserProfileID:", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=E)
        tk.Label(self.UpperFrame, text="UserID:", fg="black", font="Arial 8 bold").grid(row=1, column=0, sticky=E)
        tk.Label(self.UpperFrame, text="ProfileID:", fg="black", font="Arial 8 bold").grid(row=2, column=0, sticky=E)

        # ------- TEXTBOXES -------
        self.UserProfileID_TextBox = tk.Entry(self.UpperFrame, width=8, bg="white")
        self.UserProfileID_TextBox.grid(row=0, column=1)
        self.UserID_TextBox = tk.Entry(self.UpperFrame, width=8, bg="white")
        self.UserID_TextBox.grid(row=1, column=1)
        self.ProfileID_TextBox = tk.Entry(self.UpperFrame, width=8, bg="white")
        self.ProfileID_TextBox.grid(row=2, column=1)

        self.UserProfileID_TextBox.bind('<Return>', lambda e: self.FetchRow())  # Listens for the Enter key only if the UserID_TextBox is active and clicked on
        self.ProfileID_TextBox.bind('<Return>', lambda e: self.SubmitInfo())

        self.a = tk.Entry()
        self.b = tk.Entry()
        self.c = tk.Entry()

        self.GetData_Frame = tk.Frame()

        self.entries = []
        self.userProfileID_list = []

        # ------- BUTTONS -------
        tk.Button(self.UpperFrame, text="Delete", width=8, command=self.DeleteEntry).grid(row=0, column=3)
        tk.Button(self.UpperFrame, text="View Users", command=self.ViewUsers).grid(row=1, column=2, sticky=W)
        tk.Button(self.UpperFrame, text="Clear", width=8, command=self.ClearEntry).grid(row=1, column=3)
        tk.Button(self.UpperFrame, text="View Profiles", command=self.ViewProfiles).grid(row=2, column=2, sticky=W)
        tk.Button(self.UpperFrame, text="OK", width=8, height=1, command=self.SubmitInfo).grid(row=3, column=0, sticky=E)
        tk.Button(self.UpperFrame, text="Cancel", width=8, height=1, command=self.Cancel).grid(row=3, column=1)

        tk.Label(self.UpperFrame, textvariable=self.DatabaseUpdatedInfo_StringVariable, fg="green", font="Arial 10 bold").grid(row=4, column=0, columnspan=3, sticky=EW)

        ttk.Separator(self.UpperFrame, orient=HORIZONTAL).grid(row=5, column=0, columnspan=7, pady=12.0, sticky=EW)

        # ------- NOTEBOOK/TABS -------
        self.notebook = ttk.Notebook(self.UpperFrame)
        self.notebook.grid(row=6, column=0, columnspan=4, sticky=NSEW)
        self.page1 = tk.Frame(self.notebook)
        self.page2 = tk.Frame(self.notebook)
        self.notebook.add(self.page1, text="Mass Editing Mode")
        self.notebook.add(self.page2, text="Listbox Mode")
        self.FetchDataButton = tk.Button(self.page1, text="Fetch Data", width=16, height=2, command=self.GetData)
        self.FetchDataButton.grid(row=0, column=0)


    def DeleteEntry(self):
        if self.UserProfileID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "Do you really want to delete this entry from the database?\nWARNING: Deleted data cannot be recovered.", parent=self.master)
            if ConfirmationMessageBox == "yes":
                try:
                    ValidationCheck = cursor.execute("SELECT * FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get())) #Check if entry is valid based on UserID
                    if ValidationCheck == 1:
                        cursor.execute("DELETE FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get()))
                        db.commit()
                        self.DatabaseUpdatedInfo_StringVariable.set("Entry deleted successfully")
                        threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()

                        #Clear TextBoxes
                        self.UserProfileID_TextBox.delete(0, END)
                        self.UserID_TextBox.delete(0, END)
                        self.ProfileID_TextBox.delete(0, END)
                    else:
                        tk.messagebox.showerror("Flexbase", "This entry you tried to delete does not exist in the table of the database you are connected.\nEnsure all the information provided is correct.", parent=self.master)
                except:
                    self.DatabaseUpdatedInfo_StringVariable.set("Failed to delete entry")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()


    def ClearEntry(self):
        self.UserProfileID_TextBox.delete(0, END)
        self.UserID_TextBox.delete(0, END)
        self.ProfileID_TextBox.delete(0, END)


    def Cancel(self):
        if (self.UserProfileID_TextBox.get() and self.UserID_TextBox.get()) or (self.UserID_TextBox.get() and self.ProfileID_TextBox.get()) or self.UserProfileID_TextBox.get():
            ConfirmationMessageBox = tk.messagebox.askquestion("Flexbase", "You have an unfinished entry and it will be lost if the program would exit now.\nDo you really want to exit?", parent=self.master)
            if ConfirmationMessageBox == "yes":
                self.master.destroy()
            else:
                pass
        else:
            self.master.destroy()


    def ViewUsers(self):
        ShowInfo_Window = tk.Toplevel(self.master)
        ShowInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        ShowInfo_Window.title("Flexbase - VIEW USERS INFO")

        tk.Label(ShowInfo_Window, text="UserID", fg="black", font="Arial 11 bold").grid(row=0, column=0)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=1, rowspan=1000, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="First Name", fg="black", font="Arial 11 bold").grid(row=0, column=2)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=3, rowspan=1000, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="Surname", fg="black", font="Arial 11 bold").grid(row=0, column=4)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=5, rowspan=1000, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="Username", fg="black", font="Arial 11 bold").grid(row=0, column=6)

        ttk.Separator(ShowInfo_Window, orient=HORIZONTAL).grid(row=1, column=0, columnspan=8, pady=6.0, sticky=EW)

        cursor.execute("SELECT %s, %s, %s, %s FROM SEC_USER" % (SQL_USERID, SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME))
        result = cursor.fetchall()

        RowCounter = 2

        for value in result:
            tk.Label(ShowInfo_Window, text=value[SQL_USERID], fg="black", font="Arial 10").grid(row=RowCounter, column=0)
            tk.Label(ShowInfo_Window, text=value[SQL_FIRSTNAME], fg="black", font="Arial 10").grid(row=RowCounter, column=2)
            tk.Label(ShowInfo_Window, text=value[SQL_SURNAME], fg="black", font="Arial 10").grid(row=RowCounter, column=4)
            tk.Label(ShowInfo_Window, text=value[SQL_USERNAME], fg="black", font="Arial 10").grid(row=RowCounter, column=6)

            tk.Button(ShowInfo_Window, text="Select User", command=lambda CurrentValue=value: [self.UserID_TextBox.delete(0, END), self.UserID_TextBox.insert(0, CurrentValue[SQL_USERID]), ShowInfo_Window.destroy()]).grid(row=RowCounter, column=7, sticky=E)

            RowCounter += 1


    def ViewProfiles(self):
        ProfilesWindow = tk.Toplevel(self.master)
        ProfilesWindow.geometry("+%d+%d" % (self.x, self.y))
        ProfilesWindow.title("Flexbase - VIEW PROFILES INFO")

        ProfilesWindow.resizable(False, False)

        tk.Label(ProfilesWindow, text="ProfileID", fg="black", font="Arial 11 bold").grid(row=0, column=0, sticky=W)
        ttk.Separator(ProfilesWindow, orient=VERTICAL).grid(row=0, column=1, rowspan=6, padx=10.0, sticky=NS)

        tk.Label(ProfilesWindow, text="Profile Code", fg="black", font="Arial 11 bold").grid(row=0, column=2, sticky=W)
        ttk.Separator(ProfilesWindow, orient=VERTICAL).grid(row=0, column=3, rowspan=6, padx=10.0, sticky=NS)

        tk.Label(ProfilesWindow, text="Profile Description", fg="black", font="Arial 11 bold").grid(row=0, column=4, sticky=W)

        ttk.Separator(ProfilesWindow, orient=HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=5.0, sticky=EW)

        cursor.execute("SELECT * FROM SEC_PROFILE")
        result = cursor.fetchall()

        RowCounter = 2

        for value in result:
            tk.Label(ProfilesWindow, text=value[SQL_PROFILEID], fg="black", font="Arial 10").grid(row=RowCounter, column=0)
            tk.Label(ProfilesWindow, text=value[SQL_PROFILECODE], fg="black", font="Arial 10").grid(row=RowCounter, column=2)
            tk.Label(ProfilesWindow, text=value[SQL_PROFILEDESCRIPTION], fg="black", font="Arial 10").grid(row=RowCounter, column=4)

            tk.Button(ProfilesWindow, text="Select Row", command=lambda CurrentValue=value: [self.ProfileID_TextBox.delete(0, END), self.ProfileID_TextBox.insert(0, CurrentValue[SQL_UP_PROFILEID]), ProfilesWindow.destroy()]).grid(row=RowCounter, column=5, sticky=E)

            RowCounter += 1


    def GetData(self):
        self.FetchDataButton.destroy()
        cursor.execute("SELECT * FROM SEC_USERPROFILE")
        results = cursor.fetchall()

        self.GetData_Frame.destroy()
        self.GetData_Frame = tk.Frame(self.page1)
        self.GetData_Frame.grid(row=0, column=0, columnspan=5)

        tk.Label(self.GetData_Frame, text=SQL_USERPROFILEID, fg="black", font="Arial 8 bold").grid(row=1, column=0)
        tk.Label(self.GetData_Frame, text=SQL_UP_USERID, fg="black", font="Arial 8 bold").grid(row=1, column=1)
        tk.Label(self.GetData_Frame, text=SQL_UP_PROFILEID, fg="black", font="Arial 8 bold").grid(row=1, column=2)
        tk.Button(self.GetData_Frame, text="Refresh", width=10, fg="red", font="Arial 8 bold", command=self.Refresh).grid(row=1, column=3, columnspan=5, sticky=E)

        UP_userID_list = []
        UP_profileID_list = []
        self.userProfileID_list.clear()
        UP_userID_list.clear()
        UP_profileID_list.clear()
        self.entries.clear()

        RowCounter = 2
        ColumnCounter = -1
        ListCounter = 0
        RowListCounter = 0

        for row in results:  # Page 1 TAB
            ColumnCounter += 1
            self.userProfileID_list.append(row[SQL_USERPROFILEID])
            self.a = tk.Entry(self.GetData_Frame, fg="black", font="Arial 8 bold")
            self.a.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            self.a.insert(0, row[SQL_USERPROFILEID])
            self.entries.append(self.a)
            ColumnCounter += 1
            UP_userID_list.append(row[SQL_UP_USERID])
            self.b = tk.Entry(self.GetData_Frame, fg="black", font="Arial 8 bold")
            self.b.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            self.b.insert(0, row[SQL_UP_USERID])
            self.entries.append(self.b)
            ColumnCounter += 1
            UP_profileID_list.append(row[SQL_UP_PROFILEID])
            self.c = tk.Entry(self.GetData_Frame, fg="black", font="Arial 8 bold")
            self.c.grid(row=RowCounter, column=ColumnCounter, sticky=W)
            self.c.insert(0, row[SQL_UP_PROFILEID])
            self.entries.append(self.c)
            tk.Button(self.GetData_Frame, text="Select Row", command=lambda CurrentValue=row: [self.SelectRow(CurrentValue[SQL_USERPROFILEID], CurrentValue[SQL_UP_USERID], CurrentValue[SQL_UP_PROFILEID])]).grid(row=RowCounter, column=ColumnCounter + 2, sticky=E)
            tk.Button(self.GetData_Frame, text="Show Info", command=lambda CurrentValue=row: [self.ShowInfo(CurrentValue[SQL_USERPROFILEID], CurrentValue[SQL_UP_USERID], CurrentValue[SQL_UP_PROFILEID])]).grid(row=RowCounter, column=ColumnCounter + 3, sticky=E)

            for obj in (self.a, self.b, self.c):
                def double_click(ev, CurrentValue=row, RowCounter=RowCounter - 1):
                    print("selected row:", RowCounter)  # DEBUGGING PURPOSES
                    # Clear TextBoxes first
                    self.UserProfileID_TextBox.delete(0, END)
                    self.UserID_TextBox.delete(0, END)
                    self.ProfileID_TextBox.delete(0, END)

                    # Then proceed to filling out the new user info
                    self.UserProfileID_TextBox.insert(0, CurrentValue[SQL_USERPROFILEID])
                    self.UserID_TextBox.insert(0, CurrentValue[SQL_UP_USERID])
                    self.ProfileID_TextBox.insert(0, CurrentValue[SQL_UP_PROFILEID])
                obj.bind("<Double-Button>", double_click)

            RowCounter += 1
            ColumnCounter = -1
            ListCounter += 1
            RowListCounter += 1

        tk.Button(self.GetData_Frame, text="SUBMIT ENTRIES", command=self.SaveMassEdit).grid(row=RowCounter+2, column=1, sticky=NSEW)

        tk.Label(self.page2, text="UserProfileID", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.page2, text="UserID", fg="black", font="Arial 8 bold").grid(row=0, column=1, sticky=W)
        tk.Label(self.page2, text="ProfileID", fg="black", font="Arial 8 bold").grid(row=0, column=2, sticky=W)
        listbox1 = Listbox(self.page2, selectmode=SINGLE)
        listbox1.grid(row=1, column=0, sticky=NSEW)
        listbox2 = Listbox(self.page2, selectmode=SINGLE)
        listbox2.grid(row=1, column=1, sticky=NSEW)
        listbox3 = Listbox(self.page2, selectmode=SINGLE)
        listbox3.grid(row=1, column=2, sticky=NSEW)
        for row in self.userProfileID_list:
            listbox1.insert(END, row)
        for row in UP_userID_list:
            listbox2.insert(END, row)
        for row in UP_profileID_list:
            listbox3.insert(END, row)


    def SaveMassEdit(self):
        n = 3
        i = 0
        temp_list = []
        for index, value in enumerate(self.entries, 1):
            temp_list.append(value.get())
            if index % n == 0:
                #print("--- Seperator ---") #DEBUG
                #print("List: ", temp_list) #DEBUG
                #print("Currently on: ", self.userProfileID_list[i]) #DEBUG
                SQL_UPDATE = "UPDATE SEC_USERPROFILE SET %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_USERPROFILEID, temp_list[0], SQL_UP_USERID, temp_list[1], SQL_UP_PROFILEID, temp_list[2], SQL_USERPROFILEID, self.userProfileID_list[i])
                try:
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    i += 1
                    temp_list.clear()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entries. Ensure all entries are in the correct format.", parent=self.master)
        self.DatabaseUpdatedInfo_StringVariable.set("Entries updated successfully")
        threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()


    def Refresh(self):
        self.GetData()


    def ShowInfo(self, UserProfileID, UserID, ProfileID):
        ShowInfo_Window = tk.Toplevel(self.master)
        ShowInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        ShowInfo_Window.title("Flexbase - Show Info: UserProfileID " + str(UserProfileID))

        tk.Label(ShowInfo_Window, text="UserProfileID", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(ShowInfo_Window, text="UserID", fg="black", font="Arial 8 bold").grid(row=0, column=1, sticky=W)
        tk.Label(ShowInfo_Window, text="ProfileID", fg="black", font="Arial 8 bold").grid(row=0, column=2, sticky=W)

        ttk.Separator(ShowInfo_Window, orient=HORIZONTAL).grid(row=1, column=0, columnspan=5, sticky=NSEW)

        tk.Label(ShowInfo_Window, text=UserProfileID, fg="black", font="Arial 8").grid(row=2, column=0, sticky=W)
        tk.Label(ShowInfo_Window, text=UserID, fg="black", font="Arial 8").grid(row=2, column=1, sticky=W)
        tk.Label(ShowInfo_Window, text=ProfileID, fg="black", font="Arial 8").grid(row=2, column=2, sticky=W)
        if ProfileID == 1:
            tk.Label(ShowInfo_Window, text="Has Profile: Master", fg="black", font="Arial 10 bold").grid(row=2, column=3, sticky=W)
        elif ProfileID == 2:
            tk.Label(ShowInfo_Window, text="Has Profile: Super User", fg="black", font="Arial 10 bold").grid(row=2, column=3, sticky=W)

        ttk.Separator(ShowInfo_Window, orient=HORIZONTAL).grid(row=3, column=0, columnspan=5, sticky=NSEW)

        tk.Label(ShowInfo_Window, text="First Name", fg="black", font="Arial 8 bold").grid(row=4, column=0, sticky=W)
        tk.Label(ShowInfo_Window, text="Surname", fg="black", font="Arial 8 bold").grid(row=4, column=1, sticky=W)
        tk.Label(ShowInfo_Window, text="Username", fg="black", font="Arial 8 bold").grid(row=4, column=2, sticky=W)
        tk.Label(ShowInfo_Window, text="E-Mail Address", fg="black", font="Arial 8 bold").grid(row=4, column=3, sticky=W)

        execute_command = "SELECT %s, %s, %s, %s FROM SEC_USER WHERE %s = %d" % (SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME, SQL_EMAIL, SQL_USERID, UserID)
        cursor.execute(execute_command)
        result = cursor.fetchall()

        for value in result:
            tk.Label(ShowInfo_Window, text=value[SQL_FIRSTNAME], fg="black", font="Arial 8").grid(row=5, column=0, sticky=W)
            tk.Label(ShowInfo_Window, text=value[SQL_SURNAME], fg="black", font="Arial 8").grid(row=5, column=1, sticky=W)
            tk.Label(ShowInfo_Window, text=value[SQL_USERNAME], fg="black", font="Arial 8").grid(row=5, column=2, sticky=W)
            tk.Label(ShowInfo_Window, text=value[SQL_EMAIL], fg="black", font="Arial 8").grid(row=5, column=3, sticky=W)


    def SelectRow(self, UserProfileID, UserID, ProfileID):
        # Clear TextBoxes first
        self.UserProfileID_TextBox.delete(0, END)
        self.UserID_TextBox.delete(0, END)
        self.ProfileID_TextBox.delete(0, END)

        # Then proceed to filling out the new user info
        self.UserProfileID_TextBox.insert(0, UserProfileID)
        self.UserID_TextBox.insert(0, UserID)
        self.ProfileID_TextBox.insert(0, ProfileID)


    def FetchRow(self, event=None):
        if self.UserProfileID_TextBox.get():
            try:
                int(self.UserProfileID_TextBox.get())  # Checks if the user input is an integer
                try:
                    SQL_RETURNID = "SELECT %s FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, SQL_USERPROFILEID, self.UserProfileID_TextBox.get())
                    cursor.execute(SQL_RETURNID)
                    results = cursor.fetchone()
                    res = ",".join(("{} {}".format(*i) for i in results.items())) #Converts dictionary to string
                    del results
                    if self.UserProfileID_TextBox.get() in res:
                        SQL_RETURNINFO = "SELECT * FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get())
                        cursor.execute(SQL_RETURNINFO)
                        RETURNINFO_Results = cursor.fetchall()
                        #print(str(RETURNINFO_Results)) # DEBUG PURPOSES ONLY
                        for row in RETURNINFO_Results:
                            #Clear TextBoxes first
                            self.UserID_TextBox.delete(0, END) #0 means the very first character and END means the very last character. So, 0 to END means it clears all of it
                            self.ProfileID_TextBox.delete(0, END)

                            #Then proceed to filling out the new user info
                            self.UserID_TextBox.insert(0, row[SQL_UP_USERID])
                            self.ProfileID_TextBox.insert(0, row[SQL_UP_PROFILEID])
                except:
                    messagebox.showwarning("Flexbase", "Invalid input. Please make sure the value is correct.", parent=self.master)
            except:
                messagebox.showwarning("Flexbase", "You did not input a valid integer. Please make sure the value is correct.", parent=self.master)


    def SubmitInfo(self):
        SubmitInfo_Window = tk.Toplevel(self.master)
        SubmitInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        SubmitInfo_Window.title("Flexbase - USERPROFILE | SUBMIT INFO OPTIONS")

        tk.Label(SubmitInfo_Window, text="Do you want to save your changes?", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save", command=lambda: self.SubmitInfo_Save(1, SubmitInfo_Window)).grid(row=1, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and Close", command=lambda: self.SubmitInfo_Save(2, SubmitInfo_Window)).grid(row=2, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Save and New", command=lambda: self.SubmitInfo_Save(3, SubmitInfo_Window)).grid(row=3, column=0, sticky=W)
        tk.Button(SubmitInfo_Window, text="Cancel", command=lambda: SubmitInfo_Window.destroy).grid(row=4, column=0, sticky=W)


    def SubmitInfo_Save(self, SaveEvent, SaveWindow):
        if SaveEvent == 1: # If Save clicked
            execute_command = "SELECT * FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_USERPROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get(), SQL_UP_USERID, self.UserID_TextBox.get(), SQL_UP_PROFILEID, self.ProfileID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USERPROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_USERPROFILEID, SQL_UP_USERID, SQL_UP_PROFILEID, self.UserProfileID_TextBox.get(), self.UserID_TextBox.get(), self.ProfileID_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 2: # If Save and Close clicked
            execute_command = "SELECT * FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1:
                try:
                    SQL_UPDATE = "UPDATE SEC_USERPROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get(), SQL_UP_USERID, self.UserID_TextBox.get(), SQL_UP_PROFILEID, self.ProfileID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    SaveWindow.destroy()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else:
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USERPROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_USERPROFILEID, SQL_UP_USERID, SQL_UP_PROFILEID, self.UserProfileID_TextBox.get(), self.UserID_TextBox.get(), self.ProfileID_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    exit()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)
        elif SaveEvent == 3: # If Save and New clicked
            execute_command = "SELECT * FROM SEC_USERPROFILE WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get())
            cursor.execute(execute_command)
            if cursor.rowcount == 1: #If entry exists, update it
                try:
                    SQL_UPDATE = "UPDATE SEC_USERPROFILE SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (SQL_USERPROFILEID, self.UserProfileID_TextBox.get(), SQL_UP_USERID, self.UserID_TextBox.get(), SQL_UP_PROFILEID, self.ProfileID_TextBox.get())
                    cursor.execute(SQL_UPDATE)
                    db.commit()
                    self.UserProfileID_TextBox.delete(0, END)
                    self.UserID_TextBox.delete(0, END)
                    self.ProfileID_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.UserProfileID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry updated successfully")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error updating entry.\nEntry you tried to update does not exist.", parent=self.master)
            else: #If entry does not exist, insert it
                try:
                    SQL_SENDNEW = "INSERT INTO SEC_USERPROFILE (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (SQL_USERPROFILEID, SQL_UP_USERID, SQL_UP_PROFILEID, self.UserProfileID_TextBox.get(), self.UserID_TextBox.get(), self.ProfileID_TextBox.get())
                    cursor.execute(SQL_SENDNEW)
                    db.commit()
                    self.UserProfileID_TextBox.delete(0, END)
                    self.UserID_TextBox.delete(0, END)
                    self.ProfileID_TextBox.delete(0, END)
                    SaveWindow.destroy()
                    self.UserProfileID_TextBox.focus()
                    self.DatabaseUpdatedInfo_StringVariable.set("Entry created")
                    threading.Timer(3.5, self.DatabaseUpdatedInfo_StringVariable.set, [""]).start()
                except:
                    db.rollback()
                    messagebox.showwarning("Flexbase", "Error inserting new entry into the database.", parent=self.master)



class AddUsersToProfileWindow_Class():
    def __init__(self, master):
        self.master = master
        width = 320
        height = 100
        self.x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (height // 2)

        self.master.geometry("+%d+%d" % (self.x, self.y))
        self.master.title("Flexbase - ADD USERS TO PROFILE")

        self.master.minsize(427, 283)

        self.DatabaseUpdatedInfo_StringVariable = tk.StringVar()
        self.DatabaseUpdatedInfo_StringVariable.set("")

        self.UpperFrame = tk.Frame(self.master, relief=RAISED)
        self.UpperFrame.grid(row=0, column=0)

        # ---------- CREATE WIDGETS TO INITIALIZE ---------
        # ------- LABELS -------
        tk.Label(self.UpperFrame, text="ProfileID:", fg="black", font="Arial 8 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.UpperFrame, text="Profile Description:", fg="black", font="Arial 8 bold").grid(row=1, column=0, sticky=W)

        # ------- TEXTBOXES -------
        self.ProfileID_TextBox = tk.Entry(self.UpperFrame, width=5, bg="white")
        self.ProfileID_TextBox.grid(row=0, column=1, sticky=W)
        self.ProfileDescription_TextBox = tk.Entry(self.UpperFrame, width=14, bg="white")
        self.ProfileDescription_TextBox.grid(row=1, column=1, sticky=W)

        self.ProfileID_TextBox.bind('<Return>', lambda e: self.FetchRow())
        self.ProfileDescription_TextBox.bind('<Return>', lambda e: self.FetchRow())

        # ------- BUTTONS -------
        tk.Button(self.UpperFrame, text="View Profiles", command=self.ShowProfiles).grid(row=0, column=2, sticky=W)
        tk.Button(self.master, text="?", width=3, bg="lightblue", fg="white", font="Arial 10 bold", command=self.ShowHelpWindow).grid(row=0, column=2, sticky=E)
        tk.Button(self.UpperFrame, text="Clear", width=8, command=self.ClearEntry).grid(row=1, column=2, sticky=W)

        ttk.Separator(self.master, orient=HORIZONTAL).grid(row=1, column=0, columnspan=3, pady=10.0, sticky=EW)

        self.Frame = tk.Frame(self.master, relief=SUNKEN)
        self.Frame.grid(row=2, column=0, sticky=NSEW)

        tk.Label(self.Frame, text="Users connected to this profile:", fg="black", font="Arial 10 bold").grid(row=0, column=0, sticky=E)
        tk.Label(self.Frame, text="Users NOT connected to this profile:", fg="black", font="Arial 10 bold").grid(row=0, column=2, sticky=E)
        self.ConnectedListbox = Listbox(self.Frame, selectmode=SINGLE)
        self.ConnectedListbox.grid(row=1, column=0, rowspan=5)
        self.NotConnectedListbox = Listbox(self.Frame, selectmode=SINGLE)
        self.NotConnectedListbox.grid(row=1, column=2, rowspan=5)

        self.ConnectedListbox.bind("<Double-Button>", lambda e: self.ShowInfo(self.ConnectedListbox.get(self.ConnectedListbox.curselection())))
        self.NotConnectedListbox.bind("<Double-Button>", lambda e: self.ShowInfo(self.NotConnectedListbox.get(self.NotConnectedListbox.curselection())))

        tk.Button(self.Frame, text=">>>", command=lambda: self.AddRemove("remove")).grid(row=1, column=1)
        tk.Button(self.Frame, text="<<<", command=lambda: self.AddRemove("add")).grid(row=2, column=1)
        tk.Label(self.Frame, text="All changes you make are automatically saved.", fg="black", font="Arial 8 italic").grid(row=6, column=0, columnspan=3, sticky=EW)

        self.ConnectedList = []
        self.NotConnectedList = []


    def ClearEntry(self):
        self.ProfileID_TextBox.delete(0, END)
        self.ProfileDescription_TextBox.delete(0, END)


    def ShowProfiles(self):
        ProfilesWindow = tk.Toplevel(self.master)
        ProfilesWindow.geometry("+%d+%d" % (self.x, self.y))
        ProfilesWindow.title("Flexbase - PROFILES INFO")

        ProfilesWindow.resizable(False, False)

        tk.Label(ProfilesWindow, text="ProfileID", fg="black", font="Arial 11 bold").grid(row=0, column=0, sticky=W)
        ttk.Separator(ProfilesWindow, orient=VERTICAL).grid(row=0, column=1, rowspan=6, padx=10.0, sticky=NS)

        tk.Label(ProfilesWindow, text="Profile Code", fg="black", font="Arial 11 bold").grid(row=0, column=2, sticky=W)
        ttk.Separator(ProfilesWindow, orient=VERTICAL).grid(row=0, column=3, rowspan=6, padx=10.0, sticky=NS)

        tk.Label(ProfilesWindow, text="Profile Description", fg="black", font="Arial 11 bold").grid(row=0, column=4, sticky=W)

        ttk.Separator(ProfilesWindow, orient=HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=5.0, sticky=EW)

        cursor.execute("SELECT * FROM SEC_PROFILE")
        result = cursor.fetchall()

        RowCounter = 2

        for value in result:
            tk.Label(ProfilesWindow, text=value[SQL_PROFILEID], fg="black", font="Arial 10").grid(row=RowCounter, column=0)
            tk.Label(ProfilesWindow, text=value[SQL_PROFILECODE], fg="black", font="Arial 10").grid(row=RowCounter, column=2)
            tk.Label(ProfilesWindow, text=value[SQL_PROFILEDESCRIPTION], fg="black", font="Arial 10").grid(row=RowCounter, column=4)

            tk.Button(ProfilesWindow, text="Select Row", command=lambda CurrentValue=value: [self.SelectRow(CurrentValue[SQL_PROFILEID], CurrentValue[SQL_PROFILEDESCRIPTION]), ProfilesWindow.destroy()]).grid(row=RowCounter, column=5, sticky=E)
            RowCounter += 1


    def SelectRow(self, profileID, profileDescription):
        self.ProfileID_TextBox.delete(0, END)
        self.ProfileDescription_TextBox.delete(0, END)

        self.ProfileID_TextBox.insert(0, profileID)
        self.ProfileDescription_TextBox.insert(0, profileDescription)

        self.GetData()


    def ShowHelpWindow(self):
        HelpWindow = tk.Toplevel(self.master)
        HelpWindow.geometry("+%d+%d" % (self.x, self.y))
        HelpWindow.title("Flexbase")

        HelpWindow.minsize(562, 180)
        HelpWindow.maxsize(680, 480)

        tk.Label(HelpWindow, text="Shortcuts Documentation", fg="black", font="Arial 12 bold").grid(row=0, column=0)
        ttk.Separator(HelpWindow, orient=HORIZONTAL).grid(row=1, column=0, pady=6.0, sticky=EW)

        tk.Label(HelpWindow, text="1. If you already know a profile's ID number, type it into the ProfileID textbox and hit the ENTER key. \nIt will automatically fetch and display you all the info you need.", fg="black", font="Arial 9 bold").grid(row=2, column=0)
        tk.Label(HelpWindow, text="2. If you already know a profile's exact description, type it into the Profile Description textbox and hit the ENTER key. \nIt will automatically fetch and display you all the info you need.", fg="black", font="Arial 9 bold").grid(row=3, column=0)
        tk.Label(HelpWindow, text="3. The 2 listboxes at the bottom half of the window that display usernames give you the ability \nto double-click a specific username that's displayed and see more info about this entry.", fg="black", font="Arial 9 bold").grid(row=4, column=0)

        tk.Button(HelpWindow, text="Close", width=10, command=HelpWindow.destroy).grid(row=5, column=0)


    def ShowInfo(self, username):
        ShowInfo_Window = tk.Toplevel(self.master)
        ShowInfo_Window.geometry("+%d+%d" % (self.x, self.y))
        ShowInfo_Window.title("Flexbase - Show Info: " + username)

        tk.Label(ShowInfo_Window, text="UserID", fg="black", font="Arial 11 bold").grid(row=0, column=0, sticky=W)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=1, rowspan=3, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="First Name", fg="black", font="Arial 11 bold").grid(row=0, column=2, sticky=W)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=3, rowspan=3, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="Surname", fg="black", font="Arial 11 bold").grid(row=0, column=4, sticky=W)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=5, rowspan=3, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="Username", fg="black", font="Arial 11 bold").grid(row=0, column=6, sticky=W)
        ttk.Separator(ShowInfo_Window, orient=VERTICAL).grid(row=0, column=7, rowspan=3, padx=10.0, sticky=NS)

        tk.Label(ShowInfo_Window, text="E-Mail Address", fg="black", font="Arial 11 bold").grid(row=0, column=8, sticky=W)

        ttk.Separator(ShowInfo_Window, orient=HORIZONTAL).grid(row=1, column=0, columnspan=9, pady=6.0, sticky=EW)

        cursor.execute("SELECT %s, %s, %s, %s, %s FROM SEC_USER WHERE %s='%s'" % (SQL_USERID, SQL_FIRSTNAME, SQL_SURNAME, SQL_USERNAME, SQL_EMAIL, SQL_USERNAME, username))
        result = cursor.fetchall()

        for value in result:
            tk.Label(ShowInfo_Window, text=value[SQL_USERID], fg="black", font="Arial 10").grid(row=2, column=0)
            tk.Label(ShowInfo_Window, text=value[SQL_FIRSTNAME], fg="black", font="Arial 10").grid(row=2, column=2)
            tk.Label(ShowInfo_Window, text=value[SQL_SURNAME], fg="black", font="Arial 10").grid(row=2, column=4)
            tk.Label(ShowInfo_Window, text=value[SQL_USERNAME], fg="black", font="Arial 10").grid(row=2, column=6)
            tk.Label(ShowInfo_Window, text=value[SQL_EMAIL], fg="black", font="Arial 10").grid(row=2, column=8)


    def AddRemove(self, work):
        if work == "remove":
            cursor.execute("SELECT %s FROM SEC_USER WHERE %s='%s'" % (SQL_USERID, SQL_USERNAME, self.ConnectedListbox.get(self.ConnectedListbox.curselection())))
            result = cursor.fetchone()

            self.NotConnectedListbox.insert(END, self.ConnectedListbox.get(self.ConnectedListbox.curselection()))
            self.ConnectedListbox.delete(self.ConnectedListbox.curselection())

            cursor.execute("UPDATE SEC_USERPROFILE SET profileID = NULL WHERE userID = %s" % (result[SQL_USERID]))
        elif work == "add":
            cursor.execute("SELECT %s FROM SEC_USER WHERE %s='%s'" % (SQL_USERID, SQL_USERNAME, self.NotConnectedListbox.get(self.NotConnectedListbox.curselection())))
            result = cursor.fetchone()

            self.ConnectedListbox.insert(END, self.NotConnectedListbox.get(self.NotConnectedListbox.curselection()))
            self.NotConnectedListbox.delete(self.NotConnectedListbox.curselection())

            cursor.execute("UPDATE SEC_USERPROFILE SET profileID = %s WHERE userID = %s" % (self.ProfileID_TextBox.get(), result[SQL_USERID]))


    def FetchRow(self, event=None):
        if self.ProfileID_TextBox.get():
            try:
                int(self.ProfileID_TextBox.get())  # Checks if the user input is an integer
                try:
                    int(self.ProfileID_TextBox.get()) #Checks if the user input is an integer
                    SQL_RETURNID = "SELECT %s FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, SQL_PROFILEID, self.ProfileID_TextBox.get())
                    cursor.execute(SQL_RETURNID)
                    results = cursor.fetchone()
                    res = ",".join(("{} {}".format(*i) for i in results.items())) #Converts dictionary to string
                    del results
                    if self.ProfileID_TextBox.get() in res:
                        SQL_RETURNINFO = "SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEID, self.ProfileID_TextBox.get())
                        cursor.execute(SQL_RETURNINFO)
                        RETURNINFO_Results = cursor.fetchall()
                        #print(str(RETURNINFO_Results)) # DEBUG PURPOSES ONLY
                        for row in RETURNINFO_Results:
                            #Clear TextBoxes first
                            self.ProfileDescription_TextBox.delete(0, END)

                            #Then proceed to filling out the new user info
                            self.ProfileDescription_TextBox.insert(0,row[SQL_PROFILEDESCRIPTION])
                        self.GetData()
                except:
                    messagebox.showwarning("Flexbase", "Invalid input. Please make sure the value is correct.", parent=self.master)
            except:
                messagebox.showwarning("Flexbase", "You did not input a valid integer. Please make sure the value is correct.", parent=self.master)

        elif self.ProfileDescription_TextBox.get():
            try:
                SQL_RETURNDESC = "SELECT %s FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEDESCRIPTION, SQL_PROFILEDESCRIPTION, self.ProfileDescription_TextBox.get())
                cursor.execute(SQL_RETURNDESC)
                results = cursor.fetchone()
                res = ",".join(("{} {}".format(*i) for i in results.items()))  # Converts dictionary to string
                del results
                if self.ProfileDescription_TextBox.get() in res:
                    cursor.execute("SELECT * FROM SEC_PROFILE WHERE %s = '%s'" % (SQL_PROFILEDESCRIPTION, self.ProfileDescription_TextBox.get()))
                    RETURNINFO_Results = cursor.fetchall()
                    # print(str(RETURNINFO_Results)) # DEBUG PURPOSES ONLY
                    for row in RETURNINFO_Results:
                        # Clear TextBoxes first
                        self.ProfileID_TextBox.delete(0, END)

                        # Then proceed to filling out the new user info
                        self.ProfileID_TextBox.insert(0, row[SQL_PROFILEID])
                    self.GetData()
            except:
                messagebox.showwarning("Flexbase", "Invalid input. Please make sure the value is correct.", parent=self.master)


    def GetData(self):
        self.ConnectedList.clear()
        self.NotConnectedList.clear()
        self.ConnectedListbox.delete(0, END)
        self.NotConnectedListbox.delete(0, END)

        cursor.execute("SELECT * FROM SEC_USER INNER JOIN SEC_USERPROFILE ON SEC_USERPROFILE.%s=SEC_USER.%s WHERE SEC_USERPROFILE.%s = '%s'" % (SQL_UP_USERID, SQL_USERID, SQL_UP_PROFILEID, self.ProfileID_TextBox.get()))
        result = cursor.fetchall()
        for row in result:
            self.ConnectedList.append(row[SQL_USERNAME])

        cursor.execute("SELECT * FROM SEC_USER INNER JOIN SEC_USERPROFILE ON SEC_USERPROFILE.%s=SEC_USER.%s WHERE SEC_USERPROFILE.%s <> '%s' OR SEC_USERPROFILE.%s IS NULL" % (SQL_UP_USERID, SQL_USERID, SQL_UP_PROFILEID, self.ProfileID_TextBox.get(), SQL_UP_PROFILEID))
        result = cursor.fetchall()
        for row in result:
            self.NotConnectedList.append(row[SQL_USERNAME])

        for row in self.ConnectedList:
            self.ConnectedListbox.insert(END, row)

        for row in self.NotConnectedList:
            self.NotConnectedListbox.insert(END, row)


def main():
    root = tk.Tk()
    SecurityWindow_Class(root)
    root.mainloop()


if __name__ == '__main__':
    config = ConfigParser()
    if not path.isfile("configuration.ini"):
        messagebox.showwarning("Flexbase", "The configuration.ini file is missing. Creating a new one.")
        config.add_section('Database')
        config['Database']['Database_Domain'] = ""
        config['Database']['Database_Username'] = ""
        config['Database']['Database_Password'] = ""
        config['Database']['Database_Name'] = ""
        with open("configuration.ini", "w") as configfile:
            config.write(configfile)
        messagebox.showinfo("Flexbase", "configuration.ini file created. You will need to open Flexbase again after you populate the values in the configuration.ini file.")
        exit()
    else:
        config.read("configuration.ini")

    if not config.get('Database', 'Database_Domain'):  # If Database Domain is missing
        messagebox.showerror("Flexbase", "configuration.ini file is missing the value in key \"database_domain\" under the \"[Database]\" section. Please ensure all the values are populated.")
        exit()
    elif not config.get('Database', 'Database_Username'):  # If Database Username is missing
        messagebox.showerror("Flexbase", "configuration.ini file is missing the value in key \"database_username\" under the \"[Database]\" section. Please ensure all the values are populated.")
        exit()
    elif not config.get('Database', 'Database_Password'):  # If Database Password is missing
        messagebox.showerror("Flexbase", "configuration.ini file is missing the value in key \"database_password\" under the \"[Database]\" section. Please ensure all the values are populated.")
        exit()
    elif not config.get('Database', 'Database_Name'):  # If Database Name is missing
        messagebox.showerror("Flexbase", "configuration.ini file is missing the value in key \"database_name\" under the \"[Database]\" section. Please ensure all the values are populated.")
        exit()
    else:  # If nothing is missing
        try:
            db = pymysql.connect(config.get('Database', 'Database_Domain'),
                                 config.get('Database', 'Database_Username'),
                                 config.get('Database', 'Database_Password'),
                                 config.get('Database', 'Database_Name'), autocommit=True)
            cursor = db.cursor(pymysql.cursors.DictCursor)
        except:
            messagebox.showerror("Flexbase", "Could not connect to the database. Please make sure that all the values are correctly written and try again.")
            exit()

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + config.get('Database', 'Database_Name') + "' AND TABLE_NAME = 'SEC_USER';")
    columns = cursor.fetchall()
    columns_list = []
    for row in columns:
        for key in row:
            columns_list.append(row[key])
    SQL_USERID = columns_list[0]
    SQL_FIRSTNAME = columns_list[1]
    SQL_SURNAME = columns_list[2]
    SQL_USERNAME = columns_list[3]
    SQL_PASSWORD = columns_list[4]
    SQL_EMAIL = columns_list[5]
    del columns_list

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + config.get('Database', 'Database_Name') + "' AND TABLE_NAME = 'SEC_PROFILE';")
    columns = cursor.fetchall()
    columns_list2 = []
    for row in columns:
        for key in row:
            columns_list2.append(row[key])
    SQL_PROFILEID = columns_list2[0]
    SQL_PROFILECODE = columns_list2[1]
    SQL_PROFILEDESCRIPTION = columns_list2[2]
    del columns_list2

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + config.get('Database', 'Database_Name') + "' AND TABLE_NAME = 'SEC_USERPROFILE';")
    columns = cursor.fetchall()
    columns_list3 = []
    for row in columns:
        for key in row:
            columns_list3.append(row[key])
    SQL_USERPROFILEID = columns_list3[0]
    SQL_UP_USERID = columns_list3[1]
    SQL_UP_PROFILEID = columns_list3[2]
    del columns
    del columns_list3

    main()
