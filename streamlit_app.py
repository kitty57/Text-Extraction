import streamlit as st
import cv2
import pytesseract
from PIL import Image
import numpy as np
import requests

# Function to extract text from image
def extract_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    config = ('-l eng --oem 1 --psm 3')
    try:
        extracted_text = pytesseract.image_to_string(thresh, config=config)
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {e}"

# Streamlit app
def main():
    st.set_page_config(page_title="Text Extraction App", layout="centered")
    st.title("Text Extraction from Images")
    st.markdown("---")
    st.write("Upload an image or provide an image URL to extract text.")
    st.markdown("---")

    # Upload image or provide image URL
    option = st.radio("Select input type:", ("Upload Image", "Image URL"))

    # Image processing
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            extracted_text = extract_text(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            if extracted_text:
                st.subheader("Extracted Text:")
                st.write(extracted_text)
            else:
                st.warning("No text detected in the image.")
    elif option == "Image URL":
        image_url = st.text_input("Enter image URL:")
        if st.button("Extract Text"):
            if image_url:
                try:
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    st.image(image, caption='Image from URL', use_column_width=True)
                    extracted_text = extract_text(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
                    if extracted_text:
                        st.subheader("Extracted Text:")
                        st.write(extracted_text)
                    else:
                        st.warning("No text detected in the image.")
                except Exception as e:
                    st.error(f"Error loading image from URL: {e}")

if __name__ == "__main__":
    main()
