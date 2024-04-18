import cv2 as cv
import numpy as np
import scipy.interpolate as spi  # Add this line
import sounddevice as sd
import wavio as wv
from scipy.io.wavfile import write
from PIL import Image, ImageTk
import tkinter as tk

class VideoApp:
    def __init__(self, parent):
        self.parent = parent
        self.video_label = tk.Label(parent)
        self.video_label.pack()
        
        self.cap = cv.VideoCapture(0)
        
        # Settings for audio recording
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5

        # Distance constants
        self.REFERENCE_DISTANCES = [49, 121, 177, 241, 294.5, 353, 415]
        self.CAR_REF_WIDTH = 72.6  # INCHES
        self.KNOWN_DISTANCE = 45  # INCHES
        self.PERSON_WIDTH = 16  # INCHES

        # Object detector constant
        self.CONFIDENCE_THRESHOLD = 0.4
        self.NMS_THRESHOLD = 0.3

        # colors for object detected
        self.COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        self.GREEN = (0,255,0)
        self.LIGHT_RED = (75, 71, 255)
        self.CYAN = (0, 255, 255)
        self.WHITE = (255,255,255)
        self.BLACK =(0,0,0)

        # defining fonts
        self.FONTS = cv.FONT_HERSHEY_COMPLEX

        # getting class names from classes.txt file
        self.class_names = []
        with open("classes.txt", "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]
        
        # setting up opencv net
        self.yoloNet = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
        self.yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

        self.model = cv.dnn_DetectionModel(self.yoloNet)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

        # Read reference image for person
        self.ref_person = cv.imread('ReferenceImages/person.jpeg')
        person_data = self.object_detector(self.ref_person)
        self.person_width_in_rf = person_data[0][1]

        # Calculate car focal lengths
        self.car_focal_lengths = []
        self.car_widths = []
        for i in range(len(self.REFERENCE_DISTANCES)):
            ref_car = cv.imread(f'ReferenceImages/car{i}.png')
            car_data = self.object_detector(ref_car)

            car_width = car_data[0][1]
            if len(car_data) > 1:
                car_width = max(item[1] for item in car_data)
            self.car_widths.append(car_width)

            self.car_focal_lengths.append(self.focal_length_finder(self.REFERENCE_DISTANCES[i], self.CAR_REF_WIDTH, car_width))

        # Add filler values
        self.car_widths.extend([0, 1440])
        self.car_focal_lengths.extend([1130, 500])

        # Interpolate the focal lengths
        self.interpolate_focal = spi.interp1d(self.car_widths, self.car_focal_lengths, kind='cubic')

        # Find person focal length
        self.focal_person = self.focal_length_finder(self.KNOWN_DISTANCE, self.PERSON_WIDTH, self.person_width_in_rf)

        # Find car focal length
        self.focal_car = np.average(self.car_focal_lengths)

        # VideoWriter
        self.fourcc = cv.VideoWriter_fourcc(*'XVID')
        self.out = cv.VideoWriter('Saved Videos/out.mp4', self.fourcc, 20.0, (int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

        # Audio saving
        self.WAVE_OUTPUT_FILENAME = "Saved Videos/output_audio.wav"

    def object_detector(self, image):
        classes, scores, boxes = self.model.detect(image, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        data_list =[]
        for (classid, score, box) in zip(classes, scores, boxes):
            color= self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s : %f" % (self.class_names[classid], score)

            cv.rectangle(image, box, color, 2)
            cv.putText(image, label, (box[0], box[1]-14), self.FONTS, 0.5, color, 2)

            if classid ==0:
                data_list.append([self.class_names[classid], box[2], (box[0], box[1]-2)])
            elif classid ==2:
                data_list.append([self.class_names[classid], box[2], (box[0], box[1]-2)])
        return data_list

    def focal_length_finder(self, measured_distance, real_width, width_in_rf):
        focal_length = (width_in_rf * measured_distance) / real_width
        return focal_length

    def distance_finder(self, focal_length, real_object_width, width_in_frmae):
        distance = (real_object_width * focal_length) / width_in_frmae
        return distance

    def run(self):
        while True:
            ret, frame = self.cap.read()

            data = self.object_detector(frame) 
            for d in data:
                if d[0] =='person':
                    distance = self.distance_finder(self.focal_person, self.PERSON_WIDTH, d[1])
                    x, y = d[2]
                elif d[0] =='car':
                    distance = self.distance_finder(self.interpolate_focal(d[1]), self.CAR_REF_WIDTH, d[1])
                    x, y = d[2]
                cv.rectangle(frame, (x, y-3), (x+150, y+40), self.BLACK,-1 )
                cv.putText(frame, f'Dis: {round(distance,2)} inches', (x+5,y+13), self.FONTS, 0.48, self.GREEN, 2)
                cv.putText(frame, f'Width: {round(d[1],2)} pixels', (x+5,y+30), self.FONTS, 0.48, self.LIGHT_RED, 2)

            if ret:
                self.out.write(frame)
                # Convert the frame from BGR to RGB
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                
                # Convert the frame to a PIL Image
                image = Image.fromarray(frame)
                
                # Convert the PIL Image to a Tkinter PhotoImage
                photo = ImageTk.PhotoImage(image=image)
                
                # Update the label with the new frame
                self.video_label.config(image=photo)
                self.video_label.image = photo
                
                # Check for the 'q' key to quit
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.out.release()
        self.cap.release()
        cv.destroyAllWindows()

# Create the main application window
root = tk.Tk()
root.title("Car Guardian")

# Create an instance of VideoApp
app = VideoApp(root)

# Run the app
app.run()

# Run the main event loop
root.mainloop()
