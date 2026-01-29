# Quick Start Guide

Get your Emotion Detection app running in 5 minutes!

## 🚀 Local Setup (Quick Test)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Test It Out
- Open http://localhost:8501 in your browser
- Upload an image
- See the emotion prediction!

## 📤 Deploy to Streamlit Cloud (15 minutes)

### 1. Create GitHub Repository
- Go to github.com
- Click "+" → "New repository"
- Name it (e.g., "emotion-detector")
- Create repository

### 2. Upload Files
Upload these files to your repository:
- ✅ app.py
- ✅ requirements.txt
- ✅ keras_model.h5
- ✅ labels.txt
- ✅ README.md
- ✅ .gitignore

### 3. Deploy
- Go to share.streamlit.io
- Sign in with GitHub
- Click "New app"
- Select your repository
- Set main file: `app.py`
- Click "Deploy"

### 4. Done! 🎉
Your app is now live and shareable!

## 💾 Enable GitHub Data Storage (Optional)

### 1. Create Data Repository
- Create another GitHub repo (e.g., "emotion-data")

### 2. Generate Token
- GitHub Settings → Developer settings → Personal access tokens
- Generate new token (classic)
- Select `repo` scope
- Copy the token

### 3. Configure in App
- Open your deployed app
- Enter token and repo name in sidebar
- Enable "Save predictions to GitHub"

## 📚 Need More Help?

See the detailed guides:
- **README.md** - Full documentation
- **DEPLOYMENT.md** - Step-by-step deployment
- **Streamlit Docs** - https://docs.streamlit.io

## 🐛 Common Issues

**Model won't load?**
→ Make sure keras_model.h5 and labels.txt are in the same folder as app.py

**GitHub integration not working?**
→ Check your token has 'repo' scope and repository name is correct format (username/repo-name)

**App won't deploy?**
→ Check Streamlit Cloud logs for errors, verify all files are in repository

## 🎯 Test Images

Try with images containing faces showing different emotions:
- 😊 Happy faces
- 😢 Sad faces  
- 😤 Frustrated faces

The model works best with clear, well-lit images!
