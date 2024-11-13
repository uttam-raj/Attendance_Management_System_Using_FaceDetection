import re
import os
import csv
import cv2
import numpy as np
from time import strftime
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector

# Global variable for importCsv Function 
mydata = []

class Attendance:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Panel")
        self.root.state('zoomed')

        # Variables
        self.var_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attend = StringVar()

        # Header image
        img = Image.open(r"Images_GUI/logbanner.jpg")
        img = img.resize((1366, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image
        bg1 = Image.open(r"Images_GUI/bg2.jpg")
        bg1 = bg1.resize((1366, 768), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Back button
        back_btn = Button(self.root, text="Back", command=self.back_function, width=8, font=("times new roman", 13, "bold"), fg="white", bg="red")
        back_btn.place(x=1265, y=1, height=40)

        # Title section
        title_lb1 = Label(bg_img, text="Welcome to Attendance Panel", font=("times new roman", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Right section
        right_frame = LabelFrame(bg_img, bd=2, bg="white", relief=RIDGE, text="Student Details", font=("times new roman", 12, "bold"), fg="navyblue")
        right_frame.place(x=10, y=55, width=1346, height=700)
        
        # search_label = Label(right_frame, text="Search By Name:", font=("times new roman", 12, "bold"), bg="white", fg="navyblue")
        # search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        # search_entry = Entry(right_frame, textvariable=self.search_data, font=("times new roman", 12, "bold"), width=20)
        # search_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        # search_btn = Button(right_frame, command=self.search_data, text="Search", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        # search_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        # Bottom Left Frame
        table_frame_left = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Entry", font=("times new roman", 12, "bold"), fg="navyblue")
        table_frame_left.place(x=10, y=50, width=650, height=425)

        # Scrollbars for Bottom Left Table
        scroll_x_left = ttk.Scrollbar(table_frame_left, orient=HORIZONTAL)
        scroll_y_left = ttk.Scrollbar(table_frame_left, orient=VERTICAL)

        self.leftReport = ttk.Treeview(table_frame_left, column=("ID","Roll_No" ,"Name", "Email","Date" ,"Entry_Time", "Late_Time", "Attend"), xscrollcommand=scroll_x_left.set, yscrollcommand=scroll_y_left.set)

        scroll_x_left.pack(side=BOTTOM, fill=X)
        scroll_y_left.pack(side=RIGHT, fill=Y)
        scroll_x_left.config(command=self.leftReport.xview)
        scroll_y_left.config(command=self.leftReport.yview)

        self.leftReport.heading("ID", text="ID")
        self.leftReport.heading("Roll_No", text="Roll_No")
        self.leftReport.heading("Name", text="Name")
        self.leftReport.heading("Email", text="Email")
        self.leftReport.heading("Date", text="Date")
        # self.leftReport.heading("Time", text="Time")
        self.leftReport.heading("Entry_Time", text="Entry Time")
        self.leftReport.heading("Late_Time", text="Late Time")
        self.leftReport.heading("Attend", text="Status")
        self.leftReport["show"] = "headings"

        # Set Width of Columns 
        self.leftReport.column("ID", width=100)
        self.leftReport.column("Roll_No", width=100)
        self.leftReport.column("Name", width=100)
        self.leftReport.column("Email", width=100)
        self.leftReport.column("Date", width=100)
        # self.leftReport.column("Time", width=100)
        self.leftReport.column("Entry_Time", width=100)
        self.leftReport.column("Late_Time", width=100)
        self.leftReport.column("Attend", width=100)
        
        self.leftReport.pack(fill=BOTH, expand=1)
        self.leftReport.bind("<ButtonRelease>", self.get_cursor_left)
        self.fetch_data_left()
        
        # Bottom Right Frame
        table_frame_right = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Exit", font=("times new roman", 12, "bold"), fg="navyblue")
        table_frame_right.place(x=680, y=50, width=650, height=425)

        # Scrollbars for Bottom Right Table
        scroll_x_right = ttk.Scrollbar(table_frame_right, orient=HORIZONTAL)
        scroll_y_right = ttk.Scrollbar(table_frame_right, orient=VERTICAL)

        self.rightReport = ttk.Treeview(table_frame_right, column=("ID","Roll_No", "Name", "Email","Date" ,"Exit_Time", "Early_Time", "Attend"), xscrollcommand=scroll_x_right.set, yscrollcommand=scroll_y_right.set)

        scroll_x_right.pack(side=BOTTOM, fill=X)
        scroll_y_right.pack(side=RIGHT, fill=Y)
        scroll_x_right.config(command=self.rightReport.xview)
        scroll_y_right.config(command=self.rightReport.yview)

        self.rightReport.heading("ID", text="ID")
        self.rightReport.heading("Roll_No", text="Roll_No")
        self.rightReport.heading("Name", text="Name")
        self.rightReport.heading("Email", text="Email")
        self.rightReport.heading("Date", text="Date")
        # self.rightReport.heading("Time", text="Time")
        self.rightReport.heading("Exit_Time", text="Exit Time")
        self.rightReport.heading("Early_Time", text="Early Time")
        self.rightReport.heading("Attend", text="Status")
        self.rightReport["show"] = "headings"

        # Set Width of Columns 
        self.rightReport.column("ID", width=100)
        self.rightReport.column("Name", width=100)
        self.rightReport.column("Roll_No", width=100)
        self.rightReport.column("Email", width=100)
        self.rightReport.column("Date", width=100)
        # self.rightReport.column("Time", width=100)
        self.rightReport.column("Exit_Time", width=100)
        self.rightReport.column("Early_Time", width=100)
        self.rightReport.column("Attend", width=100)
        
        self.rightReport.pack(fill=BOTH, expand=1)
        self.rightReport.bind("<ButtonRelease>", self.get_cursor_right)
        
        self.fetch_data_right()

        # Buttons
        update_btn = Button(right_frame, command=self.update_data, text="Update", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        update_btn.grid(row=0, column=1, padx=6, pady=10, sticky=W)
        delete_btn = Button(right_frame, command=self.delete_data, text="Delete", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        delete_btn.grid(row=0, column=2, padx=6, pady=10, sticky=W)
        reset_btn = Button(right_frame, command=self.reset_data, text="Reset", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        reset_btn.grid(row=0, column=3, padx=6, pady=10, sticky=W)
        import_btn = Button(right_frame, command=self.importCsv, text="Import CSV", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        import_btn.grid(row=0, column=4, padx=6, pady=10, sticky=W)
        export_btn = Button(right_frame, command=self.exportCsv, text="Export CSV", width=12, font=("times new roman", 12, "bold"), fg="white", bg="navyblue")
        export_btn.grid(row=0, column=5, padx=6, pady=10, sticky=W)
        self.var_search=StringVar()
        search_btn=Button(right_frame,command=self.search_data,text="Search",width=12,font=("times new roman",12,"bold"),fg="white",bg="navyblue")
        search_btn.grid(row=0,column=8,padx=5,pady=10,sticky=W)
        search_entry = ttk.Entry(right_frame,textvariable=self.var_search,width=20,font=("times new roman",15,"bold"))
        search_entry.grid(row=0,column=9,padx=5,pady=10,sticky=W)
    def update_data(self):
        if self.var_id.get() == "" or self.var_roll.get() == "" or self.var_name.get() == "" or self.var_time.get() == "" or self.var_date.get() == "" or self.var_attend.get() == "Status":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='face_recognition')
                mycursor = conn.cursor()
                mycursor.execute("UPDATE stdattendance SET std_roll_no=%s, std_name=%s, std_entry_time=%s, std_date=%s, std_attendance=%s WHERE std_id=%s", ( 
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attend.get(),
                    self.var_id.get()  
                ))
                conn.commit()
                self.fetch_data_left()
                conn.close()
                messagebox.showinfo("Success", "Successfully Updated!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Student Id Must be Required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='face_recognition')
                mycursor = conn.cursor()
                
                # Check which frame the selected data belongs to
                cursor_focus_left = self.leftReport.focus()
                content_left = self.leftReport.item(cursor_focus_left)
                data_left = content_left["values"]
                
                cursor_focus_right = self.rightReport.focus()
                content_right = self.rightReport.item(cursor_focus_right)
                data_right = content_right["values"]
                
                if len(data_left) > 0:
                    # Delete from stdattendance table
                    mycursor.execute("DELETE FROM stdattendance WHERE std_id=%s", (self.var_id.get(),))
                    self.fetch_data_left()
                elif len(data_right) > 0:
                    # Delete from exitattendance table
                    mycursor.execute("DELETE FROM exitattendance WHERE std_id=%s", (self.var_id.get(),))
                    self.fetch_data_right()
                else:
                    messagebox.showerror("Error", "No data selected!", parent=self.root)
                    
                conn.commit()
                conn.close()
                messagebox.showinfo("Delete", "Successfully Deleted!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def fetch_data_left(self):
        
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='face_recognition')
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM stdattendance")
        data = mycursor.fetchall()
        if len(data) != 0:
            self.leftReport.delete(*self.leftReport.get_children())
            for row in data:
                self.leftReport.insert("", END, values=row)
            conn.commit()
        conn.close()
        
    def fetch_data_right(self):
        
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='face_recognition')
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM exitattendance")
        data = mycursor.fetchall()
        if len(data) != 0:
            self.rightReport.delete(*self.rightReport.get_children())
            for row in data:
                self.rightReport.insert("", END, values=row)
            conn.commit()
        conn.close()

    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")

    def importCsv(self):
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for row in csvread:
                mydata.append(row)
        self.fetch_data_right(mydata)
        self.fetch_data_right(mydata)

    def fetchData(self, rows):
        self.attendanceReport.delete(*self.attendanceReport.get_children())
        for row in rows:
            self.attendanceReport.insert("", END, values=row)

    def exportCsv(self):
        try:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='face_recognition')
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM stdattendance")
            data = mycursor.fetchall()
            conn.close()

            if len(data) < 1:
                messagebox.showerror("Error", "No Data Found!", parent=self.root)
                return False

            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
            with open(fln, mode="w", newline="") as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                for row in data:
                    exp_write.writerow(row)
                messagebox.showinfo("Success", "Export Data Successfully!")
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def get_cursor_right(self, event=""):
        cursor_focus = self.rightReport.focus()
        content = self.rightReport.item(cursor_focus)
        data = content["values"]
        if len(data) > 0:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            self.var_attend.set(data[5])  
        else:
            self.reset_data()
            
    def get_cursor_left(self, event=""):
        cursor_focus = self.leftReport.focus()
        content = self.leftReport.item(cursor_focus)
        data = content["values"]
        if len(data) > 0:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            self.var_attend.set(data[5])  
        else:
            self.reset_data()
    
    def search_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
        my_cursor = conn.cursor()
        # Search in stdattendance table
        my_cursor.execute("SELECT * FROM stdattendance WHERE std_name LIKE '%" + str(self.var_search.get()) + "%'")
        rows_std = my_cursor.fetchall()
        # Search in exitattendance table
        my_cursor.execute("SELECT * FROM exitattendance WHERE std_name LIKE '%" + str(self.var_search.get()) + "%'")
        rows_exit = my_cursor.fetchall()

        # Combine the results from both tables
        rows = rows_std + rows_exit
        
        if len(rows) != 0:
            self.leftReport.delete(*self.leftReport.get_children())
            for i in rows:
                self.leftReport.insert("", END, values=i)
            conn.commit()
        conn.close()

            
    def back_function(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
