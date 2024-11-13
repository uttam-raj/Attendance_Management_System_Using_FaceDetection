from tkinter import*
from tkinter import ttk
from train import Train
from PIL import Image,ImageTk
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer 
import os
from helpsupport import Helpsupport

class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Face_Recogonition_System")
        self.root.state('zoomed')


# This part is image labels settingstart 
        # first header image  
        img=Image.open(r"Images_GUI\logbanner.jpg")
        img=img.resize((1366,140),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=100)

        # backgorund image 
        bg1=Image.open(r"Images_GUI\bg3.jpg")
        bg1=bg1.resize((1366,768),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=100,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="    Attendance Managment System Using Facial Recognition",font=("times new roman",35,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # student button 1
        std_img_btn=Image.open(r"Images_GUI\std1.jpg")
        std_img_btn=std_img_btn.resize((220,220),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.student_pannels,image=self.std_img1,cursor="hand2")
        std_b1.place(x=150,y=100,width=220,height=220)

        std_b1_1 = Button(bg_img,command=self.student_pannels,text="Student Details",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=150,y=300,width=220,height=40)

        # Detect Face  button 2
        det_img_btn=Image.open(r"Images_GUI\det1.jpg")
        det_img_btn=det_img_btn.resize((220,220),Image.LANCZOS)
        self.det_img1=ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img,command=self.face_rec,image=self.det_img1,cursor="hand2",)
        det_b1.place(x=450,y=100,width=220,height=220)

        det_b1_1 = Button(bg_img,command=self.face_rec,text="Face Detector",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        det_b1_1.place(x=450,y=300,width=220,height=40)

         # Attendance System  button 3
        att_img_btn=Image.open(r"Images_GUI\att.jpg")
        att_img_btn=att_img_btn.resize((220,220),Image.LANCZOS)
        self.att_img1=ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img,command=self.attendance_pannel,image=self.att_img1,cursor="hand2",)
        att_b1.place(x=750,y=100,width=220,height=220)

        att_b1_1 = Button(bg_img,command=self.attendance_pannel,text="Attendance",cursor="hand2",font=("times  new roman",15,"bold"),bg="white",fg="navyblue")
        att_b1_1.place(x=750,y=300,width=220,height=40)

         # Help  Support  button 4
        hlp_img_btn=Image.open(r"Images_GUI\hlp.jpg")
        hlp_img_btn=hlp_img_btn.resize((220,220),Image.LANCZOS)
        self.hlp_img1=ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img,command=self.helpSupport,image=self.hlp_img1,cursor="hand2",)
        hlp_b1.place(x=1050,y=100,width=220,height=220)

        hlp_b1_1 = Button(bg_img,command=self.helpSupport,text="Help Support",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        hlp_b1_1.place(x=1050,y=300,width=220,height=40)

        # Top 4 buttons end.......
        # ---------------------------------------------------------------------------------------------------------------------------
        # Start below buttons.........
         # Train   button 5
        tra_img_btn=Image.open(r"Images_GUI\tra1.jpg")
        tra_img_btn=tra_img_btn.resize((220,220),Image.LANCZOS)
        self.tra_img1=ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img,command=self.train_pannels,image=self.tra_img1,cursor="hand2",)
        tra_b1.place(x=150,y=350,width=220,height=220)

        tra_b1_1 = Button(bg_img,command=self.train_pannels,text="Data Train",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        tra_b1_1.place(x=150,y=550,width=220,height=40)

        # Photo   button 6
        pho_img_btn=Image.open(r"Images_GUI\sample.jpg")
        pho_img_btn=pho_img_btn.resize((220,220),Image.LANCZOS)
        self.pho_img1=ImageTk.PhotoImage(pho_img_btn)

        pho_b1 = Button(bg_img,command=self.open_img,image=self.pho_img1,cursor="hand2",)
        pho_b1.place(x=450,y=350,width=220,height=220)

        pho_b1_1 = Button(bg_img,command=self.open_img,text="Photos",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        pho_b1_1.place(x=450,y=550,width=220,height=40)

        # Developers   button 7
        dev_img_btn=Image.open(r"Images_GUI\dev.jpg")
        dev_img_btn=dev_img_btn.resize((220,220),Image.LANCZOS)
        self.dev_img1=ImageTk.PhotoImage(dev_img_btn)

        dev_b1 = Button(bg_img,command=self.developr,image=self.dev_img1,cursor="hand2",)
        dev_b1.place(x=750,y=350,width=220,height=220)

        dev_b1_1 = Button(bg_img,command=self.developr,text="Developers",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        dev_b1_1.place(x=750,y=550,width=220,height=40)  

        # exit   button 8
        exi_img_btn=Image.open(r"Images_GUI\exi.jpg")
        exi_img_btn=exi_img_btn.resize((220,220),Image.LANCZOS)
        self.exi_img1=ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img,command=self.Close,image=self.exi_img1,cursor="hand2",)
        exi_b1.place(x=1050,y=350,width=220,height=220)

        exi_b1_1 = Button(bg_img,command=self.Close,text="Exit",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="navyblue")
        exi_b1_1.place(x=1050,y=550,width=220,height=40)

# ==================Funtion for Open Images Folder==================
    def open_img(self):
        os.startfile("data_img")
# ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_pannels(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)
    
    def face_rec(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
        
    
    def attendance_pannel(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)
    
    def developr(self):
        self.new_window=Toplevel(self.root)
        self.app=Developer(self.new_window)
        # (open it for developer pannel) 
    
    def helpSupport(self):
        self.new_window=Toplevel(self.root)
        self.app=Helpsupport(self.new_window)

    def Close(self):
        root.destroy()
    

if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()