import cv2
import numpy as np


def apply_mask(image, lower_bound, upper_bound):
    """
    Apply a mask to the input image based on the given lower and upper bounds.

    Parameters:
        image (numpy.ndarray): Input image in BGR color space.
        lower_bound (tuple): Lower bound for the color in HSV color space.
        upper_bound (tuple): Upper bound for the color in HSV color space.

    Returns:
        numpy.ndarray: Image with the applied mask.
    """
    # Convert BGR image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask to extract regions of the specified color
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    # Apply the mask to the original image
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    
    return masked_image

def green_mask(image):
    """
    Apply a green mask to the input image.

    Parameters:
        image (numpy.ndarray): Input image in BGR color space.

    Returns:
        numpy.ndarray: Image with the green mask applied.
    """
    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([60, 40, 40])  # Adjust these values as needed
    upper_green = np.array([100, 255, 255])  # Adjust these values as needed
    
    # Apply the green mask
    green_masked_image = apply_mask(image, lower_green, upper_green)
    
    return green_masked_image

def yellow_mask(image):
    """
    Apply a yellow mask to the input image.

    Parameters:
        image (numpy.ndarray): Input image in BGR color space.

    Returns:
        numpy.ndarray: Image with the yellow mask applied.
    """
    # Define lower and upper bounds for yellow color in HSV
    lower_yellow = np.array([20, 100, 100])  # Adjust these values as needed
    upper_yellow = np.array([40, 255, 255])  # Adjust these values as needed
    
    # Apply the yellow mask
    yellow_masked_image = apply_mask(image, lower_yellow, upper_yellow)
    
    return yellow_masked_image

def red_mask(image):
    """
    Apply a red mask to the input image.

    Parameters:
        image (numpy.ndarray): Input image in BGR color space.

    Returns:
        numpy.ndarray: Image with the red mask applied.
    """
    # Define lower and upper bounds for red color in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # Apply the red mask
    red_masked_image = apply_mask(image, lower_red1, upper_red1)
    red_masked_image += apply_mask(image, lower_red2, upper_red2)  # Combining masks for red color
    
    return red_masked_image

image_path = "/Users/jasonsze/Desktop/CSCE 483/ultralytics/traffic-light-colors-GettyImages-689407322-MLedit.jpg"

image = cv2.imread(image_path)

cv2.imshow("Image", red_mask(image))
cv2.waitKey(0)
cv2.destroyAllWindows()
