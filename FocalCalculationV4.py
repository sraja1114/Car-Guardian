import cv2 as cv 
import numpy as np
import scipy.interpolate as spi

# Distance constants 
REFERENCE_DISTANCES = [52.476, 101.22, 138.588, 177.756, 227.796, 267.396, 325.152, 390, 465.084, 532.836, 621.54, 966.264, 1291.2, 1484.76]
CAR_REF_WIDTH = 78.6 #INCHES
PERSON_WIDTH = 16 #INCHES

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

def CalculateFocalLengths():

    # getting class names from classes.txt file 
    class_names = []
    with open("classes.txt", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
    #  setttng up opencv net
    yoloNet = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

    yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

    model = cv.dnn_DetectionModel(yoloNet)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    # object detector funciton /method
    def object_detector(image):
        classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        # creating empty list to add objects data
        data_list =[]
        for (classid, score, box) in zip(classes, scores, boxes):
            # define color of each, object based on its class id 
            color= COLORS[int(classid) % len(COLORS)]
        
            label = "%s : %f" % (class_names[classid], score)

            # draw rectangle on and label on object
            cv.rectangle(image, box, color, 2)
            cv.putText(image, label, (box[0], box[1]-14), FONTS, 0.5, color, 2)
        
            # getting the data 
            # 1: class name  2: object width in pixels, 3: position where have to draw text(distance)
            if classid ==0: # person class id 
                data_list.append([class_names[classid], box[2], (box[0], box[1]-2), box[3]])
            elif classid ==2: #car class id
                data_list.append([class_names[classid], box[2], (box[0], box[1]-2), box[3]])
            elif classid == 7: #truck class id
                data_list.append([class_names[classid], box[2], (box[0], box[1]-2), box[3]])
            # if you want inclulde more classes then you have to simply add more [elif] statements here
            # returning list containing the object data. 
        return data_list

    def focal_length_finder (measured_distance, real_width, width_in_rf):
        focal_length = (width_in_rf * measured_distance) / real_width

        return focal_length

    # reading the reference image from dir 
    ref_person = cv.imread('ReferenceImages/V4/person.jpeg')
    person_data = object_detector(ref_person)
    person_width_in_rf = person_data[0][1]

    car_focal_lengths = []

    # throw in closest image that is not recognized
    car_widths = [1106]
    car_focal_lengths.append(focal_length_finder(25.98, CAR_REF_WIDTH, 1106))

    for i in range(len(REFERENCE_DISTANCES)):
        ref_car = cv.imread('ReferenceImages/V4/car' + str(i) + '.png')
        car_data = object_detector(ref_car)

        # ignore objects in the background
        car_width = car_data[0][1]
        if len(car_data) > 1:
            car_width = max(item[1] for item in car_data)
        car_widths.append(car_width)

        print(f"Car {i} width in pixels: {car_width} - Distance: {REFERENCE_DISTANCES[i]} inches")
        car_focal_lengths.append(focal_length_finder(REFERENCE_DISTANCES[i], CAR_REF_WIDTH, car_width))

    # add filler values for when at 0 pixels and 1440 pixels
    # assume average focal length at far distances and 500 at close distances
    car_widths.append(0)
    car_focal_lengths.append(1440)
    car_widths.append(1440)
    car_focal_lengths.append(200)

    # interpolate the focal lengths
    interpolate_focal = spi.interp1d(car_widths, car_focal_lengths, kind='cubic')
    return interpolate_focal