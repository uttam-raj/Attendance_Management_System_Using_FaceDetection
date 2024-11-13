# LBPH (Local Binary  patterns Histogram)
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
import time
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance as dist
import smtplib
import ssl
from email.message import EmailMessage
from apscheduler.schedulers.background import BackgroundScheduler

class Face_Recognition:

    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Panel")
        root.state('zoomed')

        # This part is image labels setting start
        img = Image.open(r"Images_GUI\logbanner.jpg")
        img = img.resize((1366, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        bg1 = Image.open(r"Images_GUI\bg2.jpg")
        bg1 = bg1.resize((1366, 768), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)
        
        self.entry_count = 0
        self.exit_count = 0

        title_lb1 = Label(bg_img, text="Welcome to Face Recognition Panel", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)


        std_img_btn = Image.open(r"Images_GUI\f_det.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.face_recog, image=self.std_img1, cursor="hand2")
        std_b1.place(x=600, y=170, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.face_recog, text="Face Detector", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=600, y=350, width=180, height=45)

        # Schedule daily check for absentees
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.check_absentees, 'cron', hour=16, minute=00)  # Run at 16:00 (4:00 PM)
        self.scheduler.start()
    
    def check_absentees(self):
        conn = mysql.connector.connect(username='root', password='', host='localhost', database='face_recognition')
        cursor = conn.cursor()

        today_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch all students
        cursor.execute("SELECT Student_ID, Name, Email FROM student")
        students = cursor.fetchall()

        # Fetch students who have marked attendance today
        cursor.execute("SELECT std_id FROM stdattendance WHERE std_date = %s", (today_date,))
        present_students = cursor.fetchall()
        present_student_ids = {student[0] for student in present_students}
        
        hod_email= 'uttamrajwar.92@gmail.com'

        # Identify and send emails to absent students
        for student in students:
            if len(student) == 8:  # Ensure the row has 4 columns
                student_id, name, email, roll_no = student
                if student_id not in present_student_ids:
                    subject = "Absent Attendance Notification"
                    body = f"Dear {name},\n\nYou were marked as absent for today's class.\n\nRegards,\nYour College"
                    
                    hod_subject = "Student Absent Notification"
                    hod_body = f"Dear HOD,\n\nThe following student was absent today:\n\nName: {name}\nEmail: {email}\n\nRegards,\nAttendance System"
                    
                    self.send_email(email, subject, body)
                    self.send_email_to_hod(hod_email, hod_subject, hod_body)
                    print(f"Absent email sent to {name} ({email})")

                    # Update the attendance table to mark the student as absent
                    cursor.execute("INSERT INTO stdattendance (std_id, std_name, std_email, std_roll_no, std_date, std_attendance) VALUES (%s, %s, %s, %s, %s, %s)",
                                   (student_id, name, email, roll_no, today_date, "Absent"))
                    conn.commit()

        conn.close()    
    
    
    def mark_attendance_entry(self, id, roll_no, name, email):
        conn = mysql.connector.connect(username='root', password='', host='localhost', database='face_recognition')
        cursor = conn.cursor()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        fixed_entry_time = '07:40:00'
        
        cursor.execute("SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s", (id, date))
        result = cursor.fetchone()
        
        hod_email= 'uttamrajwar.92@gmail.com'

        if result:
            attend_time_str = result[5]  # Ensure the correct index for the time column
            if attend_time_str is not None:  # Add a check for None
                try:
                    attend_time = datetime.strptime(attend_time_str, '%H:%M:%S').time()
        
                    if attend_time > datetime.strptime(fixed_entry_time, '%H:%M:%S').time() and result[7] != "Late":  # Ensure the correct index for 'Late' status
                        late_duration_seconds = (datetime.combine(datetime.today(), attend_time) - datetime.combine(datetime.today(),datetime.strptime(fixed_entry_time, '%H:%M:%S').time())).seconds
                        late_duration = time.gmtime(late_duration_seconds)
                        late_duration_str = f"{late_duration.tm_hour:02}:{late_duration.tm_min:02}:{late_duration.tm_sec:02}"
                        cursor.execute("UPDATE stdattendance SET std_attendance=%s, std_late_time=%s WHERE std_id=%s AND std_date=%s", ("Late", late_duration_str, id, date))
                        conn.commit()
                        
                        # Send email notification
                        subject = "Late Attendance Notification"
                        body = f"Dear {name},\n\nYou were marked as late for today class. You arrived {late_duration_str} late.\n\nRegards,\nYour Class"
                        
                        hod_subject = "Student Late Arrival Notification"
                        hod_body = f"Dear HOD,\n\nThe following student arrived late today:\n\nName: {name}\nEmail: {email}\nLate by: {late_duration_str}\n\nRegards,\nAttendance System"

                        self.send_email(email, subject, body)
                        self.send_email_to_hod(hod_email, hod_subject, hod_body)
                        
                    else:
                        subject = "Present Attendance Notification"
                        body = f"Dear {name},\n\nYou were marked as Present for today's class.\n\nRegards,\nYour Class"
                        self.send_email(email, subject, body)
                except ValueError as ve:
                    print(f"Error parsing time: {ve}")
        else:
            cursor.execute("INSERT INTO stdattendance (std_id, std_name, std_email, std_roll_no, std_date, std_entry_time, std_attendance) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, name, email, roll_no, date, current_time, "Present"))
            conn.commit()
            
            self.entry_count += 1
        conn.close()
        

    def mark_attendance_exit(self, id, roll_no ,name, email):
        conn = mysql.connector.connect(username='root', password='', host='localhost', database='face_recognition')
        cursor = conn.cursor()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        fixed_exit_time= '16:00:00'

        cursor.execute("SELECT * FROM exitattendance WHERE std_id=%s AND std_date=%s",(id,date))
        result=cursor.fetchone()
        
        hod_email= 'uttamrajwar.92@gmail.com'
        
        if result:
            attend_time_str = result[5]  # Ensure the correct index for the time column
            if attend_time_str is not None:  # Add a check for None
                try:
                    attend_time = datetime.strptime(attend_time_str, '%H:%M:%S').time()
                    
                    if attend_time < datetime.strptime(fixed_exit_time, '%H:%M:%S').time() and result[7] != "early":  # Ensure the correct index for 'Late' status
                        early_duration_seconds = (datetime.combine(datetime.today(), datetime.strptime(fixed_exit_time, '%H:%M:%S').time()) - datetime.combine(datetime.today(), attend_time)).seconds
                        early_duration = time.gmtime(early_duration_seconds)
                        early_duration_str = f"{early_duration.tm_hour:02}:{early_duration.tm_min:02}:{early_duration.tm_sec:02}"
                        cursor.execute("UPDATE exitattendance SET std_attendance=%s, std_early_time=%s WHERE std_id=%s AND std_date=%s", ("Early", early_duration_str, id, date))
                        conn.commit()
                        
                        subject = "Early Exit Notification"
                        body = f"Dear {name},\n\nYou exited the class {early_duration_str} early today.\n\nRegards,\nYour Class"
                        
                        hod_subject = "Student Early Exit Notification"
                        hod_body = f"Dear HOD,\n\nThe following student exited early today:\n\nName: {name}\nEmail: {email}\nEarly exit by: {early_duration_str}\n\nRegards,\nAttendance System"

                        self.send_email(email, subject, body)
                        self.send_email_to_hod(hod_email, hod_subject, hod_body)
                except ValueError as ve:
                    print(f"Error parsing time: {ve}")

        else:
            cursor.execute("INSERT INTO exitattendance (std_id, std_name, std_email, std_roll_no, std_date, std_exit_time,  std_attendance) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, name, email,roll_no,date, current_time,"Right Time"))
            conn.commit()  
            self.exit_count += 1  
        conn.close()

    def send_email(self, recipient, subject, body):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        email_from = 'uttamkumarrajwar13@gmail.com'
        email_password = 'buzk rrra fnis tojn'  # Replace with your App Password
        
        msg = EmailMessage()
        msg['From'] = email_from
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(email_from, email_password)
            server.send_message(msg)
            print(f"Email sent successfully to {recipient}")
            
    def send_email_to_hod(self, hod_email, subject, body):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        email_from = 'uttamkumarrajwar13@gmail.com'
        email_password = 'buzk rrra fnis tojn'  # Replace with your App Password

        msg = EmailMessage()
        msg['From'] = email_from
        msg['To'] = hod_email
        msg['Subject'] = subject
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(email_from, email_password)
            server.send_message(msg)
            print(f"Email sent successfully to HOD {hod_email}")


    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(username='root', password='', host='localhost', database='face_recognition')
                cursor = conn.cursor()

                cursor.execute("SELECT Student_ID, Roll_No, Name, Email FROM student WHERE Student_ID=%s", (id,))
                result = cursor.fetchone()
                conn.close()

                if result is not None:
                    student_id, roll_no, name, email = result
                else:
                    student_id, name, roll_no, email = 0, "Unknown", "Unknown", "Unknown"

                if confidence > 80:
                    
                        # self.mark_attendance_entry(student_id, roll_no, name, email)
                    cv2.putText(img, f"ID: {student_id}", (x, y - 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    cv2.putText(img, f"Roll: {roll_no}", (x, y - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    cv2.putText(img, f"Name: {name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    # Determine the position of the face relative to the boundary
                    face_center_x = x + w // 2
                    boundary_x = img.shape[1] // 2  # Assuming the center of the frame is the boundary
                    is_entry = face_center_x < boundary_x

                    # Mark attendance based on position
                    if is_entry:
                        self.mark_attendance_entry(student_id, roll_no, name, email)
                            
                    else:
                            self.mark_attendance_exit(student_id, roll_no ,name, email)
                            
                else:
                    student_id = "Unknown"
                    name = "Unknown"
                    roll_no = "Unknown"
                    email = "Unknown"   
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    # Determine the position of the face relative to the boundary
                    face_center_x = x + w // 2
                    boundary_x = img.shape[1] // 2  # Assuming the center of the frame is the boundary
                    is_entry = face_center_x < boundary_x
                    # Increment count for unknown faces based on position
                    if is_entry:
                        self.entry_count += 1
                    else:
                        self.exit_count += 1



                coord = [x, y, w, h]

            return coord

        def eye_aspect_ratio(eye):
            A = dist.euclidean(eye[1], eye[5])
            B = dist.euclidean(eye[2], eye[4])
            C = dist.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear

        def recognize(img, clf, faceCascade):
            # Calculate the center of the frame
            center_x = img.shape[1] // 2

            # Draw a vertical line at the center of the frame
            cv2.line(img, (center_x, 0), (center_x, img.shape[0]), (0, 255, 0), 2)

            # Add text annotations for Entry and Exit
            entry_text = "Entry"
            exit_text = "Exit"

            # Define text properties
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_color = (255,0,0)
            text_offset = 50  # Offset from the top of the frame for text placement

            # Calculate text size for Entry
            entry_text_size = cv2.getTextSize(entry_text, font, font_scale, font_thickness)[0]

            # Calculate text position for Entry (left side)
            entry_text_position = (center_x - entry_text_size[0] - 550, text_offset)
            
            # Calculate text position for Exit (right side)
            exit_text_position = (center_x + 400, text_offset)

            # Draw text annotations on the image
            cv2.putText(img, entry_text, entry_text_position, font, font_scale, text_color, font_thickness)
            cv2.putText(img, f"Entry Count: {self.entry_count}", (entry_text_position[0], entry_text_position[1] + 30), font, font_scale, text_color, font_thickness)

            cv2.putText(img, exit_text, exit_text_position, font, font_scale, text_color, font_thickness)
            cv2.putText(img, f"Exit Count: {self.exit_count}", (exit_text_position[0], exit_text_position[1] + 30), font, font_scale, text_color, font_thickness)
            
            # Draw total count
            total_count = self.entry_count - self.exit_count
            cv2.putText(img, f"Total Count: {total_count}", (img.shape[1] // 2 + 400, img.shape[0] - 30), font, font_scale, text_color, font_thickness)
            # Draw boundaries around faces
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            # Convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale image
            rects = detector(gray, 0)

            # Loop over the face detections
            for rect in rects:
                # Determine the facial landmarks for the face region
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # Extract the left and right eye coordinates
                left_eye = shape[36:42]
                right_eye = shape[42:48]

                # Calculate the eye aspect ratio for both eyes
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                # Calculate the average eye aspect ratio
                avg_ear = (left_ear + right_ear) / 2.0

                # Check if the eyes are closed (blink detected)
                if avg_ear < 0.25:  # Adjust this threshold as needed
                     print("Blink detected!")
    
                # Draw the eye regions on the image
                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)
                cv2.drawContours(img, [left_eye_hull], -1, (0, 255, 0), 1)
                cv2.drawContours(img, [right_eye_hull], -1, (0, 255, 0), 1)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("clf.xml")
        
        video_cap = cv2.VideoCapture(0)
        
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf,faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)
            if cv2.waitKey(1) == 13:
                break
            
        video_cap.release()
        cv2.destroyAllWindows()


if __name__== "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()