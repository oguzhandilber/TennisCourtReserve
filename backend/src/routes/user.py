from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from src.models.user import User, db
import datetime
from functools import wraps

user_bp = Blueprint('user', __name__, url_prefix='/api/users') # Added url_prefix

# Admin required decorator
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_current_user()
        if not current_user or current_user.role != 'admin':
            return jsonify(message="Admin access required"), 403
        return fn(*args, **kwargs)
    return wrapper

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get the profile of the currently authenticated user."""
    current_user_obj = get_current_user()
    if not current_user_obj:
        return jsonify({"message": "User not found or token invalid"}), 404 # Should be caught by jwt_required
    return jsonify(current_user_obj.to_dict()), 200

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_me():
    """Update the profile of the currently authenticated user."""
    current_user_obj = get_current_user()
    if not current_user_obj:
        return jsonify({"message": "User not found or token invalid"}), 404

    data = request.get_json()
    
    # Fields that can be updated by the user
    allowed_updates = ["full_name", "phone_number", "skill_level", "profile_picture_url", "communication_preferences"]
    
    updated = False
    for field in allowed_updates:
        if field in data:
            setattr(current_user_obj, field, data[field])
            updated = True
            
    if 'email' in data and data['email'].lower() != current_user_obj.email:
        # Check if new email is already taken
        if User.query.filter(User.email == data['email'].lower(), User.id != current_user_obj.id).first():
            return jsonify({"message": "Email already registered by another user."}), 409
        current_user_obj.email = data['email'].lower()
        updated = True

    # Password update should be handled separately, e.g., via a /me/change-password endpoint
    # For simplicity, not included here.

    if updated:
        current_user_obj.updated_at = datetime.datetime.utcnow()
        try:
            db.session.commit()
            return jsonify({"message": "Profile updated successfully.", "user": current_user_obj.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error updating profile.", "error": str(e)}), 500
    else:
        return jsonify({"message": "No update data provided."}), 400


# Admin/Generic User Routes (can be kept or refactored based on needs)
@user_bp.route('', methods=['GET']) # Changed from /users to /
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict(include_sensitive=False) for user in users]) # Ensure sensitive data is not exposed

# POST /api/users (create_user) - This is typically handled by /api/auth/register
# If needed for admin purposes, it should be protected. For now, commenting out to avoid conflict.
# @user_bp.route('', methods=['POST'])
# @jwt_required() # Consider admin protection
# def create_user():
#     data = request.json
#     # Add more validation as needed
#     if User.query.filter_by(email=data['email'].lower()).first():
#         return jsonify({"message": "Email already registered"}), 409
#     user = User(
#         email=data['email'].lower(),
#         password=data['password'], # Password should be hashed in User model's __init__ or set_password
#         full_name=data.get('full_name'),
#         role=data.get('role', 'player')
#     )
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(user.to_dict()), 201

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required # Or a more complex check if users can view other specific profiles
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict(include_sensitive=False)) # Ensure sensitive data is not exposed

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # Example: Admin can update more fields
    if 'full_name' in data: user.full_name = data['full_name']
    if 'email' in data:
        if data['email'].lower() != user.email and User.query.filter(User.email == data['email'].lower(), User.id != user.id).first():
            return jsonify({"message": "Email already registered by another user."}), 409
        user.email = data['email'].lower()
    if 'role' in data: user.role = data['role']
    # Add other fields as necessary for admin updates
    
    user.updated_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    current_user_obj = get_current_user() # This is already the admin due to @admin_required
    if current_user_obj.id == user_id: # Admin cannot delete themselves
        return jsonify({"message": "Admin cannot delete their own account via this endpoint."}), 403
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
