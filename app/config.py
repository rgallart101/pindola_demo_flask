import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

        self.DEBUG_MODE = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes", "y")

        # Put DB inside instance/ by default
        db_dir = os.getenv("FLASK_DB_DIR", None)
        if db_dir:
            db_path = os.path.join(db_dir, "app.db")
        else:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "app.db")

        self.SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Session Configuration (needed for language persistence)
        self.SESSION_PERMANENT = True
        self.PERMANENT_SESSION_LIFETIME = timedelta(days=7)
        self.SESSION_COOKIE_SAMESITE = 'Lax'

        # App URL used to generate absolute links in emails
        self.APP_URL = os.getenv("FLASK_APP_URL", "http://127.0.0.1:5000")

        # Mail placeholders (optional)
        self.MAIL_SERVER = os.getenv("MAIL_SERVER", "")
        self.MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
        self.MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes", "y")
        self.MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
        self.MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
        self.MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@example.com")
