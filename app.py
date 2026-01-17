import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import requests
import json
import time
import os
import sys
from datetime import datetime
from io import BytesIO

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="PageSpeed AI Analyzer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS with animations, modern design, and responsiveness
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Animated gradient background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 3rem 2rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: moveGrid 20s linear infinite;
    }
    
    @keyframes moveGrid {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .main-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 5px 15px rgba(0,0,0,0.3);
        letter-spacing: -2px;
        position: relative;
        z-index: 1;
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.95);
        font-weight: 300;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
        animation: fadeInUp 1s ease 0.2s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Metric Cards with 3D effect */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 25px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.3);
        color: white;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 10px 0;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .metric-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .metric-card:hover {
        transform: translateY(-15px) rotateX(5deg);
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
        border-color: rgba(255, 255, 255, 0.6);
    }
    
    .metric-card h3 {
        color: white !important;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    
    .metric-card .value {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 3px 10px rgba(0,0,0,0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .metric-card .label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Score colors with glow */
    .score-excellent { 
        color: #00ff88 !important;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }
    .score-good { 
        color: #90EE90 !important;
        text-shadow: 0 0 20px rgba(144, 238, 144, 0.5);
    }
    .score-average { 
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    .score-poor { 
        color: #FF6B6B !important;
        text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Buttons with gradient and animation */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Tab styling with modern look */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 15px;
        padding: 0 2rem;
        color: white;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: white !important;
    }
    
    /* Progress bar with gradient */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 100%;
        animation: progressShine 2s linear infinite;
    }
    
    @keyframes progressShine {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    /* Sidebar with glass effect */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: white;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Metrics with animation */
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        border-left: 5px solid;
        margin: 15px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.05), transparent);
        pointer-events: none;
    }
    
    .recommendation-card:hover {
        transform: translateX(10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .recommendation-card h4 {
        color: white !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .recommendation-card p {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    .priority-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Download button special */
    .download-button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-success { background: #00ff88; box-shadow: 0 0 10px #00ff88; }
    .status-warning { background: #FFD700; box-shadow: 0 0 10px #FFD700; }
    .status-error { background: #FF6B6B; box-shadow: 0 0 10px #FF6B6B; }
    
    /* Welcome screen cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        transition: all 0.4s ease;
        margin: 1rem 0;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1.5rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
            border-radius: 20px;
        }
        
        .main-title {
            font-size: 2.5rem;
            letter-spacing: -1px;
        }
        
        .subtitle {
            font-size: 1.2rem;
        }
        
        .glass-card {
            padding: 1.5rem;
            border-radius: 20px;
        }
        
        .metric-card {
            padding: 1.5rem;
            border-radius: 20px;
        }
        
        .metric-card h3 {
            font-size: 1rem;
        }
        
        .metric-card .value {
            font-size: 2.5rem;
        }
        
        .metric-card .label {
            font-size: 0.9rem;
        }
        
        .stButton > button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            padding: 0.8rem;
            border-radius: 15px;
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            font-size: 1rem;
            padding: 0 1rem;
            border-radius: 12px;
        }
        
        .stTextInput > div > div > input {
            padding: 0.8rem;
            font-size: 0.9rem;
            border-radius: 12px;
        }
        
        .stRadio > div {
            padding: 0.8rem;
            border-radius: 12px;
        }
        
        .stMetric {
            padding: 1rem;
            border-radius: 12px;
        }
        
        .stMetric label {
            font-size: 0.9rem !important;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        .recommendation-card {
            padding: 1.2rem;
            border-radius: 15px;
            margin: 10px 0;
        }
        
        .recommendation-card h4 {
            font-size: 1.1rem;
        }
        
        .recommendation-card p {
            font-size: 0.95rem;
        }
        
        .priority-badge {
            padding: 0.4rem 0.8rem;
            font-size: 0.75rem;
        }
        
        .feature-card {
            padding: 1.5rem;
            border-radius: 20px;
        }
        
        .feature-icon {
            font-size: 2.5rem;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
    }
    
    @media (max-width: 576px) {
        .block-container {
            padding: 1rem;
        }
        
        .hero-section {
            padding: 1.5rem 1rem;
            border-radius: 15px;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .glass-card {
            padding: 1rem;
            border-radius: 15px;
        }
        
        .metric-card {
            padding: 1rem;
            border-radius: 15px;
        }
        
        .metric-card h3 {
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-card .value {
            font-size: 2rem;
            margin: 0.5rem 0;
        }
        
        .metric-card .label {
            font-size: 0.8rem;
        }
        
        .stButton > button {
            padding: 0.7rem 1.2rem;
            font-size: 0.9rem;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.3rem;
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            font-size: 0.9rem;
            padding: 0 0.8rem;
            border-radius: 10px;
        }
        
        .stTextInput > div > div > input {
            padding: 0.7rem;
            font-size: 0.85rem;
            border-radius: 10px;
        }
        
        .stRadio > div {
            padding: 0.7rem;
            border-radius: 10px;
            flex-direction: column;
        }
        
        .stMetric {
            padding: 0.8rem;
            border-radius: 10px;
        }
        
        .stMetric label {
            font-size: 0.85rem !important;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
        
        .recommendation-card {
            padding: 1rem;
            border-radius: 12px;
            margin: 8px 0;
        }
        
        .recommendation-card h4 {
            font-size: 1rem;
        }
        
        .recommendation-card p {
            font-size: 0.9rem;
        }
        
        .priority-badge {
            padding: 0.3rem 0.6rem;
            font-size: 0.7rem;
        }
        
        .feature-card {
            padding: 1.2rem;
            border-radius: 15px;
        }
        
        .feature-icon {
            font-size: 2rem;
        }
        
        ::-webkit-scrollbar {
            width: 6px;
        }
    }
    
    /* Adjust columns for small screens */
    @media (max-width: 768px) {
        [data-testid="column"] {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero section with animated background
st.markdown("""
<div class="hero-section">
    <h1 class="main-title">⚡ PageSpeed AI Analyzer Pro</h1>
    <p class="subtitle">Next-generation AI-powered website performance analysis with real-time insights</p>
</div>
""", unsafe_allow_html=True)

# Cache the model loading
@st.cache_resource(show_spinner="🤖 Loading AI model...")
def load_ai_model():
    """Load the trained AI model"""
    try:
        model = joblib.load('data/model/model.pkl')
        scaler = joblib.load('data/model/scaler.pkl')
        features = joblib.load('data/model/features.pkl')
        return model, scaler, features
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None, None

# Cache API data fetching
@st.cache_data(ttl=3600, show_spinner="📡 Fetching PageSpeed data...")
def get_pagespeed_data(url, strategy='mobile'):
    """Fetch data from PageSpeed Insights API"""
    
    # Get API key from Streamlit secrets or config
    API_KEY = None
    
    # Try Streamlit Cloud secrets first
    try:
        API_KEY = st.secrets["API_KEY"]
        # st.success("Using API key from Streamlit secrets")
    except Exception as e:
        # Fallback to local config for development
        try:
            from config import API_KEY
            # st.success("Using API key from config.py")
        except ImportError:
            st.error("❌ **API Key Configuration Error**")
            st.info("""
            Please configure your API key:
            
            **For Streamlit Cloud:**
            1. Go to App Settings → Secrets
            2. Add: API_KEY = "your_actual_api_key"
            
            **For Local Development:**
            1. Create .env file with: API_KEY=your_api_key
            2. Or update config.py with your API key
            """)
            return None
    
    if not API_KEY or API_KEY == "your_api_key_here":
        st.error("⚠️ **API Key Not Set**")
        st.info("Please add your Google PageSpeed API key to proceed")
        return None
    
    try:
        response = requests.get(
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
            params={
                'url': url,
                'key': API_KEY,
                'strategy': strategy,
                'category': ['PERFORMANCE', 'SEO', 'ACCESSIBILITY', 'BEST_PRACTICES']
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            if response.status_code == 429:
                st.info("Rate limit exceeded. Try again in a few minutes.")
            elif response.status_code == 400:
                st.info("Invalid URL or API key. Check your input.")
            return None
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def extract_metrics(api_data):
    """Extract metrics from API response"""
    if not api_data:
        return None
    
    try:
        metrics = {}
        categories = api_data['lighthouseResult']['categories']
        
        metrics['performance_score'] = categories.get('performance', {}).get('score', 0) * 100
        metrics['seo_score'] = categories.get('seo', {}).get('score', 0) * 100
        metrics['accessibility_score'] = categories.get('accessibility', {}).get('score', 0) * 100
        metrics['best_practices_score'] = categories.get('best-practices', {}).get('score', 0) * 100
        
        audits = api_data['lighthouseResult']['audits']
        
        metrics['first_contentful_paint'] = audits.get('first-contentful-paint', {}).get('numericValue', 0)
        metrics['largest_contentful_paint'] = audits.get('largest-contentful-paint', {}).get('numericValue', 0)
        metrics['cumulative_layout_shift'] = audits.get('cumulative-layout-shift', {}).get('numericValue', 0)
        metrics['total_blocking_time'] = audits.get('total-blocking-time', {}).get('numericValue', 0)
        metrics['speed_index'] = audits.get('speed-index', {}).get('numericValue', 0)
        metrics['time_to_interactive'] = audits.get('interactive', {}).get('numericValue', 0)
        
        total_bytes = audits.get('total-byte-weight', {}).get('numericValue', 0)
        metrics['total_byte_weight'] = total_bytes / 1024
        
        metrics['meta_description_exists'] = 1 if audits.get('meta-description', {}).get('score', 0) == 1 else 0
        
        title_audit = audits.get('document-title', {})
        if title_audit.get('details', {}).get('items'):
            metrics['title_length'] = len(title_audit['details']['items'][0].get('title', ''))
        else:
            metrics['title_length'] = 0
        
        metrics['image_alt_exists'] = 1 if audits.get('image-alt', {}).get('score', 0) == 1 else 0
        metrics['server_response_time'] = audits.get('server-response-time', {}).get('numericValue', 0)
        
        return metrics
        
    except Exception as e:
        st.error(f"Error extracting metrics: {e}")
        return None

def get_score_color(score):
    """Get color class based on score"""
    if score >= 90:
        return "score-excellent"
    elif score >= 75:
        return "score-good"
    elif score >= 50:
        return "score-average"
    else:
        return "score-poor"

def create_gauge_chart(value, title, max_value=100):
    """Create a beautiful gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 24, 'color': 'white', 'family': 'Inter'}},
        delta={'reference': 75, 'increasing': {'color': "#00ff88"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 2, 'tickcolor': "white"},
            'bar': {'color': "#00ff88", 'thickness': 0.35},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 3,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 107, 107, 0.3)'},
                {'range': [50, 75], 'color': 'rgba(255, 215, 0, 0.3)'},
                {'range': [75, 90], 'color': 'rgba(144, 238, 144, 0.3)'},
                {'range': [90, 100], 'color': 'rgba(0, 255, 136, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 5},
                'thickness': 0.8,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(t=60, b=20, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter", 'size': 16}
    )
    
    return fig

def create_radar_chart(metrics):
    """Create an enhanced radar chart"""
    categories = ['Performance', 'SEO', 'Accessibility', 'Best Practices']
    values = [
        metrics.get('performance_score', 0),
        metrics.get('seo_score', 0),
        metrics.get('accessibility_score', 0),
        metrics.get('best_practices_score', 0)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.4)',
        line=dict(color='#00ff88', width=4),
        marker=dict(size=12, color='#00ff88', symbol='circle',
                   line=dict(color='white', width=2)),
        name='Current Score'
    ))
    
    # Add target line at 90
    target = [90, 90, 90, 90]
    fig.add_trace(go.Scatterpolar(
        r=target + [target[0]],
        theta=categories + [categories[0]],
        fill=None,
        line=dict(color='rgba(255,255,255,0.5)', width=2, dash='dash'),
        marker=dict(size=0),
        name='Target (90)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=14, family='Inter'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(font=dict(color='white', size=12)),
        height=400,
        margin=dict(t=40, b=40, l=40, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def get_recommendations(metrics, prediction):
    """Get recommendations based on metrics"""
    recommendations = []
    
    if metrics.get('first_contentful_paint', 0) > 1800:
        recommendations.append({
            'category': '⚡ Performance',
            'title': 'Optimize First Contentful Paint',
            'description': 'Reduce server response time and eliminate render-blocking resources to improve initial page load experience.',
            'priority': 'High' if metrics['first_contentful_paint'] > 3000 else 'Medium',
            'color': '#FF6B6B' if metrics['first_contentful_paint'] > 3000 else '#FFD700'
        })
    
    if metrics.get('largest_contentful_paint', 0) > 2500:
        recommendations.append({
            'category': '🖼️ Performance',
            'title': 'Improve Largest Contentful Paint',
            'description': 'Optimize images using next-gen formats (WebP, AVIF), implement lazy loading, and use a CDN for faster delivery.',
            'priority': 'High' if metrics['largest_contentful_paint'] > 4000 else 'Medium',
            'color': '#FF6B6B' if metrics['largest_contentful_paint'] > 4000 else '#FFD700'
        })
    
    if metrics.get('cumulative_layout_shift', 0) > 0.1:
        recommendations.append({
            'category': '📐 User Experience',
            'title': 'Reduce Cumulative Layout Shift',
            'description': 'Add explicit size attributes to images and videos, reserve space for dynamic content, and use CSS aspect-ratio.',
            'priority': 'High' if metrics['cumulative_layout_shift'] > 0.25 else 'Medium',
            'color': '#FF6B6B' if metrics['cumulative_layout_shift'] > 0.25 else '#FFD700'
        })
    
    if metrics.get('meta_description_exists', 0) == 0:
        recommendations.append({
            'category': '🔍 SEO',
            'title': 'Add Meta Description',
            'description': 'Include a unique, compelling meta description (150-160 characters) to improve search engine visibility and CTR.',
            'priority': 'Medium',
            'color': '#FFD700'
        })
    
    if metrics.get('total_byte_weight', 0) > 4000:
        recommendations.append({
            'category': '📦 Optimization',
            'title': 'Reduce Total Page Size',
            'description': 'Compress and optimize images, minify CSS/JS files, remove unused code, and enable Gzip/Brotli compression.',
            'priority': 'Medium',
            'color': '#FFD700'
        })
    
    if prediction == 'Poor':
        recommendations.append({
            'category': '🚨 Critical',
            'title': 'Urgent Performance Improvements Required',
            'description': 'Your website needs immediate attention. Focus on Core Web Vitals, reduce page weight, and optimize critical resources.',
            'priority': 'High',
            'color': '#FF6B6B'
        })
    elif prediction == 'Needs Improvement':
        recommendations.append({
            'category': '📈 Enhancement',
            'title': 'Performance Optimization Opportunities',
            'description': 'Good foundation but room for improvement. Address specific metrics below threshold for better user experience.',
            'priority': 'Medium',
            'color': '#FFD700'
        })
    
    return recommendations

def display_analysis_results(metrics, prediction, probabilities, url, device):
    """Display beautiful analysis results"""
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Performance Dashboard", 
        "🤖 AI Intelligence", 
        "📈 Detailed Analytics", 
        "💡 Action Plan"
    ])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Header with site info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🌐 Analysis Results")
            st.markdown(f"**URL:** `{url}`")
            st.markdown(f"**Device:** {device.upper()} 📱" if device == 'mobile' else f"**Device:** {device.upper()} 💻")
        with col2:
            st.markdown(f"**Analyzed:** {datetime.now().strftime('%H:%M:%S')}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Score cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            perf_score = metrics.get('performance_score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Performance</h3>
                <div class="value {get_score_color(perf_score)}">{perf_score:.0f}</div>
                <div class="label">Core Web Vitals</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            seo_score = metrics.get('seo_score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔍 SEO Score</h3>
                <div class="value {get_score_color(seo_score)}">{seo_score:.0f}</div>
                <div class="label">Search Optimization</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            acc_score = metrics.get('accessibility_score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>♿ Accessibility</h3>
                <div class="value {get_score_color(acc_score)}">{acc_score:.0f}</div>
                <div class="label">Inclusive Design</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            bp_score = metrics.get('best_practices_score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 Best Practices</h3>
                <div class="value {get_score_color(bp_score)}">{bp_score:.0f}</div>
                <div class="label">Web Standards</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Core Web Vitals
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Core Web Vitals Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fcp = metrics.get('first_contentful_paint', 0)
            fcp_status = "✅ Good" if fcp < 1800 else "⚠️ Needs Work" if fcp < 3000 else "❌ Poor"
            st.metric("First Contentful Paint", f"{fcp:.0f} ms", fcp_status)
        
        with col2:
            lcp = metrics.get('largest_contentful_paint', 0)
            lcp_status = "✅ Good" if lcp < 2500 else "⚠️ Needs Work" if lcp < 4000 else "❌ Poor"
            st.metric("Largest Contentful Paint", f"{lcp:.0f} ms", lcp_status)
        
        with col3:
            cls = metrics.get('cumulative_layout_shift', 0)
            cls_status = "✅ Good" if cls < 0.1 else "⚠️ Needs Work" if cls < 0.25 else "❌ Poor"
            st.metric("Cumulative Layout Shift", f"{cls:.3f}", cls_status)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 🤖 AI-Powered Performance Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Prediction display
            pred_colors = {
                'Excellent': '#00ff88',
                'Good': '#90EE90',
                'Needs Improvement': '#FFD700',
                'Poor': '#FF6B6B'
            }
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3)); 
                        padding: 3rem 2rem; border-radius: 25px; text-align: center;
                        border: 2px solid rgba(255,255,255,0.3); box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                <div style="font-size: 1.3rem; color: rgba(255,255,255,0.9); margin-bottom: 1rem; 
                           text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">
                    🎯 AI Prediction
                </div>
                <div style="font-size: 3.5rem; font-weight: 900; margin: 2rem 0; 
                           color: {pred_colors.get(prediction, 'white')}; 
                           text-shadow: 0 0 30px {pred_colors.get(prediction, 'white')};">
                    {prediction}
                </div>
                <div style="font-size: 1.5rem; color: white; font-weight: 600;">
                    Confidence: {max(probabilities.values())*100:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(create_radar_chart(metrics), use_container_width=True)
        
        with col2:
            # Probability bars
            st.markdown("### 📊 Prediction Confidence Distribution")
            
            categories = list(probabilities.keys())
            values = list(probabilities.values())
            
            fig = px.bar(
                x=categories,
                y=values,
                color=values,
                color_continuous_scale=[[0, '#FF6B6B'], [0.5, '#FFD700'], [0.75, '#90EE90'], [1, '#00ff88']],
                labels={'x': '', 'y': 'Probability'},
                text=[f'{v:.1%}' for v in values]
            )
            
            fig.update_traces(
                textposition='outside',
                textfont=dict(size=16, color='white', family='Inter', weight='bold'),
                marker=dict(line=dict(width=3, color='rgba(255,255,255,0.5)'))
            )
            
            fig.update_layout(
                showlegend=False,
                yaxis=dict(
                    tickformat=".0%", 
                    range=[0, 1],
                    gridcolor='rgba(255,255,255,0.2)',
                    tickfont=dict(color='white', size=12)
                ),
                xaxis=dict(tickfont=dict(color='white', size=13, family='Inter')),
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Insights
            st.markdown("### 🧠 Intelligence Report")
            
            insights = {
                'Poor': "🚨 **CRITICAL ALERT** - Your website requires immediate optimization. Performance issues are severely impacting user experience and likely affecting conversion rates and SEO rankings. Prioritize Core Web Vitals improvements.",
                'Needs Improvement': "📈 **OPTIMIZATION NEEDED** - Your website has a solid foundation but significant room for improvement. Focus on addressing specific bottlenecks to enhance user experience and search rankings.",
                'Good': "✅ **GOOD PERFORMANCE** - Your website is performing well! Minor optimizations can push you into excellent territory. Continue monitoring and maintain current standards.",
                'Excellent': "🏆 **OUTSTANDING** - Exceptional performance! Your website delivers an excellent user experience. Keep monitoring metrics and stay current with best practices to maintain this high standard."
            }
            
            st.info(insights.get(prediction, "Analysis complete."))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 📈 Comprehensive Metrics Analysis")
        
        # Gauge charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_gauge_chart(metrics.get('performance_score', 0), "⚡ Performance Score"),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_gauge_chart(metrics.get('seo_score', 0), "🔍 SEO Score"),
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Additional metrics in a grid
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Performance Metrics Grid")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏱️ Total Blocking Time", f"{metrics.get('total_blocking_time', 0):.0f} ms")
            st.metric("🚀 Speed Index", f"{metrics.get('speed_index', 0):.0f}")
        
        with col2:
            st.metric("⚡ Time to Interactive", f"{metrics.get('time_to_interactive', 0):.0f} ms")
            st.metric("📦 Total Page Size", f"{metrics.get('total_byte_weight', 0)/1024:.2f} MB")
        
        with col3:
            st.metric("🖥️ Server Response", f"{metrics.get('server_response_time', 0):.0f} ms")
            meta_status = "✅ Present" if metrics.get('meta_description_exists', 0) else "❌ Missing"
            st.metric("📝 Meta Description", meta_status)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 💡 Personalized Action Plan")
        
        recommendations = get_recommendations(metrics, prediction)
        
        if recommendations:
            st.markdown(f"### Found {len(recommendations)} optimization opportunities")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="recommendation-card" style="border-left-color: {rec['color']};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; font-size: 1.3rem;">{i}. {rec['title']}</h4>
                        <span class="priority-badge" style="background: {rec['color']};">
                            {rec['priority']} Priority
                        </span>
                    </div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.95rem; margin-bottom: 0.5rem; font-weight: 600;">
                        {rec['category']}
                    </div>
                    <p style="margin: 0; color: rgba(255,255,255,0.95); line-height: 1.8; font-size: 1.05rem;">
                        {rec['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 **Perfect!** No critical issues detected. Your website is performing excellently!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Implementation guide
        st.markdown("### 📋 Implementation Roadmap")
        
        roadmap = """
        **Phase 1: Critical Fixes (Week 1)**
        - Address all HIGH priority items immediately
        - Focus on Core Web Vitals that are in the red zone
        - Implement quick wins like image compression
        
        **Phase 2: Performance Optimization (Week 2-3)**
        - Tackle MEDIUM priority recommendations
        - Optimize resource loading and caching
        - Implement lazy loading for images and videos
        
        **Phase 3: Fine-tuning (Week 4)**
        - Address remaining LOW priority items
        - Run A/B tests to measure impact
        - Set up continuous monitoring
        
        **Phase 4: Maintenance (Ongoing)**
        - Weekly performance checks using this tool
        - Monitor real user metrics (RUM)
        - Stay updated with web performance best practices
        """
        
        st.markdown(roadmap)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Sidebar with glass effect
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-size: 4rem; animation: bounce 2s ease-in-out infinite;">⚡</div>
            <h2 style="margin-top: 1rem; font-weight: 800; letter-spacing: -1px;">Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # URL input
        url = st.text_input(
            "🌐 Website URL",
            placeholder="https://example.com",
            help="Enter the complete URL including http:// or https://"
        )
        
        # Device selection
        device = st.radio(
            "📱 Analysis Device",
            ["mobile", "desktop"],
            index=0,
            horizontal=True
        )
        
        # Analysis button
        analyze_button = st.button(
            "🚀 Start Analysis",
            type="primary",
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        # System status
        st.markdown("### 🔋 System Status")
        
        model_status = os.path.exists('data/model/model.pkl')
        data_status = os.path.exists('data/raw/websites.csv')
        
        status_html = f"""
        <div style="padding: 1rem; border-radius: 15px; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
            <div style="margin: 0.5rem 0;">
                <span class="status-indicator {'status-success' if model_status else 'status-error'}"></span>
                <span>AI Model: {'Online' if model_status else 'Offline'}</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <span class="status-indicator {'status-success' if data_status else 'status-warning'}"></span>
                <span>Training Data: {'Loaded' if data_status else 'Missing'}</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <span class="status-indicator status-success"></span>
                <span>API Connection: Active</span>
            </div>
        </div>
        """
        
        st.markdown(status_html, unsafe_allow_html=True)
        
        st.divider()
        
        # Quick info
        with st.expander("ℹ️ About This Tool"):
            st.markdown("""
            **PageSpeed AI Analyzer Pro** leverages:
            
            🤖 **Machine Learning**
            - Random Forest classifier
            - SMOTE for balanced predictions
            - Real-time metric analysis
            
            📊 **Data Sources**
            - Google PageSpeed Insights API
            - Lighthouse performance metrics
            - Core Web Vitals data
            
            🎯 **Features**
            - Instant performance scoring
            - AI-powered predictions
            - Actionable recommendations
            - Beautiful visualizations
            - Comprehensive reports
            
            Built with Streamlit, Scikit-learn & Plotly
            """)
    
    # Main content
    if not url:
        # Welcome screen with feature showcase
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <div style="font-size: 6rem; margin-bottom: 1rem; animation: bounce 2s ease-in-out infinite;">⚡</div>
                <h2 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem;">
                    Transform Your Website Performance
                </h2>
                <p style="font-size: 1.3rem; color: rgba(255,255,255,0.9); margin-bottom: 2rem;">
                    AI-powered insights • Real-time analysis • Actionable recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature cards
        col1, col2, col3, col4 = st.columns(4)
        
        features = [
            ("🤖", "AI Analysis", "Machine learning predictions"),
            ("⚡", "Real-time", "Instant performance metrics"),
            ("📊", "Visualizations", "Beautiful data charts"),
            ("💡", "Recommendations", "Actionable improvements")
        ]
        
        for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3 style="font-size: 1.2rem; margin: 0.5rem 0; color: white;">{title}</h3>
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Quick start section
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Quick Start - Try These Popular Sites")
        
        quick_cols = st.columns(4)
        quick_sites = [
            ("Google", "https://google.com", "🔍"),
            ("GitHub", "https://github.com", "💻"),
            ("Stack Overflow", "https://stackoverflow.com", "❓"),
            ("Wikipedia", "https://wikipedia.org", "📚")
        ]
        
        for i, (name, site_url, icon) in enumerate(quick_sites):
            if quick_cols[i].button(f"{icon} {name}", use_container_width=True):
                st.session_state['quick_url'] = site_url
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return
    
    # Check for quick analysis
    if 'quick_url' in st.session_state:
        url = st.session_state['quick_url']
        del st.session_state['quick_url']
        analyze_button = True
    
    # Perform analysis
    if analyze_button and url:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Animated progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1
        status_text.markdown("### 📡 Connecting to PageSpeed Insights...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        api_data = get_pagespeed_data(url, device)
        
        if not api_data:
            st.error("❌ Unable to fetch data. Please verify the URL and try again.")
            return
        
        # Step 2
        status_text.markdown("### 🔧 Processing Performance Metrics...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        metrics = extract_metrics(api_data)
        
        if not metrics:
            st.error("❌ Metric extraction failed. Please try again.")
            return
        
        # Step 3
        status_text.markdown("### 🤖 Running AI Analysis...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        model, scaler, features = load_ai_model()
        
        if model and scaler and features:
            feature_values = [metrics.get(feature, 0) for feature in features]
            features_scaled = scaler.transform([feature_values])
            
            prediction = model.predict(features_scaled)[0]
            probabilities_raw = model.predict_proba(features_scaled)[0]
            probabilities = dict(zip(model.classes_, probabilities_raw))
            
            status_text.markdown("### ✅ Analysis Complete!")
            progress_bar.progress(100)
            time.sleep(0.8)
            
            progress_bar.empty()
            status_text.empty()
            
            # Success message
            st.success(f"✅ Successfully analyzed **{url}** on **{device.upper()}**")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display results
            display_analysis_results(metrics, prediction, probabilities, url, device)
            
            # Download report
            st.markdown("<br><br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                report = f"""
# PageSpeed AI Analysis Report - Pro Edition

**Website:** {url}
**Device:** {device.upper()}
**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Performance Scores

- ⚡ Performance: {metrics.get('performance_score', 0):.1f}/100
- 🔍 SEO: {metrics.get('seo_score', 0):.1f}/100  
- ♿ Accessibility: {metrics.get('accessibility_score', 0):.1f}/100
- 🏆 Best Practices: {metrics.get('best_practices_score', 0):.1f}/100

## 🤖 AI Prediction

- Category: {prediction}
- Confidence: {max(probabilities.values())*100:.1f}%

## ⚡ Core Web Vitals

- First Contentful Paint: {metrics.get('first_contentful_paint', 0):.0f} ms
- Largest Contentful Paint: {metrics.get('largest_contentful_paint', 0):.0f} ms
- Cumulative Layout Shift: {metrics.get('cumulative_layout_shift', 0):.3f}

## 💡 Recommendations

{len(get_recommendations(metrics, prediction))} optimization opportunities identified

---
Generated by PageSpeed AI Analyzer Pro
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report,
                    file_name=f"pagespeed_pro_report_{url.replace('https://', '').replace('http://', '').replace('/', '_')[:50]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.error("❌ AI model unavailable. Please train the model first.")

if __name__ == "__main__":
    main()