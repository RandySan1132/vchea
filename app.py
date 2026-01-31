import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import os

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Potato Leaf Disease Classifier", page_icon="🥔")

# Define the file paths
MODEL_PATH = 'model.pth'  # <--- REPLACE WITH YOUR ACTUAL MODEL FILENAME
LABELS_PATH = 'labels.txt'

# --- 2. HELPER FUNCTIONS ---

@st.cache_resource
def load_labels(labels_file):
    """
    Parses the labels.txt file.
    Handles the specific format: '0 Healthy Potato Leaves'
    """
    labels = {}
    try:
        with open(labels_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                # Remove brackets and metadata if present, like 
                clean_line = line.strip()
                if not clean_line: continue
                
                # specific parsing for "0 Label Name" format
                parts = clean_line.split(' ', 1)
                
                # If the first part is metadata like , skip to the number
                if parts[0].startswith('['):
                    # Try to find the first digit in the line
                    import re
                    match = re.search(r'(\d+)\s+(.*)', clean_line)
                    if match:
                        idx = int(match.group(1))
                        name = match.group(2)
                        labels[idx] = name
                else:
                    # Standard "0 Label" format
                    if len(parts) == 2 and parts[0].isdigit():
                        labels[int(parts[0])] = parts[1]
    except Exception as e:
        st.error(f"Error loading labels: {e}")
        return {0: "Healthy", 1: "Blight"} # Fallback
    return labels

@st.cache_resource
def load_model(model_path):
    """
    Loads the PyTorch model. 
    Ensure you export your model to CPU mode before saving if deploying to a non-GPU machine.
    """
    if not os.path.exists(model_path):
        st.warning(f"Model file not found at {model_path}. Please upload it.")
        return None
    
    try:
        # Load the entire model
        model = torch.load(model_path, map_location=torch.device('cpu'))
        model.eval()
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def process_image(image):
    """
    Preprocesses the image to match the model's training input.
    Adjust resize/normalize values to match your specific training configuration.
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)), # Standard size, change if your model used 256 or others
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0) # Add batch dimension

# --- 3. MAIN APP INTERFACE ---

st.title("🥔 Potato Leaf Disease Detector")
st.write("Upload an image of a potato leaf to detect if it is **Healthy** or has **Blight**.")

# Load resources
labels_map = load_labels(LABELS_PATH)
model = load_model(MODEL_PATH)

# File Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Leaf', use_container_width=True)
    
    if st.button("Analyze Leaf"):
        if model is None:
            st.error("Model not loaded. Please ensure 'model.pth' is in the directory.")
        else:
            with st.spinner('Analyzing...'):
                # Prediction Logic
                input_tensor = process_image(image)
                with torch.no_grad():
                    outputs = model(input_tensor)
                    _, predicted = torch.max(outputs, 1)
                    prediction_index = predicted.item()
                
                # Get label name
                result_label = labels_map.get(prediction_index, "Unknown")
                
                # Display Results
                if "Healthy" in result_label:
                    st.success(f"**Prediction:** {result_label} ✅")
                else:
                    st.error(f"**Prediction:** {result_label} ⚠️")
