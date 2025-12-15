#!/usr/bin/env python3
"""
MODEL TRAINING SCRIPT: Train Random Forest with SMOTE
Requires data from 01_create_data.py
"""

import pandas as pd
import numpy as np
import joblib
import os
import sys
from config import DATA_PATH, MODEL_PATH, SCALER_PATH

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

print("=" * 60)
print("🧠 TRAINING AI MODEL")
print("=" * 60)

def load_data():
    """
    Load training data
    """
    if not os.path.exists(DATA_PATH):
        print(f"❌ No data found at {DATA_PATH}")
        print("💡 Run: python scripts/01_create_data.py first!")
        return None
    
    df = pd.read_csv(DATA_PATH)
    print(f"📊 Loaded {len(df)} training samples")
    return df

def train_model(df):
    """
    Train Random Forest Classifier with SMOTE
    """
    print("\n🔧 Preparing data for training...")
    
    # Define features for prediction
    feature_columns = [
        'first_contentful_paint',
        'largest_contentful_paint',
        'cumulative_layout_shift',
        'total_blocking_time',
        'speed_index',
        'total_byte_weight',
        'meta_description_exists',
        'title_length',
        'seo_score',
        'accessibility_score'
    ]
    
    # Use only available features
    available_features = [f for f in feature_columns if f in df.columns]
    print(f"✅ Using {len(available_features)} features: {available_features}")
    
    X = df[available_features].fillna(0)
    
    # Use performance_category as target
    if 'performance_category' not in df.columns:
        print("❌ Target column 'performance_category' not found in data")
        return None
    
    y = df['performance_category']
    
    # Show class distribution
    print("\n📈 Class Distribution (Target):")
    print(y.value_counts())
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📐 Data split:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    
    # Scale features
    print("\n⚖️ Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Handle class imbalance with SMOTE
    print("🔄 Applying SMOTE for balanced classes...")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train_scaled, y_train)
    
    print("📊 After SMOTE distribution:")
    print(pd.Series(y_resampled).value_counts())
    
    # Train Random Forest
    print("\n🌲 Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,      # Number of trees
        max_depth=10,          # Maximum depth of trees
        min_samples_split=5,   # Minimum samples to split a node
        min_samples_leaf=2,    # Minimum samples at a leaf node
        random_state=42,       # For reproducible results
        class_weight='balanced', # Handle class imbalance
        n_jobs=-1              # Use all CPU cores
    )
    
    model.fit(X_resampled, y_resampled)
    
    # Evaluate model
    print("\n" + "=" * 60)
    print("📊 MODEL EVALUATION")
    print("=" * 60)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {accuracy:.3f}")
    
    # Detailed classification report
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': available_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🏆 Top 5 Most Important Features:")
    print(feature_importance.head())
    
    # Save model and scaler
    print("\n💾 Saving trained model...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(available_features, 'data/model/features.pkl')
    
    print(f"✅ Model saved: {MODEL_PATH}")
    print(f"✅ Scaler saved: {SCALER_PATH}")
    print(f"✅ Features saved: data/model/features.pkl")
    
    return model, scaler, available_features

def test_model_predictions(model, scaler, features):
    """
    Test the trained model with sample predictions
    """
    print("\n" + "=" * 60)
    print("🧪 TEST PREDICTIONS")
    print("=" * 60)
    
    # Create sample test cases
    test_cases = [
        {
            'name': 'Fast E-commerce Site',
            'features': [800, 1500, 0.05, 100, 1800, 2000, 1, 50, 85, 88]
        },
        {
            'name': 'Slow Blog',
            'features': [3500, 5000, 0.3, 500, 4500, 6000, 0, 120, 45, 50]
        },
        {
            'name': 'Average Corporate Site',
            'features': [2000, 3000, 0.15, 250, 3200, 3500, 1, 70, 68, 72]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        # Prepare features in correct order
        feature_values = test['features'][:len(features)]
        
        # Scale features
        features_scaled = scaler.transform([feature_values])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        print(f"\n{i}. {test['name']}:")
        print(f"   🎯 Predicted: {prediction}")
        print(f"   📊 Confidence: {max(probabilities):.1%}")
        
        # Show all probabilities
        for class_name, prob in zip(model.classes_, probabilities):
            print(f"      {class_name}: {prob:.1%}")

def main():
    """
    Main training pipeline
    """
    # Step 1: Load data
    df = load_data()
    if df is None:
        return
    
    # Step 2: Train model
    result = train_model(df)
    if result is None:
        return
    
    model, scaler, features = result
    
    # Step 3: Test predictions
    test_model_predictions(model, scaler, features)
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("\n🎯 Next Steps:")
    print("1. Test predictions: python scripts/03_analyze.py")
    print("2. Launch web app: streamlit run app.py")
    print("3. Collect more real data and retrain later")

if __name__ == "__main__":
    main()