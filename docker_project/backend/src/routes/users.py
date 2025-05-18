from flask import Blueprint, request, jsonify
from src.models.user import User
from src.extensions import db # db को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__)

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_current_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    # केवल अनुमत फ़ील्ड्स को अपडेट करें
    if "full_name" in data:
        user.full_name = data["full_name"]
    if "phone_number" in data:
        user.phone_number = data["phone_number"]
    if "skill_level" in data:
        user.skill_level = data["skill_level"]
    if "profile_picture_url" in data:
        user.profile_picture_url = data["profile_picture_url"]
    if "communication_preferences" in data:
        user.communication_preferences = data["communication_preferences"]
    
    # ईमेल और पासवर्ड बदलने के लिए अलग एंडपॉइंट्स होने चाहिए
    # भूमिका परिवर्तन व्यवस्थापक द्वारा नियंत्रित किया जाना चाहिए

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "user": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating profile", "error": str(e)}), 500

@users_bp.route("/<int:user_id>/profile", methods=["GET"])
# यह एंडपॉइंट सार्वजनिक हो सकता है या प्रमाणीकरण की आवश्यकता हो सकती है, यह इस पर निर्भर करता है कि कौन सा डेटा लौटाया जा रहा है
# अभी के लिए, हम इसे प्रमाणीकृत उपयोगकर्ताओं के लिए खुला रखते हैं
@jwt_required() 
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # केवल सार्वजनिक रूप से सुरक्षित डेटा लौटाएँ
    # to_dict() मेथड में एक पैरामीटर हो सकता है जो यह नियंत्रित करता है कि कौन सा डेटा लौटाया जाए
    return jsonify(user.to_dict()), 200

