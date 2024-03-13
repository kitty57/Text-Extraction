import cv2
import streamlit as st
import pytesseract
from PIL import Image
import requests
from io import BytesIO

# Install Tesseract OCR
st.info("Installing Tesseract OCR. This may take a minute.")
!sudo apt install tesseract-ocr

st.title("Image Text Extraction")

# Function to process image and extract text
def process_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Perform OCR
    config = ('-l eng --oem 1 --psm 3')
    try:
        extracted_text = pytesseract.image_to_string(thresh, config=config)
        return extracted_text
    except Exception as e:
        return str(e)

# File uploader for image upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Text input for image URL
image_url = st.text_input("Enter image URL")

# Process image
if uploaded_file is not None:
    # Read image from file uploader
    image = Image.open(uploaded_file)
    img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    extracted_text = process_image(img_array)
    st.write("Extracted Text:", extracted_text)
elif image_url != "":
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        st.image(image, caption='Image from URL', use_column_width=True)
        extracted_text = process_image(img_array)
        st.write("Extracted Text:", extracted_text)
    except Exception as e:
        st.error(f"Error loading image from URL: {e}")
