import os
import cloudinary
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # --------------------
    # CORE SECRETS
    # --------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # --------------------
    # DATABASE
    # --------------------
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --------------------
    # SESSION
    # --------------------
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # --------------------
    # CLOUDINARY (NO FALLBACKS)
    # --------------------
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    @staticmethod
    def init_cloudinary():
        if not all([
            Config.CLOUDINARY_CLOUD_NAME,
            Config.CLOUDINARY_API_KEY,
            Config.CLOUDINARY_API_SECRET,
        ]):
            raise RuntimeError("Cloudinary credentials are missing")

        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
            secure=True,
        )
