"""
Fix and convert pickle models to joblib format
This script converts the pickle files to joblib-compatible format
"""
import os
import pickle
import joblib

def fix_model_file(input_file, output_file):
    """Convert pickle file to joblib format"""
    print(f"\n📦 Converting {input_file} → {output_file}")
    
    if not os.path.exists(input_file):
        print(f"   ❌ File not found: {input_file}")
        return False
    
    try:
        # Load using pickle
        print(f"   📥 Loading {input_file}...")
        with open(input_file, 'rb') as f:
            data = pickle.load(f)
        
        print(f"   ✅ Loaded successfully! Type: {type(data)}")
        
        # Save using joblib
        print(f"   💾 Saving to {output_file}...")
        joblib.dump(data, output_file)
        
        print(f"   ✅ Successfully converted to {output_file}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_file(filename):
    """Test if a model file can be loaded"""
    print(f"\n🧪 Testing {filename}...")
    
    if not os.path.exists(filename):
        print(f"   ❌ File not found")
        return False
    
    try:
        model = joblib.load(filename)
        print(f"   ✅ Loaded successfully!")
        print(f"   📊 Type: {type(model)}")
        print(f"   📋 Class: {model.__class__.__name__}")
        return True
    except Exception as e:
        print(f"   ❌ Error loading: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Fixing Model Files - Converting to Joblib Format")
    print("=" * 60)
    
    # Files to convert
    files_to_fix = [
        ("best_model.pkl", "best_model_fixed.pkl"),
        ("scaler.pkl", "scaler_fixed.pkl"),
        ("feature_selector.pkl", "feature_selector_fixed.pkl")
    ]
    
    results = {}
    
    # Convert files
    for input_file, output_file in files_to_fix:
        success = fix_model_file(input_file, output_file)
        results[input_file] = success
    
    # Test converted files
    print("\n" + "=" * 60)
    print("Testing Converted Files")
    print("=" * 60)
    
    test_results = {}
    for _, output_file in files_to_fix:
        success = test_model_file(output_file)
        test_results[output_file] = success
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_success = True
    for input_file, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {input_file}")
        if not success:
            all_success = False
    
    print("\nTest Results:")
    for output_file, success in test_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {output_file}")
        if not success:
            all_success = False
    
    if all_success:
        print("\n✅ All models fixed and tested successfully!")
        print("\nNext steps:")
        print("1. Update backend/main.py to use joblib.load()")
        print("2. Update model file names to *_fixed.pkl")
        print("3. Restart the backend server")
    else:
        print("\n⚠️  Some files failed. Check errors above.")
    
    print("=" * 60)

