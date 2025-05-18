from flask import Blueprint, request, jsonify
from src.models.court import Court
from src.models.user import User
from src.models.court_follower import CourtFollower
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.routes.notifications import notify_court_followers
import datetime

court_followers_bp = Blueprint("court_followers", __name__)

@court_followers_bp.route("/courts/<int:court_id>/follow", methods=["POST"])
@jwt_required()
def follow_court(court_id):
    """Follow a court to receive notifications about it."""
    current_user_id = get_jwt_identity()
    
    # Check if court exists
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    
    # Check if already following
    existing_follow = CourtFollower.query.filter_by(
        user_id=current_user_id,
        court_id=court_id
    ).first()
    
    if existing_follow:
        return jsonify({"message": "You are already following this court"}), 400
    
    # Create new follow relationship
    new_follow = CourtFollower(
        user_id=current_user_id,
        court_id=court_id,
        created_at=datetime.datetime.utcnow()
    )
    
    db.session.add(new_follow)
    db.session.commit()
    
    return jsonify({
        "message": f"You are now following {court.name}",
        "court_id": court_id,
        "court_name": court.name
    }), 201

@court_followers_bp.route("/courts/<int:court_id>/unfollow", methods=["POST"])
@jwt_required()
def unfollow_court(court_id):
    """Unfollow a court to stop receiving notifications about it."""
    current_user_id = get_jwt_identity()
    
    # Check if court exists
    court = Court.query.get(court_id)
    if not court:
        return jsonify({"message": "Court not found"}), 404
    
    # Find the follow relationship
    follow = CourtFollower.query.filter_by(
        user_id=current_user_id,
        court_id=court_id
    ).first()
    
    if not follow:
        return jsonify({"message": "You are not following this court"}), 400
    
    # Remove the follow relationship
    db.session.delete(follow)
    db.session.commit()
    
    return jsonify({
        "message": f"You have unfollowed {court.name}",
        "court_id": court_id,
        "court_name": court.name
    }), 200

@court_followers_bp.route("/courts/followed", methods=["GET"])
@jwt_required()
def get_followed_courts():
    """Get all courts followed by the current user."""
    current_user_id = get_jwt_identity()
    
    # Get all followed courts
    followed_courts = Court.query.join(
        CourtFollower, Court.id == CourtFollower.court_id
    ).filter(
        CourtFollower.user_id == current_user_id,
        Court.status == "active"
    ).all()
    
    courts_data = [court.to_dict() for court in followed_courts]
    
    return jsonify({
        "message": "Followed courts retrieved successfully",
        "courts": courts_data,
        "count": len(courts_data)
    }), 200
