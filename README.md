# Emotion Detection Streamlit App

A web application that uses a Teachable Machine model to detect emotions (happy, sad, frustrated) from images, with GitHub integration for storing prediction data.

## Features

- 📸 Upload images for emotion detection
- 🎯 Real-time prediction with confidence scores
- 📊 Visual probability distribution for all emotions
- 💾 Optional GitHub integration to store prediction data
- 🎨 Clean and intuitive user interface

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A GitHub account (for data storage feature)

### 2. Installation

```bash
# Clone or download this repository
cd your-project-folder

# Install dependencies
pip install -r requirements.txt
```

### 3. Add Your Model Files

Place these files in the same directory as `app.py`:
- `keras_model.h5` (your Teachable Machine model)
- `labels.txt` (emotion labels)

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## GitHub Integration Setup

To enable data storage in GitHub:

### 1. Create a GitHub Repository

```bash
# Create a new repository on GitHub (e.g., "emotion-data")
# You can do this via GitHub website or CLI
```

### 2. Generate a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Streamlit Emotion App")
4. Select scope: `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### 3. Configure in the App

1. Run the Streamlit app
2. In the sidebar, enter:
   - Your GitHub Personal Access Token
   - Your repository name (format: `username/repo-name`)
3. Check "Save predictions to GitHub"
4. After each prediction, click "Save Prediction to GitHub"

## Data Storage Format

Predictions are stored in `predictions.json` in your GitHub repository:

```json
[
  {
    "timestamp": "2026-01-29T10:30:45.123456",
    "predicted_emotion": "happy",
    "confidence": 0.95,
    "all_probabilities": {
      "happy": 0.95,
      "sad": 0.03,
      "frustrated": 0.02
    }
  }
]
```

## Deploying to Streamlit Cloud

### 1. Prepare Your Repository

Create a GitHub repository with these files:
```
your-repo/
├── app.py
├── requirements.txt
├── keras_model.h5
├── labels.txt
└── README.md
```

### 2. Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Deploy"

### 3. Configure Secrets (Optional)

For automatic GitHub integration, add secrets in Streamlit Cloud:

1. Go to your app settings
2. Click "Secrets"
3. Add:
```toml
github_token = "your_github_token_here"
repo_name = "username/repo-name"
```

Then modify the app to read from `st.secrets` instead of user input.

## Project Structure

```
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── keras_model.h5         # Teachable Machine model
├── labels.txt             # Emotion labels
└── README.md              # This file
```

## Usage Tips

1. **Image Quality**: Use clear, well-lit images for best results
2. **Face Detection**: Ensure faces are clearly visible in the uploaded images
3. **Data Privacy**: Be mindful of what images you upload and store
4. **Token Security**: Never commit your GitHub token to a public repository

## Troubleshooting

### Model Loading Error
- Ensure `keras_model.h5` and `labels.txt` are in the same directory as `app.py`
- Check that TensorFlow is properly installed

### GitHub Integration Issues
- Verify your personal access token has `repo` scope
- Check repository name format: `username/repository-name`
- Ensure the repository exists and you have write access

### Deployment Issues
- If deploying to Streamlit Cloud, ensure all files are pushed to GitHub
- Check that `requirements.txt` includes all necessary dependencies
- Model file size: GitHub has a 100MB file size limit; use Git LFS for larger files

## Advanced: Using Git LFS for Large Model Files

If your `keras_model.h5` is larger than 100MB:

```bash
# Install Git LFS
git lfs install

# Track the model file
git lfs track "*.h5"

# Add and commit
git add .gitattributes
git add keras_model.h5
git commit -m "Add model with Git LFS"
git push
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!

## Acknowledgments

- Model created with [Teachable Machine](https://teachablemachine.withgoogle.com/)
- Built with [Streamlit](https://streamlit.io/)
- Powered by [TensorFlow](https://www.tensorflow.org/)
