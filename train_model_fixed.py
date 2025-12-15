# train_model_fixed.py
import pandas as pd
import numpy as np
import joblib
import os
import sys

print("=" * 60)
print("🧠 TRAINING AI MODEL WITH FIXED DATA PATH")
print("=" * 60)

# Try different possible data paths
possible_paths = [
    "data/raw/sample_data.csv",
    "data/raw/websites.csv",
    "data/sample_data.csv",
    "sample_data.csv"
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        print(f"✅ Found data at: {path}")
        break

if not data_path:
    print("❌ No data found! Creating sample data...")
    
    # Create sample data immediately
    np.random.seed(42)
    data = []
    for i in range(200):
        performance = np.random.uniform(30, 100)
        
        if performance >= 90:
            category = 'Excellent'
        elif performance >= 75:
            category = 'Good'
        elif performance >= 50:
            category = 'Needs Improvement'
        else:
            category = 'Poor'
        
        data.append({
            'performance_score': performance,
            'seo_score': np.random.uniform(40, 100),
            'accessibility_score': np.random.uniform(50, 100),
            'first_contentful_paint': np.random.uniform(500, 4000),
            'largest_contentful_paint': np.random.uniform(1000, 6000),
            'cumulative_layout_shift': np.random.uniform(0, 0.4),
            'total_blocking_time': np.random.uniform(0, 600),
            'total_byte_weight': np.random.uniform(500, 8000),
            'meta_description_exists': np.random.choice([0, 1]),
            'title_length': np.random.randint(10, 100),
            'performance_category': category
        })
    
    df = pd.DataFrame(data)
    data_path = "data/raw/sample_data.csv"
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    df.to_csv(data_path, index=False)
    print(f"✅ Created {len(df)} sample records at {data_path}")

# Load data
print(f"\n📊 Loading data from {data_path}...")
df = pd.read_csv(data_path)
print(f"✅ Loaded {len(df)} training samples")

# Show column names to debug
print(f"\n🔍 Columns in data: {list(df.columns)}")

# Check if we have the target column
if 'performance_category' not in df.columns:
    print("❌ 'performance_category' column not found!")
    print("Creating it from performance_score...")
    
    # Create category from performance_score
    df['performance_category'] = pd.cut(
        df['performance_score'],
        bins=[0, 50, 75, 90, 101],
        labels=['Poor', 'Needs Improvement', 'Good', 'Excellent']
    )

# Define features
features = [
    'first_contentful_paint',
    'largest_contentful_paint', 
    'cumulative_layout_shift',
    'total_blocking_time',
    'total_byte_weight',
    'meta_description_exists',
    'title_length',
    'seo_score',
    'accessibility_score'
]

# Check which features exist
available_features = []
for feature in features:
    if feature in df.columns:
        available_features.append(feature)
    else:
        print(f"⚠️ Feature '{feature}' not found in data")

print(f"\n🔧 Using {len(available_features)} available features:")
print(f"   {available_features}")

if len(available_features) < 3:
    print("❌ Not enough features for training!")
    exit(1)

# Prepare X and y
X = df[available_features].values
y = df['performance_category'].values

print(f"\n🎯 Target classes: {np.unique(y)}")
print(f"📈 Class distribution:")
for cls in np.unique(y):
    count = np.sum(y == cls)
    print(f"   {cls}: {count} samples ({count/len(y):.1%})")

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📐 Data split:")
print(f"   Training: {len(X_train)} samples")
print(f"   Testing:  {len(X_test)} samples")

# Scale features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Handle class imbalance
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train_scaled, y_train)

print(f"\n🔄 After SMOTE:")
print(f"   Training: {len(X_resampled)} samples")

# Train Random Forest
from sklearn.ensemble import RandomForestClassifier
print("\n🌲 Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)

model.fit(X_resampled, y_resampled)

# Evaluate
from sklearn.metrics import accuracy_score, classification_report
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model trained!")
print(f"📈 Accuracy: {accuracy:.1%}")

print("\n📋 Detailed Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': available_features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🏆 Feature Importance:")
print(feature_importance)

# Save model
print("\n💾 Saving model...")
os.makedirs('data/model', exist_ok=True)

joblib.dump(model, 'data/model/model.pkl')
joblib.dump(scaler, 'data/model/scaler.pkl')
joblib.dump(available_features, 'data/model/features.pkl')

print(f"✅ Model saved: data/model/model.pkl")
print(f"✅ Scaler saved: data/model/scaler.pkl")
print(f"✅ Features saved: data/model/features.pkl")

# Test prediction
print("\n🧪 Testing prediction...")
sample_features = []
for feature in available_features:
    # Get average value for each feature
    sample_features.append(df[feature].mean())

sample_scaled = scaler.transform([sample_features])
prediction = model.predict(sample_scaled)[0]
probabilities = model.predict_proba(sample_scaled)[0]

print(f"🎯 Prediction for average website: {prediction}")
print(f"📊 Probabilities:")
for cls, prob in zip(model.classes_, probabilities):
    print(f"   {cls}: {prob:.1%}")

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print("\n🚀 Now run: streamlit run app.py")