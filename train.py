import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw

from ultralytics import YOLO

UNIVERSAL_COUNT = 0

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

        for box in prediction_boxes:
            if int(box[1].cls) != 9:  # Assuming class 9 corresponds to traffic light
                continue
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

            # Display the cropped image
            draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)
            
        return predictions
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
        cropped_frame = crop_image(frame)
        
        # Call the predict_lights function to predict traffic light colors
        predictions = predict_lights(cropped_frame)
        
        
        
        return True
    except Exception as e:
        print("An error occurred during frame processing:", e)
        return False



model = YOLO('yolov8n.pt')

# Initialize YOLO model


# Open webcam
cap = cv2.VideoCapture(0)

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
            processed_frame = frame

            
            # Display the resulting frame
            cv2.imshow('frame', processed_frame)
            
            # Stop capturing when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Release the VideoWriter object


    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    
