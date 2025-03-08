import os
import time
import cv2 as cv
import numpy as np
import mysql.connector
import datetime

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="attendence_database"
)
cursor = connection.cursor()

# Function to check if ID belongs to faculty
def is_faculty(person_id):
    cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s", (person_id,))
    return cursor.fetchone() is not None

# Function to get current slot based on time
# Function to get current slot based on time and faculty allocation
def get_current_slot(faculty_id):
    try:
        current_time = datetime.datetime.now().time()
        cursor.execute("""
            SELECT s.slot_name, s.time_range 
            FROM allocation a 
            JOIN slot s ON a.slot = s.slot_name 
            WHERE a.faculty_id = %s
        """, (faculty_id,))
        
        slots = cursor.fetchall()
        print(f"Fetched slots: {slots}")
        
        for slot_name, time_range in slots:
            start_str, end_str = time_range.strip().split(' - ')
            start_time = datetime.datetime.strptime(start_str, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_str, '%H:%M').time()
            
            if start_time <= current_time <= end_time:
                print(f"Current slot: {slot_name}")
                return slot_name
        print("No active slot at this time.")
        return None
        
    except Exception as e:
        print(f"Error fetching current slot: {e}")
        return None

# Function to update attendance status
# Function to update attendance status
def update_student_attendance(student_id, current_slot, faculty_id):
    try:
        table_name = f"{current_slot.lower()}_{faculty_id}"
        print(f"Checking table: {table_name}")
        
        # Check if the table exists
        cursor.execute("""
            SELECT table_name 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE table_schema = 'attendence_database' AND table_name = %s
        """, (table_name,))
        
        if not cursor.fetchone():
            print(f"Table {table_name} does not exist.")
            return
        
        # Update attendance (correct column name)
        cursor.execute(f"""
            UPDATE {table_name} 
            SET status = 'p' 
            WHERE student_id = %s
        """, (student_id,))
        connection.commit()
        print(f"Updated attendance for student {student_id} in {table_name}")
    except Exception as e:
        print(f"Error updating attendance: {e}")
        connection.rollback()

# Function to load and train face recognizer
def train_recognizer(photos_dir='photos', trainer_file='trainer.yml'):
    images, labels = [], []
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if not os.path.exists(photos_dir) or not os.listdir(photos_dir):
        print("No photos found in 'photos' directory.")
        return None
    
    for filename in os.listdir(photos_dir):
        img_path = os.path.join(photos_dir, filename)
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        if img is None: continue
        person_id = os.path.splitext(filename)[0]
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.8, minNeighbors=3)
        for (x, y, w, h) in faces:
            images.append(img[y:y+h, x:x+w])
            labels.append(int(person_id))
    
    if not images:
        print("No faces detected for training.")
        return None
    
    recognizer = cv.face.LBPHFaceRecognizer_create()
    if os.path.exists(trainer_file):
        recognizer.read(trainer_file)
    else:
        recognizer.train(images, np.array(labels))
        recognizer.save(trainer_file)
    
    return recognizer

# Main attendance function
def take_attendance():
    recognizer = train_recognizer()
    if not recognizer: return

    video = cv.VideoCapture(0)
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faculty_punched_in = False
    faculty_id, current_slot = None, None
    present = set()
    
    print("Press space bar to exit")
    while True:
        ret, frame = video.read()
        if not ret: break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
        
        for (x, y, w, h) in faces:
            if x+h > 150 and w+y > 150:
                face_roi = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(face_roi)
                
                if confidence < 85:
                    person_id = str(label)
                    if not faculty_punched_in and is_faculty(person_id):
                        faculty_id = int(person_id)
                        current_slot = get_current_slot(faculty_id)
                        faculty_punched_in = bool(current_slot)
                        text = f"Faculty {faculty_id} ({current_slot}) punched in" if current_slot else f"No current slot for {faculty_id}"
                    elif faculty_punched_in and person_id.isdigit():
                        present.add(int(person_id))
                        text = f"Student {person_id} marked present"
                    else:
                        text = f"Waiting for faculty punch-in {person_id}"
                else:
                    text = "Unknown face detected"
                
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv.putText(frame, text, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv.imshow('Attendance System', frame)
        if cv.waitKey(1) & 0xFF == ord(' '): break

    video.release()
    cv.destroyAllWindows()

    if faculty_punched_in and current_slot:
        for student_id in present:
            update_student_attendance(student_id, current_slot, faculty_id)
        print(f"Attendance updated for {len(present)} students.")
    else:
        print("No attendance data to update.")

    connection.close()
