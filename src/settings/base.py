import os

TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
TELEGRAM_SESSION_NAME = "telegram"
DB_URL = os.environ.get("APP_DB_HOST", "mongodb://localhost:27017")
DB_NAME = os.environ.get("APP_DB_NAME", "default")
