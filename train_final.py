# train_final.py
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("=" * 60)
print("🧠 FINAL MODEL TRAINING - SIMPLE VERSION")
print("=" * 60)

# Load your existing data
df = pd.read_csv('data/raw/sample_data.csv')
print(f"📊 Loaded {len(df)} samples")

# CRITICAL: Your data is severely imbalanced
print("\n⚠️  CRITICAL WARNING: DATA IMBALANCE DETECTED")
print("Your data has only 2 categories:")
print(df['performance_category'].value_counts())
print("\nThis model will be heavily biased toward 'Poor' predictions.")
print("Consider creating a more balanced dataset for production use.")

# Select features (only those that exist)
features = [
    'first_contentful_paint', 'largest_contentful_paint',
    'cumulative_layout_shift', 'total_blocking_time',
    'total_byte_weight', 'meta_description_exists',
    'title_length', 'seo_score', 'accessibility_score'
]

available_features = [f for f in features if f in df.columns]
X = df[available_features].values
y = df['performance_category'].values

print(f"\n🔧 Using {len(available_features)} features")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"📐 Training: {len(X_train)} samples, Testing: {len(X_test)} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model with class_weight to handle imbalance
print("\n🌲 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    class_weight='balanced',  # Helps with imbalance
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model trained!")
print(f"📈 Accuracy: {accuracy:.1%}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# Save everything
os.makedirs('data/model', exist_ok=True)
joblib.dump(model, 'data/model/model.pkl')
joblib.dump(scaler, 'data/model/scaler.pkl')
joblib.dump(available_features, 'data/model/features.pkl')

print(f"\n💾 Model saved to data/model/")
print(f"   - model.pkl")
print(f"   - scaler.pkl")
print(f"   - features.pkl")

# Quick test
print("\n🧪 Sample prediction (average values):")
sample = [df[f].mean() for f in available_features]
sample_scaled = scaler.transform([sample])
prediction = model.predict(sample_scaled)[0]
print(f"   Prediction: {prediction}")

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE! Ready for Streamlit.")
print("=" * 60)