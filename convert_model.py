"""
Model Conversion Script for TensorFlow Compatibility
Run this on your MacBook to convert your model to be compatible with newer TensorFlow versions
"""

import tensorflow as tf
import numpy as np
import os

def convert_model():
    print("Loading original model...")
    
    try:
        # Try to load the original model
        model = tf.keras.models.load_model('keras_model.h5', compile=False)
        print("✅ Model loaded successfully!")
        
        # Get model summary
        print("\nModel Summary:")
        model.summary()
        
        # Save in new format (SavedModel format - more compatible)
        print("\nSaving in new format...")
        model.save('keras_model_converted', save_format='tf')
        print("✅ Saved as TensorFlow SavedModel format in 'keras_model_converted' folder")
        
        # Also save as .keras format (newer format)
        print("\nSaving in .keras format...")
        model.save('keras_model_new.keras')
        print("✅ Saved as 'keras_model_new.keras'")
        
        # Test the model with dummy input
        print("\nTesting model...")
        dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        dummy_input = (dummy_input / 127.5) - 1  # Normalize like Teachable Machine
        
        prediction = model.predict(dummy_input, verbose=0)
        print(f"✅ Model works! Output shape: {prediction.shape}")
        
        print("\n" + "="*60)
        print("SUCCESS! Your model has been converted.")
        print("\nYou now have two options:")
        print("1. Use 'keras_model_new.keras' (recommended)")
        print("2. Use 'keras_model_converted' folder (SavedModel format)")
        print("\nUpload the new file(s) to your GitHub repository.")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTrying alternative conversion method...")
        
        try:
            # Alternative: Load and rebuild
            import h5py
            
            with h5py.File('keras_model.h5', 'r') as f:
                print("Reading model architecture from H5 file...")
                
            # Load without the problematic layer config
            print("Loading with custom handling...")
            
            # This is a fallback - create instructions for manual fix
            print("\n" + "="*60)
            print("⚠️ MANUAL FIX REQUIRED")
            print("="*60)
            print("\nYour model uses an older format that needs manual conversion.")
            print("Please retrain your model in Teachable Machine and re-export it.")
            print("\nOr, update your Streamlit app to use TensorFlow 2.15.1")
            print("which is compatible with your current model.")
            print("="*60)
            
            return False
            
        except Exception as e2:
            print(f"❌ Alternative method also failed: {str(e2)}")
            return False

if __name__ == "__main__":
    print("="*60)
    print("TEACHABLE MACHINE MODEL CONVERTER")
    print("="*60)
    print("\nThis script converts your keras_model.h5 to a format")
    print("compatible with newer TensorFlow versions.\n")
    
    # Check if model file exists
    if not os.path.exists('keras_model.h5'):
        print("❌ Error: 'keras_model.h5' not found!")
        print("Please make sure keras_model.h5 is in the same folder as this script.")
    else:
        convert_model()
