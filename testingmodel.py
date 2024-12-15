import os
import cv2 as cv
import numpy as np
import pandas as pd
import pyautogui

def take_attendance():
    photos = r'photos'
    print("press space bar to exit")
    images = []
    gray_images = []
    labels = []
    names = []
    present = []
    count = 0
    
   
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    for i in os.listdir(photos):
        img_path = os.path.join(photos, i)
        img = cv.imread(img_path)
        if img is None:
            continue
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            images.append(face)
            gray_images.append(face)
            labels.append(count)
            names.append(os.path.splitext(i)[0])
            count += 1
    
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.train(gray_images, np.asarray(labels))
    recognizer.save("trainer.yml")
    
    video = cv.VideoCapture(0)
    cv.namedWindow('Live') 
    cv.setWindowProperty('Live', cv.WND_PROP_TOPMOST, 1)

    while True:
        istrue, frame = video.read()
        if not istrue:
            break
        
       
       
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        for (x, y, w, h) in faces:
           
    
            
            if w > 100 and h > 100:
               
                face_roi = gray[y:y+h,x:x+w]
                label, confidence = recognizer.predict(face_roi)
                
                name = names[label]
                if name not in present:
                    present.append(name)
                
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv.putText(frame, f'Name: {name} marked present', (x, y - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        
      
        window_x, window_y = pyautogui.getWindowsWithTitle('Live')[0].topleft
        window_center_x = window_x + 300  
        window_center_y = window_y + 200 
        
       
        pyautogui.click(window_center_x, window_center_y)
        
        cv.imshow('Live', frame)
        
        if cv.waitKey(1) & 0xFF == ord(' '):
            break
    
    video.release()
    cv.destroyAllWindows()
    
    df = pd.DataFrame({'Index': range(1, len(present) + 1), 'Name': present})
    df.to_excel('attendance_list.xlsx', index=False)
    
    print("Attendance list created successfully!")

