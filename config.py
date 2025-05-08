import os
import cloudinary
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False 
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax' 

 
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or 'dpmstcaxl'
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or '367654284475498'
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or 'Q0oDtFZuQlpMAfG_Jqb3he1fJMo'

    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET
        )
