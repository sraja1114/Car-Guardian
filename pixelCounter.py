import cv2
import numpy as np

# Path to your image
test_image = "/Users/jasonsze/Desktop/CSCE 483/ultralytics/traffic-light-colors-GettyImages-689407322-MLedit.jpg"

# Read the image
img = cv2.imread(test_image)

# Convert to CIELAB color space
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Define lower and upper bounds for red, green, and yellow colors in LAB
lower_red = np.array([0, 128, 128])
upper_red = np.array([255, 255, 255])

lower_green = np.array([0, -128, 0])
upper_green = np.array([255, 127, 128])

lower_yellow = np.array([0, 0, 128])
upper_yellow = np.array([255, 255, 255])

# Mask of red, green, and yellow colors
mask_red = cv2.inRange(lab, lower_red, upper_red)
mask_green = cv2.inRange(lab, lower_green, upper_green)
mask_yellow = cv2.inRange(lab, lower_yellow, upper_yellow)

# Apply masks to original image
red_pixels = cv2.bitwise_and(img, img, mask=mask_red)
green_pixels = cv2.bitwise_and(img, img, mask=mask_green)
yellow_pixels = cv2.bitwise_and(img, img, mask=mask_yellow)

# Display masks and original image
cv2.imshow("Red Mask", red_pixels)
cv2.imshow("Green Mask", green_pixels)
cv2.imshow("Yellow Mask", yellow_pixels)
cv2.imshow("Original Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
