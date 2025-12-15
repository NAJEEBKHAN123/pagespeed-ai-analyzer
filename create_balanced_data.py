# create_balanced_data.py
import pandas as pd
import numpy as np
import os

print("=" * 60)
print("📊 CREATING PROPER BALANCED DATASET")
print("=" * 60)

np.random.seed(42)
n_samples = 400  # 100 per category

data = []
categories = ['Poor', 'Needs Improvement', 'Good', 'Excellent']

for category in categories:
    for _ in range(n_samples // 4):  # 100 each
        if category == 'Excellent':
            perf = np.random.uniform(90, 100)
            fcp = np.random.uniform(500, 1500)
            lcp = np.random.uniform(1000, 2500)
        elif category == 'Good':
            perf = np.random.uniform(75, 90)
            fcp = np.random.uniform(1500, 2500)
            lcp = np.random.uniform(2500, 3500)
        elif category == 'Needs Improvement':
            perf = np.random.uniform(50, 75)
            fcp = np.random.uniform(2500, 3500)
            lcp = np.random.uniform(3500, 4500)
        else:  # Poor
            perf = np.random.uniform(30, 50)
            fcp = np.random.uniform(3500, 4000)
            lcp = np.random.uniform(4500, 6000)
        
        data.append({
            'performance_score': round(perf, 1),
            'seo_score': round(perf * np.random.uniform(0.8, 1.2), 1),
            'accessibility_score': round(perf * np.random.uniform(0.9, 1.1), 1),
            'first_contentful_paint': round(fcp, 0),
            'largest_contentful_paint': round(lcp, 0),
            'cumulative_layout_shift': round(np.random.uniform(0, 0.3), 3),
            'total_blocking_time': round(np.random.uniform(0, 500), 0),
            'total_byte_weight': round(np.random.uniform(500, 5000), 0),
            'meta_description_exists': np.random.choice([0, 1], p=[0.2, 0.8]),
            'title_length': np.random.randint(10, 80),
            'performance_category': category
        })

df = pd.DataFrame(data)
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/balanced_data.csv', index=False)

print(f"✅ Created {len(df)} balanced samples")
print("\n📊 Category Distribution:")
print(df['performance_category'].value_counts())
print("\n📁 Saved to: data/raw/balanced_data.csv")