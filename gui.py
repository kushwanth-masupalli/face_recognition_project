import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from register import register
from take_attendence import take_attendance

# Hover effect functions
def on_enter(event, button, hover_color):
    button.config(bg=hover_color)

def on_leave(event, button, default_color):
    button.config(bg=default_color)

# Main GUI
def main_gui():
    global root, bg_photo
    root = tk.Tk()
    root.title("Face Recognition System")
    
    # Set window size and position
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
    # Add a background image
    try:
        bg_image = Image.open("background.jpg")  # Ensure the image path is correct
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error loading background image:", e)
    
    # Title Label
    title_label = tk.Label(root, text="Face Recognition System", font=("Arial", 24, "bold"), bg="white")
    title_label.pack(pady=20)
    
    # Buttons
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14), padding=10)
    
    register_button = tk.Button(root, text="Register Face", font=("Arial", 14), command=register, bg="#4CAF50", fg="white")
    register_button.pack(pady=10)
    register_button.bind("<Enter>", lambda e: on_enter(e, register_button, "#45a049"))
    register_button.bind("<Leave>", lambda e: on_leave(e, register_button, "#4CAF50"))
    
    attendance_button = tk.Button(root, text="Take Attendance", font=("Arial", 14), command=take_attendance, bg="#2196F3", fg="white")
    attendance_button.pack(pady=10)
    attendance_button.bind("<Enter>", lambda e: on_enter(e, attendance_button, "#0b7dda"))
    attendance_button.bind("<Leave>", lambda e: on_leave(e, attendance_button, "#2196F3"))
    
    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit, bg="#f44336", fg="white")
    exit_button.pack(pady=10)
    exit_button.bind("<Enter>", lambda e: on_enter(e, exit_button, "#da190b"))
    exit_button.bind("<Leave>", lambda e: on_leave(e, exit_button, "#f44336"))
    
    root.mainloop()

if __name__ == "__main__":
    main_gui()
