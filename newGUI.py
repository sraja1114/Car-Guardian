import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
import os
from collections import deque
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_audioclips

from pyffmpeg import FFmpeg


class VideoApp:
    def __init__(self, parent):
        self.parent = parent
        self.video_source = 0
        self.vid = cv.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(parent, width=self.vid.get(cv.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.recording = True  # Start recording automatically
        self.record_buffer = deque(maxlen=200)  # Buffer to store last 10 seconds of frames
        self.audio_buffer = []  # List to store audio clips
        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            if self.recording:
                self.record_buffer.append(frame)
                # Capture audio frame
                ret, audio_frame = self.vid.read()  # Assuming audio is recorded along with video
                if ret:
                    self.audio_buffer.append(audio_frame)
        self.parent.after(10, self.update)

    def toggle_recording(self):
        self.recording = not self.recording
        if not self.recording:
            self.save_video_segment()

    def save_video_segment(self):
        if len(self.record_buffer) > 0 and len(self.audio_buffer) > 0:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get current time as a string
            video_filename = f'Saved Videos/{current_time}_video.mp4'  # Video filename with timestamp
            audio_filename = f'Saved Videos/{current_time}_audio.mp3'  # Audio filename with timestamp

            # Write video frames to a temporary video file
            out = cv.VideoWriter(video_filename, cv.VideoWriter_fourcc(*'mp4v'), 20.0, (int(self.vid.get(cv.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv.CAP_PROP_FRAME_HEIGHT))))
            for frame in self.record_buffer:
                out.write(frame)
            out.release()

            # Write audio clips to a temporary audio file
            final_audio = concatenate_audioclips(self.audio_buffer)
            final_audio.write_audiofile(audio_filename)

            # Merge video and audio files
            video_clip = VideoFileClip(video_filename)
            video_clip.audio = AudioFileClip(audio_filename)
            video_clip.write_videofile(f'Saved Videos/{current_time}.mp4', codec='libx264', audio_codec='aac')

            # Clean up temporary files
            os.remove(video_filename)
            os.remove(audio_filename)

            self.record_buffer.clear()
            self.audio_buffer.clear()
            print("Video segment saved successfully as:", {current_time})


def Sensitivity_change(button):
    current_text = button.cget("text")
    if current_text == "High":
        button.config(text="Low")
    elif current_text == "Medium":
        button.config(text="High")
    elif current_text == "Low":
        button.config(text="Medium")

def open_video(event):
    selected_video_frame = event.widget  # Get the frame associated with the clicked video
    filename_label = selected_video_frame.winfo_children()[1]  # Get the label containing the filename
    selected_video = filename_label.cget("text")  # Get the filename
    video_path = os.path.join("Saved Videos", selected_video)
    os.startfile(video_path)  # Open the selected video file using the default application

# def get_video_thumbnail(video_path):
#     video = video_path
#     thumbImage = 'thumb.jpeg'
#     ff = FFmpeg()
#     ff.convert(video,thumbImage)

#     return thumbImage

def on_mousewheel(event, canvas):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

def dashcam_switch():
    dashcam_window = tk.Toplevel()  # Create a new window
    dashcam_window.title("Dashcam Videos")  # Set window title

    # Set the geometry of dashcam_window
    dashcam_window.geometry("600x400+740+0")  # Set the size and position

    # Create a canvas to contain the video entries
    canvas = tk.Canvas(dashcam_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame to contain the video entries
    video_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=video_frame, anchor=tk.NW)

    # Path to the folder containing the video files
    folder_path = "Saved Videos"

    # Get a list of all files in the folder
    all_files = os.listdir(folder_path)

    # Display each video entry in a card format
    for file in all_files:
        video_entry_frame = tk.Frame(video_frame, bg="white", bd=1, relief=tk.RAISED)
        video_entry_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Load video thumbnail (you need to implement this)
        thumbnail_label = tk.Label(video_entry_frame, text="Thumbnail", bg="gray", width=10, height=5)
        thumbnail_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Display video filename
        filename_label = tk.Label(video_entry_frame, text=file, font=("Arial", 10))
        filename_label.pack(side=tk.TOP, pady=(5, 0))

        # Bind click event to open the video
        video_entry_frame.bind("<Button-1>", open_video)

    # Add a scrollbar for the canvas
    scrollbar = tk.Scrollbar(dashcam_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    # Allow canvas to scroll
    canvas.bind('<Configure>', lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas: on_mousewheel(event, canvas))


def settings_open():
    settings_window = tk.Toplevel()  # Create a new window
    settings_window.title("Settings")  # Set window title

    # Set the geometry of settings_window
    settings_window.geometry("400x300+740+0")  # Set the size and position

    # Add widgets or content to the settings window as needed

def main():
    root = tk.Tk()
    root.title("Car Guardian")

    # Create frames for video and buttons
    video_frame = tk.Frame(root, bg="black")
    video_frame.grid(row=0, column=0, padx=10, pady=10)

    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=1, padx=10, pady=10)

    # Create a label widget
    # Assuming you have an image file named "logo.png" in the current directory
    image_path = "logo.png"
    image = tk.PhotoImage(file=image_path)
    # Resize the image
    image = image.subsample(2)  # Adjust the subsample value to change the size

    # Create the label widget with both text and image
    label = tk.Label(button_frame, text="I love Car Guardian <3", image=image, compound=tk.TOP, font=("Arial", 12))
    label.grid(row=0, column=0, pady=(10, 30), sticky="n")  # Place the label using grid layout manager


    # Create buttons
    Sens_button = tk.Button(button_frame, text="High", command=lambda: Sensitivity_change(Sens_button), width=20, height=2, font=("Arial", 10))
    Sens_button.grid(row=1, column=0, pady=(0, 10))

    dashcam_button = tk.Button(button_frame, text="Dashcam", command=dashcam_switch, width=20, height=2, font=("Arial", 10))
    dashcam_button.grid(row=2, column=0, pady=(0, 10))

    settings_button = tk.Button(button_frame, text="Settings", command=settings_open, width=20, height=2, font=("Arial", 10))
    settings_button.grid(row=3, column=0, pady=(0, 10))

    # Create and run the video app
    video_app = VideoApp(video_frame)

    # Button to start/stop recording
    record_button = tk.Button(button_frame, text="Record", command=video_app.toggle_recording, width=20, height=2, font=("Arial", 10))
    record_button.grid(row=4, column=0, pady=(0, 10))

    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    if not os.path.exists("Saved Videos"):
        os.makedirs("Saved Videos")
    main()
