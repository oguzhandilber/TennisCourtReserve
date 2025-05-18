import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.extensions import db
from src.models.user import User
from flask import Flask
from src.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    return app

def create_admin_user():
    """Create an admin user for testing purposes"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin_email = "admin@tenniscourt.com"
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if existing_admin:
            print(f"Admin user already exists with email: {admin_email}")
            return
        
        # Create new admin user
        admin_user = User(
            email=admin_email,
            password="admin123",
            full_name="Admin User",
            role="admin"
        )
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created successfully with email: {admin_email} and password: admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin_user()
