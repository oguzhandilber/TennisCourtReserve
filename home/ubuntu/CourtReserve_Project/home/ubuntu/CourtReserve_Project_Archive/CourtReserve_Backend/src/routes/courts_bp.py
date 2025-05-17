from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from src.models import db, Court, User # Assuming User model is in src.models
from src.models.court import court_followers_association # Import the association table
from datetime import datetime, date as DDate, timedelta

courts_bp = Blueprint("courts_bp", __name__, url_prefix="/api/courts")

@courts_bp.route("", methods=["GET"])
@jwt_required()
def get_courts():
    current_user_obj = get_current_user()
    courts = Court.query.order_by(Court.name).all()
    return jsonify([court.to_dict(current_user_id=current_user_obj.id) for court in courts]), 200

@courts_bp.route("/<int:court_id>", methods=["GET"])
@jwt_required()
def get_court_details(court_id):
    current_user_obj = get_current_user()
    court = Court.query.get_or_404(court_id)
    return jsonify(court.to_dict(current_user_id=current_user_obj.id)), 200

@courts_bp.route("/<int:court_id>/follow", methods=["POST"])
@jwt_required()
def follow_court(court_id):
    current_user_obj = get_current_user()
    court = Court.query.get_or_404(court_id)

    if court in current_user_obj.followed_courts:
        return jsonify({"message": f"You are already following {court.name}."}), 409 # Conflict

    current_user_obj.followed_courts.append(court)
    db.session.commit()
    return jsonify({"message": f"You are now following {court.name}."}), 200

@courts_bp.route("/<int:court_id>/unfollow", methods=["POST"])
@jwt_required()
def unfollow_court(court_id):
    current_user_obj = get_current_user()
    court = Court.query.get_or_404(court_id)

    if court not in current_user_obj.followed_courts:
        return jsonify({"message": f"You are not following {court.name}."}), 404

    current_user_obj.followed_courts.remove(court)
    db.session.commit()
    return jsonify({"message": f"You have unfollowed {court.name}."}), 200

# Placeholder for availability - this is complex and will be built out
@courts_bp.route("/<int:court_id>/availability", methods=["GET"])
@jwt_required()
def get_court_availability(court_id):
    court = Court.query.get_or_404(court_id)
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Date query parameter is required (YYYY-MM-DD)"}), 400
    
    try:
        target_date = DDate.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Simplified operating hours - assuming a default if not specified for the day
    # In a real app, this would be more dynamic (e.g. per day of week)
    operating_hours_today = court.operating_hours.get("default", ["07:00", "22:00"])
    open_time_dt = datetime.strptime(operating_hours_today[0], "%H:%M").time()
    close_time_dt = datetime.strptime(operating_hours_today[1], "%H:%M").time()

    available_slots = []
    current_slot_time = datetime.combine(target_date, open_time_dt)
    close_datetime = datetime.combine(target_date, close_time_dt)

    from src.models.booking import Booking # Avoid circular import if possible, or move Booking import

    while current_slot_time < close_datetime:
        slot_end_time = current_slot_time + timedelta(hours=1)
        # Check for existing bookings for this slot
        existing_booking = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.start_time == current_slot_time,
            Booking.status.in_(["confirmed", "pending_approval"]) # Consider both confirmed and pending
        ).first()

        slot_info = {
            "time": current_slot_time.strftime("%H:%M"),
        }

        if existing_booking:
            slot_info["status"] = existing_booking.status # or map to 'booked', 'pending_approval'
            slot_info["booking_id"] = existing_booking.id
            current_user_obj = get_current_user()
            slot_info["booked_by_current_user"] = (existing_booking.user_id == current_user_obj.id)
        else:
            slot_info["status"] = "available"
        
        available_slots.append(slot_info)
        current_slot_time = slot_end_time

    return jsonify({
        "court_id": court.id,
        "court_name": court.name,
        "date": date_str,
        "operating_hours": operating_hours_today,
        "available_slots": available_slots
    }), 200

