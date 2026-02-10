import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

        self.SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            os.getenv("FLASK_DB_DIR", ""),  # allow override if desired
            "app.db",
        )
        # Put DB inside instance/ by default
        # Flask will resolve relative paths to instance folder when instance_relative_config=True
        if "FLASK_DB_DIR" not in os.environ:
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join("instance", "app.db")

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # App URL used to generate absolute links in emails
        self.APP_URL = os.getenv("FLASK_APP_URL", "http://127.0.0.1:5000")

        # Mail placeholders (optional)
        self.MAIL_SERVER = os.getenv("MAIL_SERVER", "")
        self.MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
        self.MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes", "y")
        self.MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
        self.MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
        self.MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@example.com")
