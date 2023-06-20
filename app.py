from flask import Flask, render_template, request
import cv2
import easyocr
import numpy as np

app = Flask(__name__)

# Specify the languages to be recognized
languages = ['en']  # English

# Initialize the EasyOCR reader
reader = easyocr.Reader(languages)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()