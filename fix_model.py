"""
Fix Teachable Machine Model - Remove 'groups' parameter
This script fixes the compatibility issue with newer TensorFlow versions
"""

import h5py
import json
import shutil
import os

def fix_model(input_file='keras_model.h5', output_file='keras_model_fixed.h5'):
    """
    Fix the Teachable Machine model by removing the 'groups' parameter
    from DepthwiseConv2D layer configurations
    """
    
    # Create a backup
    backup_file = input_file + '.backup'
    if not os.path.exists(backup_file):
        shutil.copy2(input_file, backup_file)
        print(f"✅ Created backup: {backup_file}")
    
    print(f"Opening {input_file}...")
    
    # Open the HDF5 file
    with h5py.File(input_file, 'r') as f_in:
        # Check if model_config exists
        if 'model_config' not in f_in.attrs:
            print("❌ No model_config found in the file")
            return False
        
        # Get the model config
        model_config_str = f_in.attrs['model_config']
        if isinstance(model_config_str, bytes):
            model_config_str = model_config_str.decode('utf-8')
        
        model_config = json.loads(model_config_str)
        
        print("Scanning layers for 'groups' parameter...")
        
        # Track if we made any changes
        fixed_count = 0
        
        # Recursively search and fix DepthwiseConv2D layers
        def fix_layer_config(obj):
            nonlocal fixed_count
            if isinstance(obj, dict):
                # Check if this is a DepthwiseConv2D layer config
                if obj.get('class_name') == 'DepthwiseConv2D':
                    if 'config' in obj and 'groups' in obj['config']:
                        print(f"  Found DepthwiseConv2D layer: {obj['config'].get('name', 'unnamed')}")
                        print(f"    Removing 'groups' parameter (value: {obj['config']['groups']})")
                        del obj['config']['groups']
                        fixed_count += 1
                
                # Recursively process nested dictionaries
                for key, value in obj.items():
                    fix_layer_config(value)
            
            elif isinstance(obj, list):
                # Recursively process lists
                for item in obj:
                    fix_layer_config(item)
        
        # Fix the config
        fix_layer_config(model_config)
        
        if fixed_count == 0:
            print("ℹ️  No 'groups' parameters found. Model may already be fixed.")
            return True
        
        print(f"\n✅ Fixed {fixed_count} DepthwiseConv2D layer(s)")
        
        # Convert back to JSON string
        fixed_config_str = json.dumps(model_config)
        
        # Create new file with fixed config
        print(f"\nCreating fixed model: {output_file}...")
        
        shutil.copy2(input_file, output_file)
        
        with h5py.File(output_file, 'r+') as f_out:
            # Update the model config
            f_out.attrs['model_config'] = fixed_config_str
            print("✅ Updated model configuration")
        
        print(f"\n{'='*60}")
        print("SUCCESS! Your model has been fixed!")
        print(f"{'='*60}")
        print(f"\nOriginal file: {input_file}")
        print(f"Backup file:   {backup_file}")
        print(f"Fixed file:    {output_file}")
        print(f"\n📤 Upload '{output_file}' to your GitHub repository")
        print("   and rename it to 'keras_model.h5' (replace the old one)")
        print(f"{'='*60}\n")
        
        return True

if __name__ == "__main__":
    print("="*60)
    print("TEACHABLE MACHINE MODEL FIX UTILITY")
    print("="*60)
    print("\nThis script removes the 'groups' parameter that causes")
    print("compatibility issues with newer TensorFlow versions.\n")
    
    if not os.path.exists('keras_model.h5'):
        print("❌ Error: 'keras_model.h5' not found!")
        print("Please make sure the model file is in the same folder.")
    else:
        success = fix_model()
        
        if success:
            print("\n🎉 Done! Your model is now compatible with TensorFlow 2.16+")
            print("\nNext steps:")
            print("1. Upload 'keras_model_fixed.h5' to GitHub")
            print("2. Rename it to 'keras_model.h5' (replace old file)")
            print("3. Your Streamlit app will work! ✨")
