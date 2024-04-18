import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
from functools import partial

class VideoApp:
    def __init__(self, parent):
        self.parent = parent
        self.video_source = 0
        self.vid = cv.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(parent, width=self.vid.get(cv.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.parent.after(10, self.update)

def Sensitivity_change(button):
    current_text = button.cget("text")
    if current_text == "High":
        button.config(text="Low")
    elif current_text == "Medium":
        button.config(text="High")
    elif current_text == "Low":
        button.config(text="Medium")

def dashcam_switch():
    print("Switching to Dashcam mode...")

def settings_open():
    print("Opening settings...")

def main():
    root = tk.Tk()
    root.title("Car Guardian")

    # Create frames for video and buttons
    video_frame = tk.Frame(root, bg="black")
    video_frame.grid(row=0, column=0, padx=10, pady=10)

    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=1, padx=10, pady=10)

    # Create a label widget
    label = tk.Label(button_frame, text="I love Car Guardian <3", font=("Arial", 12))
    label.grid(row=0, column=0, pady=(10, 30), sticky="n")  # Place the label using grid layout manager

    # Create buttons
    Sens_button = tk.Button(button_frame, text="High", command=partial(Sensitivity_change, Sens_button), width=20, height=2, font=("Arial", 10))
    Sens_button.grid(row=1, column=0, pady=(0, 10))

    dashcam_button = tk.Button(button_frame, text="Dashcam", command=dashcam_switch, width=20, height=2, font=("Arial", 10))
    dashcam_button.grid(row=2, column=0, pady=(0, 10))

    settings_button = tk.Button(button_frame, text="Settings", command=settings_open, width=20, height=2, font=("Arial", 10))
    settings_button.grid(row=3, column=0, pady=(0, 10))

    # Create and run the video app
    video_app = VideoApp(video_frame)

    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
