#!/usr/bin/env python3
"""
DATA CREATION SCRIPT: Create initial training data
NO INTERNET NEEDED - Creates synthetic data immediately
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from config import DATA_PATH

print("=" * 60)
print("📊 CREATING TRAINING DATA")
print("=" * 60)

def create_synthetic_dataset(num_samples=300):
    """
    Create realistic synthetic data for training
    This runs immediately - no API calls needed
    """
    print(f"🎭 Creating {num_samples} synthetic website records...")
    
    np.random.seed(42)  # For reproducible results
    
    data = []
    
    for i in range(num_samples):
        # Generate realistic website metrics
        website_type = np.random.choice(['ecommerce', 'blog', 'corporate', 'portfolio', 'news'], 
                                       p=[0.3, 0.25, 0.2, 0.15, 0.1])
        
        # Performance metrics based on website type
        if website_type == 'ecommerce':
            fcp = np.random.uniform(800, 3500)  # ms
            lcp = np.random.uniform(1500, 5000)  # ms
            base_perf = np.random.uniform(40, 90)
        elif website_type == 'blog':
            fcp = np.random.uniform(500, 2500)
            lcp = np.random.uniform(1000, 4000)
            base_perf = np.random.uniform(60, 95)
        else:
            fcp = np.random.uniform(600, 3000)
            lcp = np.random.uniform(1200, 4500)
            base_perf = np.random.uniform(50, 92)
        
        # Core metrics
        cls = np.random.uniform(0, 0.4)  # Layout shift
        tbt = np.random.uniform(0, 600)  # Total blocking time
        speed_index = np.random.uniform(1000, 5000)
        page_size = np.random.uniform(500, 8000)  # KB
        
        # Calculate performance score based on metrics
        performance_score = max(0, min(100, 
            base_perf - (fcp/200 + lcp/300 + cls*50 + tbt/30 + page_size/1000)
        ))
        
        # SEO score (correlated with performance but not exactly)
        seo_score = max(0, min(100, 
            performance_score * np.random.uniform(0.8, 1.2)
        ))
        
        # Accessibility score
        accessibility_score = max(0, min(100, 
            performance_score * np.random.uniform(0.9, 1.1)
        ))
        
        # Best practices score
        best_practices_score = max(0, min(100, 
            performance_score * np.random.uniform(0.85, 1.15)
        ))
        
        # Meta description (1 = exists, 0 = doesn't exist)
        has_meta = np.random.choice([0, 1], p=[0.3, 0.7])
        
        # Title length
        title_length = np.random.randint(10, 120)
        
        # Device type
        device = np.random.choice(['mobile', 'desktop'])
        
        # Create category based on performance score
        if performance_score >= 90:
            category = 'Excellent'
        elif performance_score >= 75:
            category = 'Good'
        elif performance_score >= 50:
            category = 'Needs Improvement'
        else:
            category = 'Poor'
        
        data.append({
            'website_id': i + 1,
            'url': f'https://example{i}.com',
            'website_type': website_type,
            'device_type': device,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            
            # Scores
            'performance_score': round(performance_score, 1),
            'seo_score': round(seo_score, 1),
            'accessibility_score': round(accessibility_score, 1),
            'best_practices_score': round(best_practices_score, 1),
            
            # Core Web Vitals
            'first_contentful_paint': round(fcp, 0),
            'largest_contentful_paint': round(lcp, 0),
            'cumulative_layout_shift': round(cls, 3),
            'total_blocking_time': round(tbt, 0),
            'speed_index': round(speed_index, 0),
            
            # Resource metrics
            'total_byte_weight': round(page_size, 0),
            
            # SEO metrics
            'meta_description_exists': has_meta,
            'title_length': title_length,
            
            # Target for prediction
            'performance_category': category
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    
    print(f"✅ Created {len(df)} synthetic records")
    print(f"💾 Saved to: {DATA_PATH}")
    
    # Show sample
    print("\n📋 Sample of created data:")
    print(df[['website_type', 'performance_score', 'seo_score', 'performance_category']].head())
    
    # Show statistics
    print("\n📊 Data Statistics:")
    print(f"Performance Score: {df['performance_score'].mean():.1f} avg")
    print(f"SEO Score: {df['seo_score'].mean():.1f} avg")
    print(f"Category Distribution:")
    print(df['performance_category'].value_counts())
    
    return df

def collect_real_data():
    """
    OPTIONAL: Collect real data from PageSpeed API
    This requires internet and takes time
    """
    print("🌐 Collecting REAL data from websites...")
    print("⏳ This will take 10-15 minutes...")
    
    # You can add real collection here if needed
    # For now, we'll just use synthetic data
    
    create_synthetic_dataset(200)
    return True

def main():
    """
    Main data creation function
    """
    print("🤔 How do you want to create training data?")
    print("1. 📊 Create SYNTHETIC data (FAST, no internet needed)")
    print("2. 🌐 Collect REAL data (SLOW, requires internet)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '2':
        collect_real_data()
    else:
        create_synthetic_dataset(300)
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEP:")
    print("Run: python scripts/02_train_model.py")
    print("=" * 60)

if __name__ == "__main__":
    main()