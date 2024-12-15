import cv2 as cv
import os
import pyautogui

def register():
 
    video = cv.VideoCapture(0)
    cv.namedWindow('Live')
    cv.setWindowProperty('Live', cv.WND_PROP_TOPMOST, 1)
    cv.resizeWindow('Live', 600, 400) 

   
    save_folder = "photos"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    print("Press 'c' to capture a photo, or 'q' to quit.")

    while True:
        istrue, frame = video.read()
        if istrue:
           
            cv.putText(frame, "Press 'c' to capture, 'q' to quit", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.imshow('Live', frame)
           
            window_x, window_y = pyautogui.getWindowsWithTitle('Live')[0].topleft
            window_center_x = window_x + 300  
            window_center_y = window_y + 200 
        
       
            pyautogui.click(window_center_x, window_center_y)
            key = cv.waitKey(1) & 0xFF

            if key == ord('q'):  
                print("Exiting...")
                break
            elif key == ord('c'):  
                cv.destroyAllWindows()
                name = input("Enter the name for the photo: ")
                img_path = os.path.join(save_folder, name + '.jpg')
                cv.imwrite(img_path, frame)
                print(f"Photo saved at: {img_path}")
                cv.destroyAllWindows()
                break

   
    video.release()
    cv.destroyAllWindows()
