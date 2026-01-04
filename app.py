from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta
import logging
import os
import traceback

from dotenv import load_dotenv
load_dotenv()

from extensions import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# --------------------
# LOGGING
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------
# APP INIT
# --------------------
app = Flask(__name__)

# --------------------
# DATABASE
# --------------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --------------------
# SECRETS
# --------------------
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "dev-secret-key"
)

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "dev-jwt-secret"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

# --------------------
# SESSION / COOKIES
# --------------------
app.config["SESSION_COOKIE_SECURE"] = os.getenv(
    "SESSION_COOKIE_SECURE", "false"
).lower() == "true"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = os.getenv(
    "SESSION_COOKIE_SAMESITE", "Lax"
)

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

# --------------------
# EXTENSIONS
# --------------------
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# --------------------
# CORS
# --------------------
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5173",
        "https://fashion-design-fronted.vercel.app",
        "https://fashion-design-fronted-git-main-ythaka1s-projects.vercel.app",
        "https://fashion-design-frontend-three.vercel.app",
        "https://fashion-designed-frontend.vercel.app",
        "https://fashion-designed-frontend-e8ja26wcj-ythaka1s-projects.vercel.app",
    ],
)

# --------------------
# BLUEPRINTS
# --------------------
from routes.auth import auth_bp
from routes.mpesa import mpesa_bp
from routes.main import main

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(mpesa_bp, url_prefix="/mpesa/api")
app.register_blueprint(main)

# --------------------
# HEALTH CHECKS
# --------------------
@app.route("/api/test")
def test():
    return jsonify({"message": "API is working"})

@app.route("/api/test-db")
def test_db():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"success": True})
    except Exception:
        logger.error(traceback.format_exc())
        return jsonify({"success": False}), 500

# --------------------
# GLOBAL ERROR HANDLER
# --------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(traceback.format_exc())
    return jsonify({"message": "Internal server error"}), 500

# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
