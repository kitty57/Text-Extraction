import streamlit as st
import cv2
from PIL import Image
import numpy as np
import requests
import easyocr

# Function to extract text from image
def extract_text(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    extracted_text = '\n'.join([res[1] for res in result])
    return extracted_text

# Streamlit app
def main():
    st.set_page_config(page_title="Text Extraction App", layout="wide")
    st.title("Text Extraction from Images")
    st.markdown("---")
    st.write("Upload an image or provide an image URL to extract text.")
    st.markdown("---")

    # Upload image or provide image URL
    option = st.radio("Select input type:", ("Upload Image", "Image URL"))

    # Image processing
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"], help="Supported formats: JPG, PNG, JPEG")
        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file))
            st.image(image, caption='Uploaded Image', use_column_width=True)
            if st.button("Extract Text"):
                with st.spinner('Extracting text...'):
                    extracted_text = extract_text(image)
                    if extracted_text:
                        st.subheader("Extracted Text:")
                        st.write(extracted_text)
                    else:
                        st.error("No text detected in the image.")
    elif option == "Image URL":
        image_url = st.text_input("Enter image URL:")
        if st.button("Extract Text"):
            if image_url:
                with st.spinner('Extracting text...'):
                    try:
                        image = np.array(Image.open(requests.get(image_url, stream=True).raw))
                        st.image(image, caption='Image from URL', use_column_width=True)
                        extracted_text = extract_text(image)
                        if extracted_text:
                            st.subheader("Extracted Text:")
                            st.write(extracted_text)
                        else:
                            st.error("No text detected in the image.")
                    except Exception as e:
                        st.error(f"Error loading image from URL: {e}")

if __name__ == "__main__":
    main()
