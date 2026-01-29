import os
# --- CRITICAL FIX: Force Legacy Keras ---
# This must be set before importing tensorflow to handle Teachable Machine models
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Set page title
st.set_page_config(page_title="Keras Image Classifier", layout="centered")

# --- Load the Model ---
@st.cache_resource
def load_my_model():
    # This specific fix handles the "groups" error common in Teachable Machine models
    # when loading in newer TensorFlow versions
    custom_objects = {
        "DepthwiseConv2D": lambda **kwargs: tf.keras.layers.DepthwiseConv2D(
            **{k: v for k, v in kwargs.items() if k != "groups"}
        )
    }
    
    try:
        model = tf.keras.models.load_model(
            'keras_model.h5', 
            compile=False, 
            custom_objects=custom_objects
        )
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load model outside the main flow to ensure it's cached properly
model = load_my_model()

# --- UI Layout ---
st.title("🤖 AI Image Classifier")
st.write("Upload an image, and the model will predict what it is.")

if model is None:
    st.error("Model failed to load. Please check your 'keras_model.h5' file.")
else:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        
        st.write("### Classifying...")
        
        # --- Preprocessing ---
        # Most Keras models (like Teachable Machine) expect 224x224 images
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        
        # Convert image to numpy array and normalize
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        
        # Create the payload for the model (batch size 1, 224, 224, 3)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # --- Prediction ---
        prediction = model.predict(data)
        index = np.argmax(prediction)
        
        # Check if you have a labels.txt file, otherwise show raw index
        try:
            with open("labels.txt", "r") as f:
                class_names = f.readlines()
            prediction_label = class_names[index].strip()
            confidence_score = prediction[0][index]
            st.success(f"Prediction: **{prediction_label}**")
            st.info(f"Confidence Score: {confidence_score:.2%}")
        except FileNotFoundError:
            st.warning("Prediction complete, but 'labels.txt' was not found.")
            st.write(f"Raw Prediction Index: {index}")
            st.write(f"Full Prediction Array: {prediction}")
