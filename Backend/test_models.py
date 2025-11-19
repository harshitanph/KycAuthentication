"""
Test script to load and verify pickle model files
"""
import pickle
import os
import sys

def test_model_loading():
    """Test loading all model files"""
    print("=" * 60)
    print("Testing Model File Loading")
    print("=" * 60)
    
    files_to_test = {
        "Model": "best_model.pkl",
        "Scaler": "scaler.pkl",
        "Feature Selector": "feature_selector.pkl"
    }
    
    results = {}
    
    for name, filename in files_to_test.items():
        print(f"\n📦 Testing {name} ({filename}):")
        
        # Check if file exists
        if not os.path.exists(filename):
            print(f"   ❌ File not found: {filename}")
            results[name] = False
            continue
        
        # Check file size
        file_size = os.path.getsize(filename)
        print(f"   📄 File size: {file_size} bytes")
        
        if file_size == 0:
            print(f"   ❌ File is empty!")
            results[name] = False
            continue
        
        # Try to load the pickle file
        try:
            with open(filename, 'rb') as f:
                obj = pickle.load(f)
            
            print(f"   ✅ Loaded successfully!")
            print(f"   📊 Type: {type(obj)}")
            
            # Try to get more info about the object
            if hasattr(obj, '__class__'):
                print(f"   📋 Class: {obj.__class__.__name__}")
            
            # Check for common ML model attributes
            if hasattr(obj, 'predict'):
                print(f"   ✅ Has predict() method")
            if hasattr(obj, 'predict_proba'):
                print(f"   ✅ Has predict_proba() method")
            if hasattr(obj, 'transform'):
                print(f"   ✅ Has transform() method")
            if hasattr(obj, 'fit'):
                print(f"   ✅ Has fit() method")
            
            results[name] = True
            
        except Exception as e:
            print(f"   ❌ Error loading: {e}")
            print(f"   ❌ Error type: {type(e).__name__}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_loaded = True
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
        if not success:
            all_loaded = False
    
    if all_loaded:
        print("\n✅ All model files loaded successfully!")
        print("   Models are ready to use in the backend.")
    else:
        print("\n⚠️  Some model files failed to load.")
        print("   Check the errors above and fix the issues.")
    
    return all_loaded

if __name__ == "__main__":
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = test_model_loading()
    sys.exit(0 if success else 1)

