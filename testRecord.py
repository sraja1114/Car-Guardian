import sys
import cv2
import os
import threading  # Import threading module
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import pyaudio
import wave
from datetime import datetime
from collections import deque
from moviepy.editor import VideoFileClip, AudioFileClip

from moviepy.audio.io.AudioFileClip import AudioFileClip


class VideoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Guardian")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.canvas_label = QLabel()
        self.canvas_label.setAlignment(Qt.AlignCenter)
        self.canvas_label.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.canvas_label.setFixedSize(800, 600)

        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.toggle_recording)

        self.save_button = QPushButton("Save Last 10 Seconds")
        self.save_button.clicked.connect(self.save_last_10_seconds)

        self.record_buffer = deque(maxlen=1800)
        self.audio_buffer = []
        self.recording = True
        self.record_audio()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas_label)
        layout.addWidget(self.record_button)
        layout.addWidget(self.save_button)
        self.central_widget.setLayout(layout)

        self.update()

    def record_audio(self):
        def audio_thread_func():
            p = pyaudio.PyAudio()
            chunk = 1024
            sample_format = pyaudio.paInt16
            channels = 1
            fs = 44100
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)
            while True:
                data = stream.read(chunk)
                self.audio_buffer.append(data)
                if len(self.audio_buffer) > 1800:
                    self.audio_buffer.pop(0)

        audio_thread = threading.Thread(target=audio_thread_func)
        audio_thread.start()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            qImg = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.canvas_label.setPixmap(pixmap)

            if self.recording:
                frame = cv2.resize(frame, (1440, 1080))
                self.record_buffer.append(frame)

        QTimer.singleShot(10, self.update)

    def toggle_recording(self):
        self.recording = not self.recording

    def save_last_10_seconds(self):
        if len(self.record_buffer) > 0 and len(self.audio_buffer) > 0:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            video_filename = f'Saved Videos/{current_time}_video.mp4'
            audio_filename = f'Saved Videos/{current_time}_audio.wav'

            # Calculate the number of frames corresponding to 10 seconds
            fps = 30  # Assuming 30 frames per second
            num_frames = 10 * fps

            # Trim the video buffer to the last 10 seconds of frames
            last_10_seconds_frames = list(self.record_buffer)[-num_frames:]

            # Trim the audio buffer to match the duration of the last 10 seconds of video
            # Calculate the corresponding number of audio samples
            fs = 44100  # Audio sampling frequency
            max_audio_samples = len(last_10_seconds_frames) * int(fs / fps)
            if len(self.audio_buffer) > max_audio_samples:
                self.audio_buffer = self.audio_buffer[-max_audio_samples:]

            out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (1440, 1080))
            for frame in last_10_seconds_frames:
                out.write(frame)
            out.release()

            wf = wave.open(audio_filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.audio_buffer))
            wf.close()

            video_clip = VideoFileClip(video_filename)
            audio_clip = AudioFileClip(audio_filename)
            video_clip = video_clip.set_audio(audio_clip)
            video_clip.write_videofile(f'Saved Videos/{current_time}.mp4', codec='libx264', audio_codec='aac')

            os.remove(video_filename)
            os.remove(audio_filename)

            self.record_buffer.clear()
            self.audio_buffer.clear()
            print(f"Video segment saved successfully as: {current_time}.mp4")

    def toggle_recording(self):
        self.recording = not self.recording
        if not self.recording:
            self.save_last_10_seconds()
            self.record_buffer.clear()
            self.audio_buffer.clear()


    def closeEvent(self, event):
        # Release the camera when the application is closed
        self.vid.release()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if not os.path.exists("Saved Videos"):
        os.makedirs("Saved Videos")
    main()
