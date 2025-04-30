import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # General Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: JWT or Mail configs can go here
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-secret'
