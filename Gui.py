import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import pygetwindow as gw
import sys
import os

# Global variables
off = False
video_capture = None
capture_thread = None

# Handle face detection
def detect_faces(image):
    face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(faces), faces

# Minimize all windows
def close_tabs():
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        try:
            window.minimize()
        except Exception:
            pass  # Some windows can't be minimized

# Face monitoring logic
def on(video_frame):
    face_count, _ = detect_faces(video_frame)
    face_label.config(text=f"Faces detected: {face_count}")
    if face_count > 1:
        close_tabs()
    

# Turn on face detection
def on_button_click():
    global off, video_capture, capture_thread
    off = False
    messagebox.showinfo("Shy Programs", 'Shy Programs is ON')

    video_capture = cv2.VideoCapture(0)

    def capture():
        global off
        while not off:
            result, video_frame = video_capture.read()
            if not result:
                break
            on(video_frame)
        if video_capture:
            video_capture.release()
        cv2.destroyAllWindows()

    capture_thread = threading.Thread(target=capture, daemon=True)
    capture_thread.start()

# Turn off face detection
def off_button_click():
    global off
    off = True
    messagebox.showinfo("Shy Programs", 'Shy Programs is OFF')
    face_label.config(text="Faces detected: 0")

# Gradient background
def create_gradient(canvas, width, height, color1, color2):
    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)

# Tkinter UI setup
root = tk.Tk()
root.title("Shy Programs")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, 400, 300, (255, 140, 0), (75, 0, 130))

frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=230)

label = tk.Label(frame, text="Shy Programs", font=("Arial", 14), bg="#ffffff", fg="#333333")
label.pack(pady=5)

# Display number of faces
face_label = tk.Label(frame, text="Faces detected: 0", font=("Arial", 12), bg="#ffffff", fg="black")
face_label.pack(pady=5)

# ON Button
on_button = tk.Button(frame, text="Click to turn on", font=("Arial", 12), bg="#4CAF50", fg="white", command=on_button_click)
on_button.pack(pady=5)

# OFF Button
off_button = tk.Button(frame, text="Click to turn off", font=("Arial", 12), bg="#f44336", fg="white", command=off_button_click)
off_button.pack(pady=5)

# Entry (not connected to anything yet, but kept for UI)
entry = tk.Entry(frame, font=("Arial", 12), bg="#f0f0f0", fg="#333333")
entry.pack(pady=5)

# For PyInstaller compatibility
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller adds this
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root.protocol("WM_DELETE_WINDOW", lambda: (off_button_click(), root.destroy()))
root.mainloop()
