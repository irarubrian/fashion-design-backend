from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.models import User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "customer")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists"}), 400

    try:
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["is_admin"] = user.role == "admin"

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "isAdmin": user.role == "admin"
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Register error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    session["user_id"] = user.id
    session["is_admin"] = user.role == "admin"

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "isAdmin": user.role == "admin"
        }
    }), 200


# =========================
# ADMIN LOGIN
# =========================
@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    if user.role != "admin":
        return jsonify({"success": False, "message": "Admin access required"}), 403

    session["user_id"] = user.id
    session["is_admin"] = True

    return jsonify({
        "success": True,
        "message": "Admin login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "isAdmin": True
        }
    }), 200


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


# =========================
# CHECK AUTH
# =========================
@auth_bp.route("/check", methods=["GET"])
def check_auth():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    user = User.query.get(user_id)

    if not user:
        session.clear()
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "isAdmin": user.role == "admin"
        }
    }), 200
