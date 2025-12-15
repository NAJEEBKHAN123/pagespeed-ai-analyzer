#!/usr/bin/env python3
"""
SETUP SCRIPT: Verify API key and create necessary folders
"""

import os
import sys
from config import API_KEY
import requests

print("=" * 60)
print("🔧 SETUP AND VERIFICATION")
print("=" * 60)

# Check API key
print(f"🔑 API Key: {'✅ Found' if API_KEY else '❌ Missing'}")

if API_KEY:
    # Test API key
    print("\n🧪 Testing API key...")
    test_url = "https://google.com"
    
    try:
        response = requests.get(
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
            params={'url': test_url, 'key': API_KEY},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API Key is working!")
        else:
            print(f"❌ API Key error: {response.status_code}")
            print("Check your API key at: https://console.cloud.google.com/apis/credentials")
    
    except Exception as e:
        print(f"❌ Connection error: {e}")

# Create necessary directories
print("\n📁 Creating directories...")
directories = ['data/raw', 'data/model', 'logs']
for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    print(f"  Created: {dir_path}")

print("\n" + "=" * 60)
print("✅ SETUP COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Run: python scripts/01_create_data.py")
print("2. Run: python scripts/02_train_model.py")
print("3. Run: streamlit run app.py")