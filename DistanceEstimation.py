import cv2 as cv 
import numpy as np
import scipy.interpolate as spi

# Distance constants 
REFERENCE_DISTANCES = [52.476, 101.22, 138.588, 177.756, 227.796, 267.396, 325.152, 390, 465.084, 532.836, 621.54, 966.264, 1291.2, 1484.76]
CAR_REF_WIDTH = 78.6 #INCHES
AVG_CAR_WIDTH = 70 #INCHES
KNOWN_DISTANCE = 45 #INCHES
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

# distance finder function 
def distance_finder(focal_length, real_object_width, width_in_frmae):
    distance = (real_object_width * focal_length) / width_in_frmae
    return distance

# reading the reference image from dir 
ref_person = cv.imread('ReferenceImages/person.jpeg')
person_data = object_detector(ref_person)
person_width_in_rf = person_data[0][1]

car_focal_lengths = []

# throw in closest image that is not recognized
car_widths = [1106]
car_focal_lengths.append(focal_length_finder(25.98, CAR_REF_WIDTH, 1106))

for i in range(len(REFERENCE_DISTANCES)):
    ref_car = cv.imread('ReferenceImages/car' + str(i) + '.png')
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

# finding person focal length
print(f"Person width in pixels : {person_width_in_rf}")
focal_person = focal_length_finder(KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)

# finding car focal length
print(f"Focal length for cars: {car_focal_lengths}")
focal_car = np.average(car_focal_lengths)

cap = cv.VideoCapture(2)
cap.set(3, 1440)
cap.set(4, 1080)

while True:
    ret, frame = cap.read()

    data = object_detector(frame)
    relative_velocity = 0
    center_car = []
    distances = []
    count = 0
    for d in data:
        if d[0] =='person':
            distance = distance_finder(focal_person, PERSON_WIDTH, d[1])
            x, y = d[2]
        elif d[0] =='car' or d[0] == 'truck':
            # print("Focal:", interpolate_focal(d[1]))
            distance = distance_finder (interpolate_focal(d[1]), CAR_REF_WIDTH, d[1])
            #distance = distance_finder (focal_car, CAR_REF_WIDTH, d[1])
            x, y = d[2]
            # print(count, ":", 'x:', x, 'y:', y)
            # if x is between 400 and 1000 then append the distance to the center_car list
            center = int(x + d[1]/2)
            if center > 520 and center < 920:
                center = int(x + d[1]/2)
                # cv.circle(frame, (center, 540), 5, GREEN, 3)
                center_car.append([center, distance, d[1], d[3]])
        count += 1 
        
        #print the distance of the car closest to the center
        if len(center_car) > 0:
            center_car = sorted(center_car, key=lambda x: abs(x[0] - 720))
            #if two cars are within 100 pixels of each other, find the area of the bounding box
            if len(center_car) > 1 and abs(center_car[0][0] - center_car[1][0]) < 150:
                area1 = center_car[0][2] * center_car[0][3] * (150 - abs(720 - center_car[0][0]))
                area2 = center_car[1][2] * center_car[1][3] * (150 - abs(720 - center_car[1][0]))

                #show area on screen
                # cv.putText(frame, f'Area1: {area1}', (center_car[0][0], 540), FONTS, 0.48, GREEN, 2)
                # cv.putText(frame, f'Area2: {area2}', (center_car[1][0], 540), FONTS, 0.48, GREEN, 2)
                # print("1",center_car)

                if area1 > area2:
                    # print("Area 1 Larger")
                    center_car.pop(1)
                else:
                    # print("Area 2 Larger")
                    center_car.pop(0)
            pre_collision_dist = center_car[0][1]
            distances.append(pre_collision_dist)
            print("2", center_car)
            cv.circle(frame, (center_car[0][0], 540), 5, GREEN, 5)
            print(f"Distance: {pre_collision_dist} inches")
        
        center = int(x + d[1]/2)
        if center > 520 and center < 920:
            cv.rectangle(frame, (x, y-3), (x+150, y+75),BLACK,-1 )
            #put a rectangle in the middle 1/3 of the frame (1440px wide)
            cv.rectangle(frame, (520, 0), (920, 1080), CYAN, 2)
            #put a point in the middle of the frame
            # cv.circle(frame, (720, 540), 5, GREEN, -1)
            cv.circle(frame, (350, 540), 5, GREEN, -1)
            cv.circle(frame, (1050, 540), 5, GREEN, -1)
            cv.putText(frame, f'Dis: {round(distance,2)} inches', (x+5,y+13), FONTS, 0.48, GREEN, 2)
            cv.putText(frame, f'Feet: {round(distance/12.0,2)} ft', (x+5,y+30), FONTS, 0.48, GREEN, 2)
            cv.putText(frame, f'Width: {round(d[1],2)} pixels', (x+5,y+48), FONTS, 0.48, LIGHT_RED, 2)
            #print x
            cv.putText(frame, f'X: {int(x + d[1]/2)}', (x+5,y+66), FONTS, 0.48, LIGHT_RED, 2)


    cv.imshow('frame',frame)
    
    key = cv.waitKey(1)
    if key ==ord('q'):
        break
cv.destroyAllWindows()
cap.release()

