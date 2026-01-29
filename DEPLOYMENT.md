# Deployment Guide

This guide will help you deploy your Emotion Detection app to GitHub and Streamlit Cloud.

## Step 1: Prepare Your GitHub Repository

### 1.1 Create a New Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the '+' icon in the top right → "New repository"
3. Name it (e.g., "emotion-detection-app")
4. Choose "Public" or "Private"
5. Click "Create repository"

### 1.2 Upload Your Files

You'll need to upload these files to your repository:

```
your-repo/
├── app.py
├── requirements.txt
├── keras_model.h5
├── labels.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

**Option A: Using GitHub Web Interface**

1. On your repository page, click "Add file" → "Upload files"
2. Drag and drop all the files (or use the file chooser)
3. Add a commit message: "Initial commit"
4. Click "Commit changes"

**Option B: Using Git Command Line**

```bash
# Navigate to your project folder
cd /path/to/your/project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/emotion-detection-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note about Large Files**: If your `keras_model.h5` is larger than 100MB, you'll need to use Git LFS:

```bash
# Install Git LFS (one-time setup)
git lfs install

# Track .h5 files
git lfs track "*.h5"

# Add the .gitattributes file
git add .gitattributes

# Now add and commit normally
git add keras_model.h5
git commit -m "Add model file with LFS"
git push
```

## Step 2: Create a Data Storage Repository (Optional)

If you want to store prediction data:

1. Create another GitHub repository (e.g., "emotion-data")
2. This repository will store `predictions.json`
3. You can make it private if you want to keep data confidential

## Step 3: Generate GitHub Personal Access Token

1. Go to GitHub → Settings (top right, click your profile picture)
2. Scroll down to "Developer settings" (left sidebar, near bottom)
3. Click "Personal access tokens" → "Tokens (classic)"
4. Click "Generate new token (classic)"
5. Configure the token:
   - **Note**: "Streamlit Emotion App"
   - **Expiration**: Choose duration (90 days, 1 year, or no expiration)
   - **Scopes**: Check `repo` (this gives full control of repositories)
6. Click "Generate token"
7. **IMPORTANT**: Copy the token immediately and save it securely (you won't see it again!)

## Step 4: Deploy to Streamlit Cloud

### 4.1 Sign Up / Sign In

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit

### 4.2 Deploy Your App

1. Click "New app" button
2. Fill in the deployment form:
   - **Repository**: Select your repository (e.g., `yourusername/emotion-detection-app`)
   - **Branch**: `main` (or whatever your main branch is called)
   - **Main file path**: `app.py`
3. Click "Advanced settings" (optional):
   - Python version: 3.9 or 3.10 recommended
4. Click "Deploy!"

### 4.3 Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- This takes 2-5 minutes typically
- You'll see logs showing the installation progress
- Once complete, your app will be live!

## Step 5: Configure GitHub Integration in Your App

### Option A: Manual Entry (Easiest)

1. Open your deployed Streamlit app
2. In the sidebar, enter:
   - **GitHub Personal Access Token**: Paste the token you generated
   - **Repository**: Enter `yourusername/emotion-data` (or your data repo name)
3. Check "Save predictions to GitHub"
4. Upload an image and click "Save Prediction to GitHub" to test

### Option B: Using Streamlit Secrets (More Secure)

1. In Streamlit Cloud, go to your app dashboard
2. Click on your app → Click the "⋮" menu → "Settings"
3. Go to "Secrets" section
4. Add your secrets in TOML format:

```toml
github_token = "ghp_your_token_here"
repo_name = "yourusername/emotion-data"
```

5. Modify `app.py` to read from secrets (I can help with this if needed)

## Step 6: Test Your App

1. Visit your app URL (e.g., `https://yourusername-emotion-detection-app.streamlit.app`)
2. Upload a test image
3. Verify the emotion prediction works
4. If GitHub integration is enabled, test saving a prediction
5. Check your data repository for the `predictions.json` file

## Updating Your App

When you want to update the app:

```bash
# Make changes to your files
# Commit changes
git add .
git commit -m "Update description"
git push

# Streamlit Cloud will automatically redeploy!
```

## Troubleshooting

### App Won't Deploy
- Check the logs in Streamlit Cloud for errors
- Verify `requirements.txt` has all dependencies
- Make sure all files are in the repository

### Model File Too Large
- Use Git LFS (see Step 1)
- Consider model compression or quantization

### GitHub Integration Not Working
- Verify token has `repo` scope
- Check repository name format: `username/repo-name`
- Ensure the repository exists

### App is Slow
- Consider using a smaller model
- Optimize image preprocessing
- Cache model loading (already done in the code)

## Sharing Your App

Once deployed, you can share your app URL with anyone:
- Public apps: Anyone can access
- Private repos: Only you can access unless you add collaborators

Example URL format:
```
https://yourusername-emotion-detection-app.streamlit.app
```

## Cost

- **Streamlit Cloud**: Free tier includes 1 app, 1GB resources
- **GitHub**: Free for public repos, free private repos with limits
- **No credit card required** for basic usage!

## Security Best Practices

1. **Never commit tokens to Git**: Use `.gitignore` or Streamlit Secrets
2. **Use token expiration**: Set tokens to expire after a reasonable period
3. **Limit token scope**: Only give `repo` access, nothing more
4. **Monitor usage**: Regularly check your GitHub repository access logs
5. **Rotate tokens**: Regenerate tokens periodically

## Getting Help

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Forum**: https://discuss.streamlit.io
- **GitHub Docs**: https://docs.github.com

Good luck with your deployment! 🚀
