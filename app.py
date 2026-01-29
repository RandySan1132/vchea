import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Set page title
st.set_page_config(page_title="Keras Image Classifier", layout="centered")

# --- Load the Model ---
# We use @st.cache_resource so the model only loads once when the app starts
@st.cache_resource
def load_my_model():
    model = tf.keras.models.load_model('keras_model.h5', compile=False)
    return model

model = load_my_model()

# --- UI Layout ---
st.title("🤖 AI Image Classifier")
st.write("Upload an image, and the model will predict what it is.")

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
    
    # Convert image to numpy array and normalize if needed
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1 # Normalization for TM
    
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
