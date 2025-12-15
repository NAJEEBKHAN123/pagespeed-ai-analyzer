#!/usr/bin/env python3
"""
TEST SCRIPT: Test the trained model on any website
"""

import sys
import os
import joblib
import requests
import json
from config import API_KEY, MODEL_PATH, SCALER_PATH

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("🔍 TEST MODEL WITH REAL WEBSITE")
print("=" * 60)

def get_real_time_data(url):
    """
    Get real-time data from PageSpeed API
    """
    print(f"\n🌐 Fetching real-time data for: {url}")
    
    try:
        response = requests.get(
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
            params={
                'url': url,
                'key': API_KEY,
                'strategy': 'mobile',
                'category': ['PERFORMANCE', 'SEO', 'ACCESSIBILITY']
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract metrics
            metrics = {}
            categories = data['lighthouseResult']['categories']
            
            metrics['performance_score'] = categories.get('performance', {}).get('score', 0) * 100
            metrics['seo_score'] = categories.get('seo', {}).get('score', 0) * 100
            metrics['accessibility_score'] = categories.get('accessibility', {}).get('score', 0) * 100
            
            audits = data['lighthouseResult']['audits']
            
            metrics['first_contentful_paint'] = audits.get('first-contentful-paint', {}).get('numericValue', 0)
            metrics['largest_contentful_paint'] = audits.get('largest-contentful-paint', {}).get('numericValue', 0)
            metrics['cumulative_layout_shift'] = audits.get('cumulative-layout-shift', {}).get('numericValue', 0)
            metrics['total_blocking_time'] = audits.get('total-blocking-time', {}).get('numericValue', 0)
            metrics['speed_index'] = audits.get('speed-index', {}).get('numericValue', 0)
            metrics['total_byte_weight'] = audits.get('total-byte-weight', {}).get('numericValue', 0) / 1024
            
            # SEO metrics
            metrics['meta_description_exists'] = 1 if audits.get('meta-description', {}).get('score', 0) == 1 else 0
            
            # Title length
            title_audit = audits.get('document-title', {})
            if title_audit.get('details', {}).get('items'):
                metrics['title_length'] = len(title_audit['details']['items'][0].get('title', ''))
            else:
                metrics['title_length'] = 0
            
            print("✅ Real-time data fetched successfully!")
            return metrics
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """
    Main testing function
    """
    # Test URL
    test_url = "https://google.com"
    
    # Get real-time data
    real_metrics = get_real_time_data(test_url)
    
    if real_metrics:
        print("\n📊 Real-time Metrics:")
        print(f"  Performance Score: {real_metrics.get('performance_score', 0):.1f}")
        print(f"  SEO Score: {real_metrics.get('seo_score', 0):.1f}")
        print(f"  First Contentful Paint: {real_metrics.get('first_contentful_paint', 0):.0f} ms")
        print(f"  Largest Contentful Paint: {real_metrics.get('largest_contentful_paint', 0):.0f} ms")
        
        # Load trained model
        try:
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)
            features = joblib.load('data/model/features.pkl')
            
            print(f"\n✅ Loaded trained model with {len(features)} features")
            
            # Prepare features for prediction
            feature_values = []
            for feature in features:
                feature_values.append(real_metrics.get(feature, 0))
            
            # Scale features
            features_scaled = scaler.transform([feature_values])
            
            # Make prediction
            prediction = model.predict(features_scaled)[0]
            probabilities = model.predict_proba(features_scaled)[0]
            
            print("\n" + "=" * 60)
            print("🤖 AI PREDICTION")
            print("=" * 60)
            
            print(f"\n🎯 Predicted Performance Category: {prediction}")
            print(f"📊 Confidence: {max(probabilities):.1%}")
            
            print("\n📈 All Probabilities:")
            for class_name, prob in zip(model.classes_, probabilities):
                print(f"  {class_name}: {prob:.1%}")
            
        except Exception as e:
            print(f"\n❌ Error loading model: {e}")
            print("💡 Run: python scripts/02_train_model.py first!")
    
    else:
        print("\n❌ Could not fetch real-time data")

if __name__ == "__main__":
    main()