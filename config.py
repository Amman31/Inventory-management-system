import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
# Database directory
DATABASE_DIR = DATA_DIR
DATABASE_PATH = os.path.join(DATA_DIR, "database.db")
# Bills directory
BILL_DIR = os.path.join(DATA_DIR, "bills")
# Images directory
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BILL_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
