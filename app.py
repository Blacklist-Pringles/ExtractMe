import cv2
import easyocr

# Specify the languages to be recognized
languages = ['en']  # English

# Initialize the EasyOCR reader
reader = easyocr.Reader(languages)

# Read the image
image_path = 'images/Sample2.jpg'
image = cv2.imread(image_path)
original_image = image.copy()

# Define the starting and ending points of the rectangle
start_point = None
end_point = None
drawing = False

# Define the callback function for mouse events
def draw_rectangle(event, x, y, flags, param):
    global image, start_point, end_point, drawing, original_image
    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing the rectangle
        start_point = (x, y)
        end_point = (x, y)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Update the ending point as the mouse is moved
            end_point = (x, y)
            # Display the rectangle on the image
            image = original_image.copy()
            cv2.rectangle(image, start_point, end_point, (0, 0, 255), 2) # draw a red rectangle
            cv2.imshow(window_name, image)
    elif event == cv2.EVENT_LBUTTONUP:
        # Finish drawing the rectangle
        end_point = (x, y)
        drawing = False

# Create a window to display the image
window_name = 'Image'
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, draw_rectangle)

while True:
    # Display the image
    cv2.imshow(window_name, image)
    key = cv2.waitKey(1)
    # Extract text within the rectangle when 'c' key is pressed
    if key == ord('c') and not drawing:
        if start_point and end_point:
            # Check if the selected region is valid
            if start_point[0] < end_point[0] and start_point[1] < end_point[1]:
                roi = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                if roi.size != 0:
                    result = reader.readtext(roi)
                    if len(result) > 0:
                        for detection in result:
                            text = detection[1]
                            print(text)
                    else:
                        print("No text detected in the selected region.")
            else:
                print("Invalid region selected.")
    elif key == 27:  # Press Esc key to exit
        break

cv2.destroyAllWindows()
