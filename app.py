from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import traceback
import os
from datetime import timedelta
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for sessions and JWT
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-this'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-key-change-this'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Session configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


from extensions import db
db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Update CORS to allow requests from all your frontend URLs
CORS(app, 
     resources={r"/*": {"origins": [
         "http://localhost:5173", 
         "https://fashion-design-fronted.vercel.app",
         "https://fashion-design-fronted-git-main-ythaka1s-projects.vercel.app",
         "https://fashion-design-frontend-three.vercel.app",  # Add your new frontend domain
         # For maximum compatibility, you can use a wildcard for all subdomains
         "https://*.vercel.app"
     ]}},
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"])


with app.app_context():
    from models.models import User, Category, Product, CartItem, Order, Invoice, Address


from routes.auth import auth_bp
from routes.mpesa import mpesa_bp  

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(mpesa_bp, url_prefix='/mpesa/api') 


@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return jsonify(success=True)


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working'})


@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        
        result = db.session.execute('SELECT 1').fetchone()
        if result:
            return jsonify({'success': True, 'message': 'Database connection successful'})
        else:
            return jsonify({'success': False, 'message': 'Database connection failed'})
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'})


@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(traceback.format_exc())
    response = jsonify({'success': False, 'message': 'Internal server error'})
    response.status_code = 500
    return response

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
        
        
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                username='Admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),  
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created")
    
    app.run(debug=True)
