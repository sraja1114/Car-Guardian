import cv2
import numpy as np

# Path to your image
test_image = "/Users/jasonsze/Desktop/CSCE 483/ultralytics/testb.png"

# Read the image
img = cv2.imread(test_image)

# Convert to CIELAB color space
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Define lower and upper bounds for green color in LAB (on the 'a' channel)
lower_green = np.array([0, 0, 0])
upper_green = np.array([255, 127, 255])  # Adjust upper bounds accordingly based on the 'a' channel range

# Mask of green color
mask = cv2.inRange(lab, lower_green, upper_green)

# Apply the mask to the original image
green = cv2.bitwise_and(img, img, mask=mask)

# Display the sliced green image
cv2.imshow("Filtered Green Image", green)
cv2.waitKey(0)
cv2.destroyAllWindows()
