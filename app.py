from flask import Flask, render_template, request, jsonify
import cv2
import easyocr
import numpy as np


app = Flask(__name__)

# Initialize the EasyOCR reader
languages = ['en']  # Specify the languages to be recognized
reader = easyocr.Reader(languages)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to extract text from selected area in user-uploaded image
@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Get data via AJAX from the selected region of interest in the image
        roi_data = request.get_json()

        # Extract the data from roi_data
        startX = roi_data['startX']  # int
        startY = roi_data['startY']  # int
        endX = roi_data['endX']  # int
        endY = roi_data['endY']  # int
        imageData = roi_data['imageData'] # array of pixel data within ROI

        # Convert the pixel data to a NumPy array
        numpy_array = np.array(imageData, dtype=np.uint8)

        # Reshape the NumPy array to the desired dimensions (height, width, channels)
        image = numpy_array.reshape((endY - startY, endX - startX, -1))  #  -1 indicates that the number of channels should be inferred from the array itself.

        # Convert the NumPy array to an OpenCV image object
        cv2_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        # Extract text from the roi image using EasyOCR
        results = reader.readtext(cv2_image) # results will be a list containing multiple tuples corresponding to the number of words that were extracted. Each tuple has 3 elements - first element is a list of text box coordinates [x.y], 2nd element is the extracted text, and 3rd element is the model confidence level

        # Check if text was extracted
        if results:
            # Retrieve all extracted text from results and join into a single string, seperated by new line
            text = '\n'.join(text[1] for text in results)
            # Set response as extracted text
            response = {'extracted_text': text}
        else:
            # Set response as feedback message if no text detected
            response = {'extracted_text': 'No text detected in region'}
    
    # Error handling for text extraction
    except:
        # Set response as error message if error occured
        response = {'extracted_text': 'An error occured during text extraction.'}

    # Return response to client
    return jsonify(response)


if __name__ == '__main__':
    app.run()