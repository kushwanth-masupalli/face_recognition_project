import cv2 as cv
import os

def register():
    video = cv.VideoCapture(0)
    
    if not video.isOpened():
        print("Error: Cannot access the webcam.")
        return

    cv.namedWindow('Live')
    cv.setWindowProperty('Live', cv.WND_PROP_TOPMOST, 1)
    cv.resizeWindow('Live', 600, 400) 

    save_folder = "photos"
    os.makedirs(save_folder, exist_ok=True)

    print("Press 'c' to capture a photo, or 'q' to quit.")
    while True:
        istrue, frame = video.read()
        if istrue:
            cv.putText(frame, "Press 'c' to capture, 'q' to quit", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.imshow('Live', frame)

            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                video.release()
                cv.destroyAllWindows()
                print("Exiting...")
                break
            elif key == ord('c'):
                video.release()
                cv.destroyAllWindows()
                name = input("Enter unique id number: ")
                img_path = os.path.join(save_folder, name + '.jpg')
                cv.imwrite(img_path, frame)
                print(f"Photo saved at: {img_path}")
                break

    
