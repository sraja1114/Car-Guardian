import cv2 as cv 
import numpy as np
import matplotlib.pyplot as plt
import torch
import scipy.interpolate as spi
from ultralytics import YOLO

# Distance constants 
REFERENCE_DISTANCES = [25.98, 52.476, 101.22, 138.588, 177.756, 227.796, 267.396, 325.152, 390, 465.084, 532.836, 621.54, 966.264, 1291.2, 1484.76]
CAR_REF_WIDTH = 78.6 #INCHES
AVG_CAR_WIDTH = 70 #INCHES
DISTANCE_FROM_FRONT = 57.76 #INCHES

# Object detector constant
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3
 
# colors for object detected
COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN = (0,255,0)
LIGHT_RED = (75, 71, 255)
CYAN = (0, 255, 255)
WHITE = (255,255,255)
BLACK =(0,0,0)
# defining fonts 
FONTS = cv.FONT_HERSHEY_COMPLEX

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

model = YOLO('yolov8n.pt').to(device)

def focal_length_finder (measured_distance, real_width, width_in_rf):
        focal_length = (width_in_rf * measured_distance) / real_width

        return focal_length

def calculate_focal(img, index):
    try:
        # Make predictions on the input image
        results = model.predict(img)
        
        # Assume you are interested in the first prediction
        prediction_index = 0
        prediction_boxes = list(zip(results[prediction_index].boxes.xyxy, results[prediction_index].boxes))

        center_car = []

        for box in prediction_boxes:
            if (int(box[1].cls) == 2) or (int(box[1].cls) == 7):
                x_min, y_min, x_max, y_max = map(int, box[0])

                height = y_max - y_min
                width = x_max - x_min
                center = (x_min + x_max) / 2

                focal_length = focal_length_finder(REFERENCE_DISTANCES[index] + DISTANCE_FROM_FRONT, CAR_REF_WIDTH, width)

                if center > 520 and center < 920:
                    center_car.append([center, focal_length, width, height])
                    
        print("Count", len(prediction_boxes))
        print("Center Car", center_car)

        if len(center_car) > 0:
            center_car = sorted(center_car, key=lambda x: abs(x[0] - 720))
            #if two cars are within 150 pixels of each other, find the area of the bounding box
            if len(center_car) > 1 and abs(center_car[0][0] - center_car[1][0]) < 150:
                area1 = center_car[0][2] * center_car[0][3] * (150 - abs(720 - center_car[0][0]))
                area2 = center_car[1][2] * center_car[1][3] * (150 - abs(720 - center_car[1][0]))

                if area1 > area2:
                    # print("Area 1 Larger")
                    center_car.pop(1)
                else:
                    # print("Area 2 Larger")
                    center_car.pop(0)
                
            print(f"Car {index} width in pixels: {center_car[0][2]} - Distance: {REFERENCE_DISTANCES[index]} inches")
            return [center_car[0][1], center_car[0][2]]
        
        return [0, 0]
    except Exception as e:
        print("An error occurred during prediction:", e)
        return [0, 0]


def CalculateFocalLengths():

    car_focal_lengths = []
    car_widths = []

    # throw in closest image that is not recognized

    for i in range(len(REFERENCE_DISTANCES)):
        ref_car = cv.imread('ReferenceImages/car' + str(i) + '.png')
        focal_length, width = calculate_focal(ref_car, i)
        car_focal_lengths.append(focal_length)
        car_widths.append(width)

    # add filler values for when at 0 pixels and 1440 pixels
    # assume average focal length at far distances and 500 at close distances
    car_widths.append(0)
    car_focal_lengths.append(1650)
    car_widths.append(1440)
    car_focal_lengths.append(1050)

    print("Car Focal Lengths", car_focal_lengths)
    print("Car Widths", car_widths)

    # interpolate the focal lengths
    interpolate_focal = spi.interp1d(car_widths, car_focal_lengths, kind='cubic')

    #plot interpolated focal lengths
    x = np.linspace(0, 1440, 1000)
    y = interpolate_focal(x)
    plt.plot(x, y)
    plt.show()

    return interpolate_focal