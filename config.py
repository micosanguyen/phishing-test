import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_KEY = os.getenv("ADMIN_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = "sqlite:///phishing_test.db"
EXAM_SIZE = int(os.getenv("EXAM_SIZE", "10"))
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
