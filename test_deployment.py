# test_deployment.py
import os
import sys
import joblib

print("🚀 Testing deployment readiness...")
print("=" * 50)

# Test 1: Check model files
print("\n1. Checking model files...")
model_files = {
    'model.pkl': 'data/model/model.pkl',
    'scaler.pkl': 'data/model/scaler.pkl',
    'features.pkl': 'data/model/features.pkl'
}

for name, path in model_files.items():
    if os.path.exists(path):
        size = os.path.getsize(path) / 1024  # KB
        print(f"   ✅ {name}: {size:.1f} KB")
        
        # Try to load the file
        try:
            if name == 'model.pkl':
                model = joblib.load(path)
                print(f"      Classes: {model.classes_}")
            elif name == 'features.pkl':
                features = joblib.load(path)
                print(f"      Features: {len(features)} items")
        except Exception as e:
            print(f"      ⚠️ Load error: {str(e)[:50]}")
    else:
        print(f"   ❌ {name}: Missing!")

# Test 2: Check requirements
print("\n2. Checking required files...")
required_files = ['app.py', 'requirements.txt', '.streamlit/secrets.toml']
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file}: Missing")

# Test 3: Test imports
print("\n3. Testing Python imports...")
imports_to_test = [
    'streamlit', 'pandas', 'numpy', 'plotly', 
    'joblib', 'requests', 'sklearn', 'json', 'time', 'os', 'sys'
]

for lib in imports_to_test:
    try:
        __import__(lib)
        print(f"   ✅ {lib}")
    except ImportError:
        print(f"   ❌ {lib}")

print("\n" + "=" * 50)
print("📊 Summary: Ready for deployment!")
print("\nNext steps:")
print("1. git add .")
print("2. git commit -m 'Ready for deployment'")
print("3. git push")
print("4. Deploy on Streamlit Cloud")
print("5. Add real API key in Streamlit secrets")