import cv2

from ultralytics import YOLO

model = YOLO(model="yolov8n.pt")
img = cv2.imread('/Users/jasonsze/Desktop/CSCE 483/ultralytics/2.165ft.png')
results = model(img)
prediction_boxes = zip(results[0].boxes.xyxy, results[0].boxes)
for x in prediction_boxes:
    x_min, y_min, x_max, y_max = map(int, x[0])
    print(x_max-x_min)
    
print(img.shape) # Print image shape (height, width, channels)

# Display original image
cv2.imshow("original", img)

# Calculate middle and margin for cropping horizontally
x_middle = int(img.shape[1] / 2)
x_margin = int(img.shape[1] / 6)

# Cropping the image (middle third horizontally)
cropped_image = img[0:img.shape[0], (x_middle - x_margin):(x_middle + x_margin)]

# Display cropped image
cv2.imshow("cropped", cropped_image)

# Save the cropped image
cv2.imwrite("Cropped_Image.jpg", cropped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
