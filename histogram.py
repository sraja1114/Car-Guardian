import cv2
import matplotlib.pyplot as plt
import numpy as np

# Path to your image
test_image = "/Users/jasonsze/Desktop/CSCE 483/ultralytics/traffic-light-colors-GettyImages-689407322-MLedit.jpg"

# Read the image
img = cv2.imread(test_image)

# Convert to CIELAB color space
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Split LAB image into channels
l_channel, a_channel, b_channel = cv2.split(lab)

# Plot histograms for each channel
plt.figure(figsize=(10, 5))

# Plot histogram for L channel
plt.subplot(1, 3, 1)
plt.hist(l_channel.flatten(), bins=256, color='gray', alpha=0.5)
plt.title('L Channel Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

# Plot histogram for a channel
plt.subplot(1, 3, 2)
plt.hist(a_channel.flatten(), bins=256, color='r', alpha=0.5)
plt.title('a Channel Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

# Plot histogram for b channel
plt.subplot(1, 3, 3)
plt.hist(b_channel.flatten(), bins=256, color='b', alpha=0.5)
plt.title('b Channel Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
