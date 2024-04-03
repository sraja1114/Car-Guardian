import cv2
from scipy.io.wavfile import write


# Function to process each frame
def process_frame(frame):
    # Your frame processing logic goes here
    return frame

def main():
    # Open webcam
    cap = cv2.VideoCapture(1)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    
    # Sampling frequency and duration for audio recording
    freq = 44100
    duration = 5

    try:
        # Start audio recording
        

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            # Check if the frame is captured successfully
            if not ret:
                print("Error: Unable to capture frame.")
                break
            
            # Process the frame
            processed_frame = process_frame(frame)
            
            # Write the frame into the video file
            out.write(processed_frame)

            # Display the resulting frame
            cv2.imshow('frame', processed_frame)
            
            # Stop capturing when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    

    
    finally:
        # Release the VideoWriter object
        out.release()

        # Release the webcam and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
def stitcher():
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("audio.mp3")
    
if __name__ == "__main__":
    main()