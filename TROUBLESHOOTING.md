# Streamlit Cloud Deployment Troubleshooting

## Error: "Error installing requirements"

This error typically occurs due to package version conflicts or memory issues during installation.

### Solution 1: Use the Updated requirements.txt

I've updated your `requirements.txt` file with these changes:
- Changed `tensorflow==2.15.0` to `tensorflow-cpu==2.15.0` (lighter, cloud-friendly)
- Added `protobuf==3.20.3` to prevent conflicts

**Action Required:**
1. Delete your current `requirements.txt` from GitHub
2. Upload the new `requirements.txt` I've provided
3. Streamlit Cloud will automatically redeploy

### Solution 2: Try Minimal Requirements (requirements-minimal.txt)

If Solution 1 doesn't work, try using `requirements-minimal.txt`:
1. Rename `requirements-minimal.txt` to `requirements.txt`
2. Push to GitHub
3. This uses the latest compatible versions automatically

### Solution 3: Use Python 3.9

Streamlit Cloud deployment settings:
1. In Streamlit Cloud, click your app → Settings
2. Click "Advanced settings"
3. Set Python version to `3.9`
4. Save and redeploy

### Solution 4: Increase Memory

Sometimes the error is due to memory limits during installation:
1. This typically auto-resolves after a few minutes
2. Try redeploying by clicking "Reboot" in Streamlit Cloud
3. Or make a dummy commit to trigger redeploy:
   ```bash
   git commit --allow-empty -m "Trigger redeploy"
   git push
   ```

## Alternative: Use TensorFlow Lite

If you continue having issues, convert your model to TensorFlow Lite (smaller, faster):

### Convert Model Script:
```python
import tensorflow as tf

# Load your model
model = tf.keras.models.load_model('keras_model.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

Then update requirements.txt to:
```
streamlit
tensorflow-lite
Pillow
numpy
PyGithub
```

And modify app.py to use TFLite interpreter instead.

## Common Error Messages & Fixes

### "ERROR: Could not find a version that satisfies the requirement tensorflow"
**Fix**: Use `tensorflow-cpu` instead of `tensorflow`

### "ERROR: No matching distribution found for tensorflow==2.15.0"
**Fix**: Remove version pin, use just `tensorflow-cpu` 

### "Package installation failed after multiple attempts"
**Fix**: Wait 5 minutes and try "Reboot" in Streamlit Cloud

### "Memory limit exceeded"
**Fix**: 
- Use `tensorflow-cpu` instead of `tensorflow`
- Or upgrade to Streamlit Cloud paid tier
- Or deploy on alternative platform (Heroku, Railway, etc.)

## Checking Deployment Logs

To see detailed error messages:
1. Go to Streamlit Cloud
2. Click on your app
3. Click "Manage app" 
4. View the terminal logs
5. Look for specific error messages

Common issues to look for:
- Package not found
- Version conflicts
- Memory errors
- Timeout errors

## Quick Fix Checklist

✅ Use `tensorflow-cpu` instead of `tensorflow`  
✅ Add `protobuf<4.0.0` to requirements  
✅ Set Python version to 3.9 in Advanced Settings  
✅ Ensure all files are committed to GitHub  
✅ Try "Reboot" in Streamlit Cloud  
✅ Wait 5-10 minutes for installation to complete  

## Still Not Working?

### Option A: Deploy Locally First
Test that everything works locally before deploying:
```bash
pip install -r requirements.txt
streamlit run app.py
```
If it works locally, the issue is with cloud deployment settings.

### Option B: Alternative Deployment Platforms

If Streamlit Cloud continues to fail, try:

1. **Hugging Face Spaces** (Free, ML-friendly)
   - More generous resource limits
   - Better TensorFlow support
   - Visit: https://huggingface.co/spaces

2. **Railway** (Free tier available)
   - Easy deployment
   - Better control over resources
   - Visit: https://railway.app

3. **Render** (Free tier available)
   - Simple deployment
   - Good for ML apps
   - Visit: https://render.com

### Option C: Use Google Colab

Create a Colab notebook version:
- Upload to Google Colab
- Run Streamlit with ngrok for public URL
- No deployment needed!

## Need More Help?

1. **Check Streamlit logs**: Look for specific error messages
2. **Streamlit Forum**: https://discuss.streamlit.io
3. **GitHub Issues**: Check if others have similar issues
4. **Try requirements-minimal.txt**: Sometimes less is more!

## Updated Files Available

I've created these updated files for you:
- ✅ `requirements.txt` - Updated with tensorflow-cpu
- ✅ `requirements-minimal.txt` - Minimal versions (backup option)

Replace your current requirements.txt with the updated version and try again!
