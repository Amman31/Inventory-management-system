import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "ims.db")

IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

# Ensure folders exist at import time (database, bills, images)
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(BILL_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)