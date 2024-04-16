import wave
import torch
import FocalCalculation as FocalCalculation
import cv2
import numpy as np
from PIL import Image, ImageDraw

from ultralytics import YOLO

UNIVERSAL_COUNT = 0
CAR_REF_WIDTH = 78.6 #INCHES
AVG_CAR_WIDTH = 70 #INCHES

# distance finder function 
def distance_finder(focal_length, real_object_width, width_in_frmae):
    distance = (real_object_width * focal_length) / width_in_frmae
    return distance

def crop_image(img):
    try:
        x_middle = int(img.shape[1] / 2)
        x_margin = int(img.shape[1] / 6)

        # Cropping the image (middle third horizontally)
        cropped_image = img[0:img.shape[0], (x_middle - x_margin):(x_middle + x_margin)]
        return cropped_image
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def predict_lights(img):
    try:
        # Make predictions on the input image
        results = model(img)
        
        predictions = []
        image_np_rgb = img[:, :, ::-1]  # Convert BGR to RGB if necessary
        image_pil = Image.fromarray(image_np_rgb)  # Convert NumPy array to PIL Image
          # Display the original image
        draw = ImageDraw.Draw(image_pil)
        
        # Assume you are interested in the first prediction
        prediction_index = 0
        prediction_boxes = zip(results[prediction_index].boxes.xyxy, results[prediction_index].boxes)

        center_car = []

        for box in prediction_boxes:
            if (int(box[1].cls) == 2) or (int(box[1].cls) == 7):
                x_min, y_min, x_max, y_max = map(int, box[0])

                height = y_max - y_min
                width = x_max - x_min
                center = (x_min + x_max) / 2

                distance = distance_finder(interpolate_focal(width), CAR_REF_WIDTH, width)

                if center > 520 and center < 920:
                    center_car.append([center, distance, width, height])
                    draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)
                    #add background rectangle behind text 
                    draw.rectangle([(x_min, y_min - 20), (x_max, y_min)], fill=(0, 0, 0))
                    draw.text((x_min, y_min - 20), model.names[int(box[1].cls)], fill=(255, 255, 255))
                    #add distance
                    draw.text((x_min, y_min - 10), f'{round(distance/12, 2)} feet', fill=(255, 255, 255))
                    

            elif int(box[1].cls) == 9:  # Assuming class 9 corresponds to traffic light
                x_min, y_min, x_max, y_max = map(int, box[0])

                # Crop the region
                cropped_img = image_pil.crop((x_min, y_min, x_max, y_max))

                # Count the number of pixels for each color using HSV
                red_pixels, yellow_pixels, green_pixels = count_hsv_pixels(np.array(cropped_img))
                
                
                # Compare the counts to determine the traffic light color
                if red_pixels > green_pixels and red_pixels > yellow_pixels:
                    predictions.append("red")
                    print("Traffic light color: Red", red_pixels, green_pixels, yellow_pixels)
                elif green_pixels > red_pixels and green_pixels > yellow_pixels:
                    predictions.append("green")
                    print("Traffic light color: Green", red_pixels, green_pixels, yellow_pixels)
                elif yellow_pixels > red_pixels and yellow_pixels > green_pixels:
                    predictions.append("yellow")
                    print("Traffic light color: Yellow", red_pixels, green_pixels, yellow_pixels)
                else:
                    print("Unable to determine traffic light color")

                draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)
                draw.text((x_min, y_min - 10), model.names[int(box[1].cls)], fill=(255, 255, 255))
               

        if len(center_car) > 0:
            center_car = sorted(center_car, key=lambda x: abs(x[0] - 720))
            #if two cars are within 150 pixels of each other, find the area of the bounding box
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
            draw.ellipse((center_car[0][0] - 5, 540 - 5, center_car[0][0] + 5, 540 + 5), fill="green")

            #would run precollision warning here

            print("2", center_car)
            print(f"Distance: {pre_collision_dist} inches")

        return np.array(image_pil)
    except Exception as e:
        print("An error occurred during prediction:", e)
        return []



def count_hsv_pixels(image):
    # Convert RGB to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    # Define ranges for red, yellow, and green in HSV color space
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_green = np.array([60, 100, 100])
    upper_green = np.array([100, 255, 255])
    
    # Threshold the HSV image to get only desired colors
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
    
    # Count the number of red, yellow, and green pixels
    red_pixels = cv2.countNonZero(mask_red)
    yellow_pixels = cv2.countNonZero(mask_yellow)
    green_pixels = cv2.countNonZero(mask_green)
    
    return red_pixels, yellow_pixels, green_pixels


def process_frame(frame):
    global UNIVERSAL_COUNT
    try:
        # Call the crop_image function to crop the frame
        # cropped_frame = crop_image(frame)
        
        # Call the predict_lights function to predict traffic light colors
        new_frame = predict_lights(frame)
        
        
        
        return new_frame
    except Exception as e:
        print("An error occurred during frame processing:", e)
        return False

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

model = YOLO('yolov8n.pt').to(device)

interpolate_focal = FocalCalculation.CalculateFocalLengths()
# Initialize YOLO model


# Open webcam
cap = cv2.VideoCapture(2)
cap.set(3, 1440)
cap.set(4, 1080)

# print resolution of the camera
print('Width :',cap.get(3))
print('Height :',cap.get(4))

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Unable to open webcam.")
else:

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Check if the frame is captured successfully
        if not ret:
            print("Error: Unable to capture frame.")
            break
        
        # Process the frame
        processed_frame = process_frame(frame)
        processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)

        
        # Display the resulting frame
        cv2.imshow('frame', processed_frame_bgr)
        
        # Stop capturing when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the VideoWriter object


    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    
