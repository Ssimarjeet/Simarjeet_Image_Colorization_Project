import numpy as np
import streamlit as st
from PIL import Image
from pathlib import Path
import torch
from deoldify import device
from deoldify.visualize import *
import tempfile

# Define path to the models directory
root_folder = Path(r"C:\Users\simarjeet singh\OneDrive\Desktop\deoldify_models")  # Update this path

# Load the colorizer model (use the correct path to your models folder)
colorizer = get_image_colorizer(artistic=True, root_folder=root_folder)

# Function to colorize using DeOldify
def colorize_image(img):
    # Convert PIL image to RGB and resize to model input size
    img = img.convert("RGB")
    img = img.resize((512, 512))  # DeOldify uses 512x512 input size

    # Create a temporary file to save the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_filename = temp_file.name
        img.save(temp_filename)  # Save the image to the temporary file
        
    # Now use the temporary file's path with DeOldify colorizer
    colorized_image = colorizer.get_transformed_image(temp_filename)
    
    # Optionally, remove the temporary file after use (cleanup)
    Path(temp_filename).unlink()

    return colorized_image

##########################################################################################################
# Streamlit code to upload and display images
st.write("""
          # Colorize your Black and white image
          """
          )

st.write("This is an app to colorize your B&W images using DeOldify.")

# File upload section
file = st.sidebar.file_uploader("Please upload an image file", type=["jpg", "png"])

if file is None:
    st.text("You haven't uploaded an image file")
else:
    # Open image with PIL and convert to numpy array
    image = Image.open(file)
    img = np.array(image)

    # Display original image
    st.text("Your original image")
    st.image(image, use_container_width=True)

    # Colorize and display the result
    st.text("Your colorized image")
    colorized = colorize_image(image)  # Colorize the uploaded image
    st.image(colorized, use_container_width=True)

    print("done!")
