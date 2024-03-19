import cv2 as cv 
import numpy as np
import scipy.interpolate as spi

# Distance constants 
REFERENCE_DISTANCES = [49, 121, 177, 241, 294.5, 353, 415]
CAR_REF_WIDTH = 72.6 #INCHES
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
            data_list.append([class_names[classid], box[2], (box[0], box[1]-2)])
        elif classid ==2:
            data_list.append([class_names[classid], box[2], (box[0], box[1]-2)])
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
car_widths = []
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
car_focal_lengths.append(1130)
car_widths.append(1440)
car_focal_lengths.append(500)

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
    for d in data:
        if d[0] =='person':
            distance = distance_finder(focal_person, PERSON_WIDTH, d[1])
            x, y = d[2]
        elif d[0] =='car':
            distance = distance_finder (interpolate_focal(d[1]), CAR_REF_WIDTH, d[1])
            #distance = distance_finder (focal_car, CAR_REF_WIDTH, d[1])
            x, y = d[2]
        cv.rectangle(frame, (x, y-3), (x+150, y+40),BLACK,-1 )
        cv.putText(frame, f'Dis: {round(distance,2)} inches', (x+5,y+13), FONTS, 0.48, GREEN, 2)
        cv.putText(frame, f'Width: {round(d[1],2)} pixels', (x+5,y+30), FONTS, 0.48, LIGHT_RED, 2)

    cv.imshow('frame',frame)
    
    key = cv.waitKey(1)
    if key ==ord('q'):
        break
cv.destroyAllWindows()
cap.release()

