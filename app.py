import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime
import json
import os
from github import Github
import io

# Page configuration
st.set_page_config(
    page_title="Emotion Detector",
    page_icon="😊",
    layout="centered"
)

# Load the model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model(
            "keras_model.h5",
            compile=False,
            custom_objects={
                "DepthwiseConv2D": lambda **kwargs: tf.keras.layers.DepthwiseConv2D(
                    **{k: v for k, v in kwargs.items() if k != "groups"}
                )
            }
        )
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load labels
@st.cache_data
def load_labels():
    with open('labels.txt', 'r') as f:
        labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
    return labels

# GitHub integration for data storage
class GitHubDataStore:
    def __init__(self, token, repo_name, file_path='predictions.json'):
        self.token = token
        self.repo_name = repo_name
        self.file_path = file_path
        self.github = Github(token) if token else None
        
    def save_prediction(self, prediction_data):
        if not self.github:
            st.warning("GitHub token not configured. Data will not be saved.")
            return False
            
        try:
            repo = self.github.get_repo(self.repo_name)
            
            # Try to get existing file
            try:
                file = repo.get_contents(self.file_path)
                existing_data = json.loads(file.decoded_content.decode())
                existing_data.append(prediction_data)
                
                # Update file
                repo.update_file(
                    self.file_path,
                    f"Add prediction at {prediction_data['timestamp']}",
                    json.dumps(existing_data, indent=2),
                    file.sha
                )
            except:
                # File doesn't exist, create it
                repo.create_file(
                    self.file_path,
                    f"Initialize predictions file",
                    json.dumps([prediction_data], indent=2)
                )
            
            return True
        except Exception as e:
            st.error(f"Error saving to GitHub: {str(e)}")
            return False

# Preprocess image for the model
def preprocess_image(image):
    # Resize image to 224x224 (Teachable Machine default)
    image = image.resize((224, 224))
    
    # Convert to array
    image_array = np.array(image)
    
    # Normalize the image (Teachable Machine uses normalization)
    normalized_image = (image_array.astype(np.float32) / 127.5) - 1
    
    # Reshape to add batch dimension
    reshaped = normalized_image.reshape((1, 224, 224, 3))
    
    return reshaped

# Main app
def main():
    st.title("😊 Emotion Detection App")
    st.markdown("Upload an image to detect the emotion: **Happy**, **Sad**, or **Frustrated**")
    
    # Sidebar for GitHub configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("### GitHub Data Storage")
        
        github_token = st.text_input(
            "GitHub Personal Access Token",
            type="password",
            help="Generate a token at: https://github.com/settings/tokens"
        )
        
        repo_name = st.text_input(
            "Repository (username/repo-name)",
            help="e.g., yourusername/emotion-data"
        )
        
        save_to_github = st.checkbox("Save predictions to GitHub", value=False)
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This app uses a Teachable Machine model to classify emotions from images.")
    
    # Initialize GitHub data store
    github_store = None
    if save_to_github and github_token and repo_name:
        github_store = GitHubDataStore(github_token, repo_name)
    
    # Load model and labels
    try:
        model = load_model()
        labels = load_labels()
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Make sure 'keras_model.h5' and 'labels.txt' are in the same directory as this app.")
        return
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image to detect the emotion"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption='Uploaded Image', use_container_width=True)
        
        with col2:
            with st.spinner('Analyzing emotion...'):
                # Preprocess and predict
                processed_image = preprocess_image(image)
                predictions = model.predict(processed_image, verbose=0)
                predicted_class = np.argmax(predictions[0])
                confidence = predictions[0][predicted_class]
                
                # Display results
                st.markdown("### 🎯 Prediction Results")
                st.success(f"**Detected Emotion:** {labels[predicted_class].upper()}")
                st.metric("Confidence", f"{confidence * 100:.2f}%")
                
                # Show all probabilities
                st.markdown("### 📊 All Probabilities")
                for i, label in enumerate(labels):
                    prob = predictions[0][i]
                    st.progress(float(prob), text=f"{label.capitalize()}: {prob * 100:.1f}%")
        
        # Save to GitHub if enabled
        if save_to_github and github_store:
            if st.button("💾 Save Prediction to GitHub"):
                prediction_data = {
                    'timestamp': datetime.now().isoformat(),
                    'predicted_emotion': labels[predicted_class],
                    'confidence': float(confidence),
                    'all_probabilities': {
                        labels[i]: float(predictions[0][i]) for i in range(len(labels))
                    }
                }
                
                with st.spinner('Saving to GitHub...'):
                    if github_store.save_prediction(prediction_data):
                        st.success("✅ Prediction saved to GitHub successfully!")
                    else:
                        st.error("❌ Failed to save prediction to GitHub")
    
    # Example section
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        1. **Upload an Image**: Click on the upload button and select an image
        2. **View Results**: The app will display the detected emotion and confidence score
        3. **Configure GitHub** (Optional):
           - Create a GitHub Personal Access Token with 'repo' scope
           - Enter your token and repository name in the sidebar
           - Enable "Save predictions to GitHub"
           - Click "Save Prediction to GitHub" button after each prediction
        
        **Note**: Your predictions will be stored in a `predictions.json` file in your GitHub repository.
        """)

if __name__ == "__main__":
    main()
