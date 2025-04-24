from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from .routes import api_bp
from .extensions import db, ma, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)
    Swagger(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
