from datetime import datetime
import os
import time
import cv2
import pyaudio
import wave
import threading
import moviepy.editor as mp

# Set filename output
filename_video = "webcam_output.mp4"
filename_audio = "microphone_output.wav"

# Set resolution
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Set video codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename_video, fourcc, 60.0, (1440, 1080))

# Set audio recorder settings
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100

p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

# Flag to control the audio recording loop
is_recording = True

# Create a thread for audio recording
def record_audio(stream, frames):
    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

# Start the thread for audio recording
thread = threading.Thread(target=record_audio, args=(stream, frames,))
thread.start()

print("Recording...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame into the file 'output.mp4'
    out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Set the flag to stop the audio recording loop
is_recording = False

# Wait for the audio recording thread to complete
thread.join()

print("Done recording.")

# Release everything when job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

# Stop and close the stream 
stream.stop_stream()
stream.close()

# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename_audio, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

# Load video clip
video_clip = mp.VideoFileClip(filename_video)

# Load audio clip
audio_clip = mp.AudioFileClip(filename_audio)

# Set audio attribute to video clip
video_clip = video_clip.set_audio(audio_clip)

# Write final video file with ".mp4" extension
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get current time as a string
output_filename = f'Saved Videos/{current_time}.mp4'
video_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

# Delete the temporary video and audio files
os.remove(filename_video)
os.remove(filename_audio)

print(f'Final video saved as: {output_filename}.mp4')