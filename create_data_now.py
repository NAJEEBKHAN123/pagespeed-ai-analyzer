# create_data_now.py
import pandas as pd
import numpy as np
import os

print("=" * 60)
print("📊 CREATING TRAINING DATA NOW")
print("=" * 60)

# Create 300 sample websites
np.random.seed(42)

data = []
for i in range(300):
    # Generate realistic performance scores
    website_type = np.random.choice(['ecommerce', 'blog', 'corporate', 'portfolio', 'news'])
    
    if website_type == 'ecommerce':
        performance = np.random.uniform(40, 95)
    elif website_type == 'blog':
        performance = np.random.uniform(60, 98)
    else:
        performance = np.random.uniform(50, 92)
    
    # Core metrics
    fcp = np.random.uniform(500, 4000)  # ms
    lcp = np.random.uniform(1000, 6000)  # ms
    cls = np.random.uniform(0, 0.4)
    tbt = np.random.uniform(0, 600)  # ms
    page_size = np.random.uniform(500, 8000)  # KB
    
    # Adjust performance based on metrics
    performance = max(0, min(100, 
        performance - (fcp/200 + lcp/300 + cls*50 + tbt/30 + page_size/1000)
    ))
    
    # Other scores
    seo = max(0, min(100, performance * np.random.uniform(0.8, 1.2)))
    accessibility = max(0, min(100, performance * np.random.uniform(0.9, 1.1)))
    best_practices = max(0, min(100, performance * np.random.uniform(0.85, 1.15)))
    
    # Create category
    if performance >= 90:
        category = 'Excellent'
    elif performance >= 75:
        category = 'Good'
    elif performance >= 50:
        category = 'Needs Improvement'
    else:
        category = 'Poor'
    
    data.append({
        'url': f'https://example{i}.com',
        'website_type': website_type,
        'device_type': np.random.choice(['mobile', 'desktop']),
        'timestamp': f'2024-01-{str(i%30+1).zfill(2)} 10:00:00',
        
        # Scores
        'performance_score': round(performance, 1),
        'seo_score': round(seo, 1),
        'accessibility_score': round(accessibility, 1),
        'best_practices_score': round(best_practices, 1),
        
        # Core Web Vitals
        'first_contentful_paint': round(fcp, 0),
        'largest_contentful_paint': round(lcp, 0),
        'cumulative_layout_shift': round(cls, 3),
        'total_blocking_time': round(tbt, 0),
        'speed_index': round(np.random.uniform(1000, 5000), 0),
        'time_to_interactive': round(np.random.uniform(2000, 8000), 0),
        
        # Resource metrics
        'total_byte_weight': round(page_size, 0),
        
        # SEO metrics
        'meta_description_exists': np.random.choice([0, 1], p=[0.3, 0.7]),
        'title_length': np.random.randint(10, 120),
        'h1_count': np.random.randint(1, 5),
        
        # Accessibility
        'image_alt_exists': np.random.choice([0, 1], p=[0.2, 0.8]),
        
        # Target for prediction
        'performance_category': category
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_path = "data/raw/sample_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ Created {len(df)} sample records")
print(f"📁 Saved to: {output_path}")

# Show sample
print("\n📋 Sample of data (first 5 rows):")
print(df[['url', 'performance_score', 'seo_score', 'performance_category']].head())

# Show statistics
print("\n📊 Data Statistics:")
print(f"Performance Score: {df['performance_score'].mean():.1f} average")
print(f"SEO Score: {df['seo_score'].mean():.1f} average")
print("\nCategory Distribution:")
print(df['performance_category'].value_counts())

print("\n" + "=" * 60)
print("✅ DATA CREATION COMPLETE!")
print("=" * 60)
print("\n🎯 Next: Run training script")
print("   python scripts/02_train_model.py")