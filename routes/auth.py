from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import logging
import traceback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        
        from models.models import User
        
        data = request.get_json()
        logger.info(f"Registration attempt with data: {data}")
        
        
        if not all(key in data for key in ['username', 'email', 'password']):
            logger.warning("Missing required fields in registration request")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            logger.warning(f"Registration failed: Email already exists: {data['email']}")
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
       
        role = data.get('role', 'customer')
        
       
        try:
            new_user = User(
                username=data['username'],
                email=data['email'],
                password_hash=generate_password_hash(data['password']),
                role=role
            )
            
            logger.info(f"Creating new user: {data['username']}, {data['email']}, role: {role}")
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User created successfully with ID: {new_user.id}")
            
           
            session['user_id'] = new_user.id
            session['is_admin'] = role == 'admin'
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'role': new_user.role,
                    'isAdmin': role == 'admin'
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during user registration: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'success': False, 'message': f'Registration error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in register route: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        
        from models.models import User
        
        data = request.get_json()
        logger.info(f"Login attempt for email: {data.get('email', 'not provided')}")
        
        
        if not all(key in data for key in ['email', 'password']):
            logger.warning("Missing email or password in login request")
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
      
        user = User.query.filter_by(email=data['email']).first()
        
        
        if not user:
            logger.warning(f"Login failed: User not found for email: {data['email']}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        if not check_password_hash(user.password_hash, data['password']):
            logger.warning(f"Login failed: Invalid password for user: {user.email}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
       
        session['user_id'] = user.id
        session['is_admin'] = user.role == 'admin'
        logger.info(f"User logged in successfully: {user.email}, role: {user.role}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'isAdmin': user.role == 'admin'
            }
        }), 200
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/admin/login', methods=['POST', 'OPTIONS'])
def admin_login():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        
        from models.models import User
        
        data = request.get_json()
        logger.info(f"Admin login attempt for email: {data.get('email', 'not provided')}")
        
       
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        
        user = User.query.filter_by(email=data['email']).first()
        
        
        if not user:
            logger.warning(f"Admin login failed: User not found for email: {data.get('email')}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        if not check_password_hash(user.password_hash, data['password']):
            logger.warning(f"Admin login failed: Invalid password for user: {user.email}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
       
        if user.role != 'admin':
            logger.warning(f"Admin login failed: User is not an admin: {user.email}")
            return jsonify({'success': False, 'message': 'You do not have admin privileges'}), 403
        
       
        session['user_id'] = user.id
        session['is_admin'] = True
        logger.info(f"Admin logged in successfully: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Admin login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'isAdmin': True
            }
        }), 200
    except Exception as e:
        logger.error(f"Error during admin login: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        user_id = session.get('user_id')
        if user_id:
            logger.info(f"User logged out: ID {user_id}")
        
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/check', methods=['GET', 'OPTIONS'])
def check_auth():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        
        from models.models import User
        
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                is_admin = session.get('is_admin', False) or user.role == 'admin'
                logger.info(f"Auth check: User is authenticated: {user.email}, Admin: {is_admin}")
                return jsonify({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'isAdmin': is_admin
                    }
                }), 200
        
        logger.info("Auth check: User is not authenticated")
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    except Exception as e:
        logger.error(f"Error during auth check: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500


@auth_bp.route('/create-admin', methods=['POST', 'OPTIONS'])
def create_admin():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
       
        from models.models import User
        
        data = request.get_json()
        logger.info(f"Create admin attempt with data: {data}")
        
        
        if not all(key in data for key in ['username', 'email', 'password']):
            logger.warning("Missing required fields in create admin request")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            logger.warning(f"Create admin failed: Email already exists: {data['email']}")
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
       
        try:
            new_admin = User(
                username=data['username'],
                email=data['email'],
                password_hash=generate_password_hash(data['password']),
                role='admin'
            )
            
            logger.info(f"Creating new admin: {data['username']}, {data['email']}")
            db.session.add(new_admin)
            db.session.commit()
            logger.info(f"Admin created successfully with ID: {new_admin.id}")
            
            return jsonify({
                'success': True,
                'message': 'Admin created successfully',
                'user': {
                    'id': new_admin.id,
                    'username': new_admin.username,
                    'email': new_admin.email,
                    'role': new_admin.role
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during admin creation: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'success': False, 'message': f'Admin creation error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in create admin route: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'Server error'}), 500
