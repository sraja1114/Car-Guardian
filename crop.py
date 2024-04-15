def crop_image(img):
    try:
        # Convert OpenCV frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Get the dimensions of the original image
        width, height = pil_image.size
        
        # Calculate the coordinates for cropping
        left = width // 3
        top = height // 3
        right = 2 * (width // 3)
        bottom = 2 * (height // 3)
        
        # Crop the image
        cropped_image = pil_image.crop((left, top, right, bottom))
        
        return cropped_image
    except Exception as e:
        print("An error occurred:", e)
        return None
