from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)  # ✅ fixed __name__
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (important for migrations)
    from models import models # ✅ leave it here so Flask-Migrate sees the models

    # Register Blueprints
    from routes.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()

if __name__ == "__main__":  # ✅ fixed __name__
    app.run(debug=True)
