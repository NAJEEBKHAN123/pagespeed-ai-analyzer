import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('PAGESPEED_API_KEY')
if not API_KEY:
    print("❌ ERROR: Add your API key to .env file")
    exit(1)

# Paths
DATA_PATH = "data/raw/websites.csv"
MODEL_PATH = "data/model/model.pkl"
SCALER_PATH = "data/model/scaler.pkl"