import os
import cloudinary

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # General Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    # Database (PostgreSQL if available, else fallback to SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('dpmstcaxl') or 'your_cloud_name'
    CLOUDINARY_API_KEY = os.environ.get('367654284475498') or 'your_api_key'
    CLOUDINARY_API_SECRET = os.environ.get('Q0oDtFZuQlpMAfG_Jqb3he1fJMo') or 'your_api_secret'

    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET
        )
