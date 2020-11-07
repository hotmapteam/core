import os

TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
TELEGRAM_SESSION_NAME = "telegram"
DB_URL = os.environ.get("APP_DB_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("APP_DB_NAME", "default")
API_LISTEN = os.environ.get("API_LISTEN", "127.0.0.1:8000").split(":")
