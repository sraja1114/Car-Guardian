import tkinter as tk
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import interp1d

# Constants
REFERENCE_DISTANCES = [52.476, 101.22, 138.588, 177.756, 227.796, 267.396, 325.152, 390, 465.084, 532.836, 621.54, 966.264, 1291.2, 1484.76]
CAR_REF_WIDTH = 78.6  # INCHES
KNOWN_DISTANCE = 45  # INCHES
PERSON_WIDTH = 16  # INCHES
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3
COLORS = [(255, 0, 0), (255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
LIGHT_RED = (75, 71, 255)
FONTS = cv.FONT_HERSHEY_COMPLEX

# Load YOLO model
yoloNet = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
model = cv.dnn_DetectionModel(yoloNet)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

class VideoApp:
    def __init__(self, parent):
        self.parent = parent
        self.cap = cv.VideoCapture(0)
        self.cap.set(3, 1440)
        self.cap.set(4, 1080)
        self.canvas = tk.Canvas(parent, width=1440, height=1080)
        self.canvas.pack()
        self.focal_person = None
        self.interpolate_focal = None
        self.update_distances()
        self.update()

    def update_distances(self):
        # Read reference images and calculate focal lengths
        ref_person = cv.imread('ReferenceImages/person.jpeg')
        person_data = self.object_detector(ref_person)
        person_width_in_rf = person_data[0][1]
        self.focal_person = self.focal_length_finder(KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)

        car_focal_lengths = []
        car_widths = [1106]  # Initial width not recognized
        car_focal_lengths.append(self.focal_length_finder(25.98, CAR_REF_WIDTH, 1106))
        for i in range(len(REFERENCE_DISTANCES)):
            ref_car = cv.imread('ReferenceImages/car' + str(i) + '.png')
            car_data = self.object_detector(ref_car)
            car_width = car_data[0][1] if len(car_data) == 1 else max(item[1] for item in car_data)
            car_widths.append(car_width)
            car_focal_lengths.append(self.focal_length_finder(REFERENCE_DISTANCES[i], CAR_REF_WIDTH, car_width))
        car_widths.extend([0, 1440])  # Fillers for unknown and maximum width
        car_focal_lengths.extend([1440, 200])  # Assumed focal lengths
        self.interpolate_focal = interp1d(car_widths, car_focal_lengths, kind='cubic')

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            data = self.object_detector(frame)
            center_car = []
            cv.rectangle(frame, (520, 0), (920, 1080), LIGHT_RED, 2)
            for d in data:
                if d[0] == 'person':
                    distance = self.distance_finder(self.focal_person, PERSON_WIDTH, d[1])
                elif d[0] == 'car' or d[0] == 'truck':
                    distance = self.distance_finder(self.interpolate_focal(d[1]), CAR_REF_WIDTH, d[1])
                    center = int(d[2][0] + d[1] / 2)
                    if 520 < center < 920:
                        center_car.append([center, distance])
            if center_car:
                center_car = sorted(center_car, key=lambda x: abs(x[0] - 720))
                pre_collision_dist = center_car[0][1]
                cv.circle(frame, (center_car[0][0], 540), 5, (0, 255, 0), 5)
                print(f"Distance: {pre_collision_dist} inches")
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.parent.after(10, self.update)

    def object_detector(self, image):
        classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        data_list = []
        for (classid, _, box) in zip(classes, scores, boxes):
            color = COLORS[classid % len(COLORS)]
            label = "%s : %f" % (class_names[classid], _)
            cv.rectangle(image, box, color, 2)
            cv.putText(image, label, (box[0], box[1] - 14), FONTS, 0.5, color, 2)
            if classid in [0, 2, 7]:
                data_list.append([class_names[classid], box[2], (box[0], box[1] - 2)])
        return data_list

    @staticmethod
    def focal_length_finder(measured_distance, real_width, width_in_rf):
        return (width_in_rf * measured_distance) / real_width

    @staticmethod
    def distance_finder(focal_length, real_object_width, width_in_frame):
        return (real_object_width * focal_length) / width_in_frame

def main():
    root = tk.Tk()
    root.title("Car Guardian")
    video_app = VideoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
