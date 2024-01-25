# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 02:02:58 2024

@author: DELL
"""

import streamlit as st
from PIL import Image
import pytesseract
import re
# Function to perform OCR on the image and return the text
def perform_ocr(image_data):
    try:
        img = Image.open(image_data)
        text_result = pytesseract.image_to_string(img)
        return text_result.strip()  # Strip leading and trailing whitespaces
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def clean_string(input_value):
    if isinstance(input_value, list):
        # If the input is a list, join its elements into a single string
        input_string = ' '.join(map(str, input_value))
    else:
        # If the input is already a string, use it as is
        input_string = str(input_value)

    # Use regular expression to keep only alphanumeric, '@', and '-'
    cleaned_string = re.sub(r'[^\w\s@+\-.]', '', input_string)
    return cleaned_string

# Function to parse the extracted text and return segments
def parse_text(text):
    lines = text.split('\n')

    # Initialize variables for each segment
    name, designation, address, phone_number, company_email, website = "", "", "", "", "", ""

    # Check if there are enough lines to extract the desired segments
    if len(lines) >= 1:
            name=lines[:1]
    if len(lines) >= 1:
            designation= lines[1:3]
    if len(lines) >= 3:
            address= lines[3:6]    
    if len(lines) >= 1:
            phone_number= lines[6:7]         
    if len(lines) >= 1:
             company_email= lines[8:9]        
    if len(lines) >= 1:
             website= lines[9:]    
    name=clean_string(name)
    designation=clean_string(designation)
    address=clean_string(address)
    phone_number=clean_string(phone_number)
    company_email=clean_string(company_email)
    website=clean_string(website)
    return name, designation, address, phone_number, company_email, website

# Main Streamlit app
def main():
    # Set a background image
    import base64
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('C:/Users/DELL/Downloads/Grey_BG.jpg') 

    st.markdown("<h1 style='color: black;'>Image OCR App</h1>", unsafe_allow_html=True)
    # Use Markdown to set the color of the selectbox label to black
    st.markdown("<label style='color: black; font-weight: bold;'>Select the option</label>", unsafe_allow_html=True)

# Create the selectbox
    selection = st.selectbox("", ['Camera', 'Upload your Image'])
    col1, col2 = st.columns(2)
    data = None
    text = None

    with col1:
        if selection == 'Camera':
            st.markdown("<label style='color: black; font-weight: bold;'>Scan the Image</label>", unsafe_allow_html=True)
            data = st.camera_input('')
        elif selection == 'Upload your Image':
            st.markdown("<label style='color: black; font-weight: bold;'>Upload Image</label>", unsafe_allow_html=True)
            data = st.file_uploader('', type=['png', 'jpg', 'jpeg'])

    with col2:
        if data:
            st.image(data)
            text = perform_ocr(data)

    st.markdown("----")

    if text:
        col4,col5 = st.columns(2)
        
        with col4:
            st.markdown("<h1 style='color: black;'>User Interaction</h1>", unsafe_allow_html=True)
            name, designation, address, phone_number, company_email, personal_email = parse_text(text)

            # Display individual text inputs for each segment
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Name</label>", unsafe_allow_html=True)
            st.text_input('',value=name,key='name')
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Designation</label>", unsafe_allow_html=True)
            st.text_input('',value=designation,key='designation')
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Address</label>", unsafe_allow_html=True)
            st.text_input('',value=address,key='address')
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Phone Number</label>", unsafe_allow_html=True)
            st.text_input('',value=phone_number,key='phone_number')
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Company Email</label>", unsafe_allow_html=True)
            st.text_input('',value=company_email,key='company_email')
            st.markdown("<label style='color: black; font-style: italic;font-weight: bold;'>Website</label>", unsafe_allow_html=True)
            st.text_input('',value=personal_email,key='website')

if __name__ == "__main__":
    main()
