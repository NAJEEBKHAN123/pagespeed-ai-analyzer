# train_with_balanced.py
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("=" * 60)
print("🧠 TRAINING WITH BALANCED DATASET")
print("=" * 60)

# Load the NEW balanced data
df = pd.read_csv('data/raw/balanced_data.csv')
print(f"📊 Loaded {len(df)} BALANCED samples")

print("\n✅ PERFECTLY BALANCED DISTRIBUTION:")
print(df['performance_category'].value_counts())

# Select features
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

# Train model
print("\n🌲 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model trained!")
print(f"📈 Accuracy: {accuracy:.1%}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': available_features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🏆 Top 5 Most Important Features:")
print(feature_importance.head())

# Save model (OVERWRITE old one)
os.makedirs('data/model', exist_ok=True)
joblib.dump(model, 'data/model/model.pkl')
joblib.dump(scaler, 'data/model/scaler.pkl')
joblib.dump(available_features, 'data/model/features.pkl')

print(f"\n💾 Model saved to data/model/")
print("   (Overwrote previous model with balanced data)")

# Test predictions
print("\n🧪 Testing predictions with sample websites:")

test_cases = [
    {'name': 'Excellent Site', 'perf': 95, 'fcp': 800, 'lcp': 1500},
    {'name': 'Good Site', 'perf': 80, 'fcp': 2000, 'lcp': 2800},
    {'name': 'Needs Improvement Site', 'perf': 60, 'fcp': 3000, 'lcp': 4000},
    {'name': 'Poor Site', 'perf': 40, 'fcp': 3800, 'lcp': 5500}
]

for test in test_cases:
    # Create realistic feature vector
    features_vec = [
        test['fcp'],  # first_contentful_paint
        test['lcp'],  # largest_contentful_paint
        np.random.uniform(0, 0.2),  # cumulative_layout_shift
        np.random.uniform(50, 300),  # total_blocking_time
        np.random.uniform(1000, 3000),  # total_byte_weight
        1,  # meta_description_exists
        np.random.randint(30, 70),  # title_length
        test['perf'] * np.random.uniform(0.9, 1.1),  # seo_score
        test['perf'] * np.random.uniform(0.9, 1.1)  # accessibility_score
    ]
    
    features_scaled = scaler.transform([features_vec])
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    print(f"\n🌐 {test['name']}:")
    print(f"   🎯 Prediction: {prediction}")
    print(f"   📊 Confidence: {max(probabilities):.1%}")

print("\n" + "=" * 60)
print("✅ BALANCED MODEL TRAINING COMPLETE!")
print("=" * 60)
print("\n🚀 Now run: streamlit run app.py")