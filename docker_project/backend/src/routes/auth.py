from flask import Blueprint, request, jsonify
from src.models.user import User
from src.extensions import db, jwt # db और jwt को main.py से इम्पोर्ट करें
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if User.query.filter_by(email=email.lower()).first():
        return jsonify({"message": "Email already registered"}), 409

    new_user = User(email=email.lower(), password=password, full_name=full_name)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

    # रजिस्ट्रेशन के बाद टोकन जारी करें
    access_token = create_access_token(identity=str(new_user.id))
    refresh_token = create_refresh_token(identity=str(new_user.id))

    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": new_user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email.lower()).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True) # यह सुनिश्चित करता है कि केवल एक वैध रिफ्रेश टोकन ही इस एंडपॉइंट तक पहुँच सकता है
def refresh_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200

# OAuth और अन्य प्रमाणीकरण संबंधित एंडपॉइंट्स यहाँ जोड़े जा सकते हैं

