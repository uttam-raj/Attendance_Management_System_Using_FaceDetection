from tkinter import*
from tkinter import ttk
from train import Train
from PIL import Image,ImageTk
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
import os

class Developer:
    def __init__(self,root):
        self.root=root
        self.root.title("Face_Recogonition_System")
        self.root.state('zoomed')

# This part is image labels setting start 
        # first header image  
        img=Image.open(r"Images_GUI\logbanner.jpg")
        img=img.resize((1366,130),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r"Images_GUI\bg4.png")
        bg1=bg1.resize((1366,768),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)

        back_btn = Button(self.root, text="Back", command=self.back_function, width=8, font=("times new roman", 13, "bold"), fg="white", bg="red")
        back_btn.place(x=1265, y=1,height=40)

        #title section
        title_lb1 = Label(bg_img,text="Developer Pannel",font=("times new roman",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # student button 1
        std_img_btn=Image.open(r"Images_GUI\v.jpeg")
        std_img_btn=std_img_btn.resize((280,250),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,image=self.std_img1,cursor="hand2")
        std_b1.place(x=100,y=200,width=200,height=200)

        std_b1_1 = Button(bg_img,text="MD IRFAN ANSARI \n Branch: CSE",cursor="hand2",font=("times new roman",13,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=100,y=380,width=200,height=70)

        # Detect Face  button 2
        det_img_btn=Image.open(r"Images_GUI\v.jpeg")
        det_img_btn=det_img_btn.resize((250,220),Image.LANCZOS)
        self.det_img1=ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img,image=self.det_img1,cursor="hand2",)
        det_b1.place(x=330,y=200,width=200,height=200)

        det_b1_1 = Button(bg_img,text="NILESH KR. UPADHYAY \n Branch: CSE",cursor="hand2",font=("times new roman",13,"bold"),bg="white",fg="navyblue")
        det_b1_1.place(x=330,y=380,width=200,height=70)

         # Attendance System  button 3
        att_img_btn=Image.open(r"Images_GUI\v.jpeg")
        att_img_btn=att_img_btn.resize((250,250),Image.LANCZOS)
        self.att_img1=ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img,image=self.att_img1,cursor="hand2",)
        att_b1.place(x=560,y=200,width=200,height=200)

        att_b1_1 = Button(bg_img,text="UTTAM KUMAR RAJWAR\n Branch: CSE",cursor="hand2",font=("times new roman",13,"bold"),bg="white",fg="navyblue")
        att_b1_1.place(x=560,y=380,width=200,height=70)

         # Help  Support  button 4
        hlp_img_bt=Image.open(r"Images_GUI\vishal.jpeg")
        hlp_img_bt=hlp_img_bt.resize((250,250),Image.LANCZOS)
        self.hlp_img=ImageTk.PhotoImage(hlp_img_bt)

        hlp_b = Button(bg_img,image=self.hlp_img,cursor="hand2",)
        hlp_b.place(x=790,y=200,width=200,height=200)

        hlp_b_1 = Button(bg_img,text="VISHAL KUMAR \n Branch: CSE",cursor="hand2",font=("times new roman",13,"bold"),bg="white",fg="navyblue")
        hlp_b_1.place(x=790,y=380,width=200,height=70)
        
        hlp_img_btn=Image.open(r"Images_GUI\abj.jpeg")
        hlp_img_btn=hlp_img_btn.resize((250,230),Image.LANCZOS)
        self.hlp_img1=ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img,image=self.hlp_img1,cursor="hand2",)
        hlp_b1.place(x=1020,y=200,width=200,height=200)

        hlp_b1_1 = Button(bg_img,text="ABHIJEET KR. MISHRA \n Branch: CSE",cursor="hand2",font=("times new roman",13,"bold"),bg="white",fg="navyblue")
        hlp_b1_1.place(x=1020,y=380,width=200,height=70)


    def back_function(self):
        self.root.destroy() 

if __name__ == "__main__":
    root=Tk()
    obj=Developer(root)
    root.mainloop()