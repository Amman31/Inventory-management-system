"""App-wide settings: paths and directories."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_DIR = DATA_DIR
DATABASE_PATH = os.path.join(DATA_DIR, "database.db")
BILL_DIR = os.path.join(DATA_DIR, "bills")
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BILL_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
