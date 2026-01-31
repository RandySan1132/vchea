import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
import os

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Potato Leaf Disease Classifier", page_icon="🥔")

# Define the file paths
MODEL_PATH = 'keras_model.h5'  # <--- Now pointing to your Keras file
LABELS_PATH = 'labels.txt'

# --- 2. HELPER FUNCTIONS ---

@st.cache_resource
def load_labels(labels_file):
    """
    Parses the labels.txt file from Teachable Machine.
    """
    labels = []
    if not os.path.exists(labels_file):
        st.error(f"Labels file not found at {labels_file}")
        return ["Unknown"]
        
    try:
        with open(labels_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                # Teachable Machine often exports "0 ClassName"
                # This splits it to get just "ClassName"
                parts = line.strip().split(' ', 1)
                if len(parts) > 1:
                    labels.append(parts[1])
                else:
                    labels.append(parts[0])
    except Exception as e:
        st.error(f"Error loading labels: {e}")
        return ["Healthy", "Blight"] # Fallback
    return labels

@st.cache_resource
def load_model(model_path):
    """
    Loads the Keras model (h5).
    """
    if not os.path.exists(model_path):
        st.warning(f"Model file not found at {model_path}. Please upload 'keras_model.h5'.")
        return None
    
    try:
        # compile=False is recommended for inference as it's faster and safer
        model = tf.keras.models.load_model(model_path, compile=False)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def process_image_and_predict(image, model):
    """
    Preprocesses the image for Teachable Machine and returns the prediction.
    TM requires: 224x224, normalized to -1 to 1.
    """
    # 1. Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # 2. Resize the image to 224x224
    # ImageOps.fit crops from the center to maintain aspect ratio
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # 3. Turn the image into a numpy array
    image_array = np.asarray(image)

    # 4. Normalize the image (Teachable Machine standard)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # 5. Load the image into the array
    data[0] = normalized_image_array

    # 6. Run the inference
    prediction = model.predict(data)
    return prediction

# --- 3. MAIN APP INTERFACE ---

st.title("🥔 Potato Leaf Disease Detector")
st.write("Upload an image of a potato leaf to detect if it is **Healthy** or has **Blight**.")

# Load resources
class_names = load_labels(LABELS_PATH)
model = load_model(MODEL_PATH)

# File Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Leaf', use_container_width=True)
    
    if st.button("Analyze Leaf"):
        if model is None:
            st.error("Model not loaded. Please ensure 'keras_model.h5' is in the directory.")
        else:
            with st.spinner('Analyzing...'):
                # Get Prediction
                prediction = process_image_and_predict(image, model)
                
                # Find the index of the highest confidence score
                index = np.argmax(prediction)
                class_name = class_names[index]
                confidence_score = prediction[0][index]
                
                # Display Results
                st.write("---")
                
                # Logic for success/error messages based on label content
                if "Healthy" in class_name:
                    st.success(f"**Result:** {class_name}")
                else:
                    st.error(f"**Result:** {class_name}")
                
                st.info(f"**Confidence:** {confidence_score * 100:.2f}%")
