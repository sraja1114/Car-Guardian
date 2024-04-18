import cv2


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        # Get the HSV values of the pixel under the cursor
        h, s, v = hsv_img[y, x]
        print(f"Hovering over pixel at ({x}, {y}): Hue={h}, Saturation={s}, Value={v}")

# Path to your PNG image
png_image_path = "/Users/jasonsze/Desktop/CSCE 483/ultralytics/testa.png"

# Read the PNG image
img = cv2.imread(png_image_path)

# Convert the image to HSV color space
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create a window and bind the mouse event callback function
cv2.namedWindow("HSV Image")
cv2.setMouseCallback("HSV Image", on_mouse)

# Display the HSV image
cv2.imshow("HSV Image", hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
