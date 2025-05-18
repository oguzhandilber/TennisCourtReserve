from flask import Blueprint, request, jsonify
from src.models.court import Court
from src.models.booking import Booking
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
import datetime

courts_bp = Blueprint("courts", __name__)

@courts_bp.route("", methods=["GET"])
def list_courts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    query = Court.query.filter(Court.status == "active")
    search_term = request.args.get("search")
    if search_term:
        query = query.filter(Court.name.ilike(f"%{search_term}%") | Court.address.ilike(f"%{search_term}%"))
    
    surface_type = request.args.get("surface_type")
    if surface_type:
        query = query.filter(Court.surface_type.ilike(f"%{surface_type}%"))
    
    setting = request.args.get("setting")
    if setting:
        query = query.filter(Court.setting.ilike(f"%{setting}%"))
    
    paginated_courts = query.paginate(page=page, per_page=per_page, error_out=False)
    courts_data = [court.to_dict() for court in paginated_courts.items]
    
    return jsonify({
        "message": "Courts retrieved successfully",
        "courts": courts_data,
        "total_pages": paginated_courts.pages,
        "current_page": paginated_courts.page,
        "total_courts": paginated_courts.total
    }), 200

@courts_bp.route("/<int:court_id>", methods=["GET"])
def get_court_details(court_id):
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    return jsonify(court.to_dict()), 200

@courts_bp.route("/<int:court_id>/availability", methods=["GET"])
def get_court_availability(court_id):
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"message": "Date parameter is required (YYYY-MM-DD)"}), 400
    
    try:
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Default operating hours (8 AM to 10 PM)
    operating_hours = ["08:00", "22:00"]
    
    # Generate time slots
    available_slots = []
    start_hour = 8
    end_hour = 22
    
    # Get current user ID if authenticated
    current_user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            from flask_jwt_extended import decode_token
            token = auth_header.split(' ')[1]
            decoded = decode_token(token)
            current_user_id = decoded.get('sub')
        except:
            pass
    
    for hour in range(start_hour, end_hour):
        time_str = f"{hour:02d}:00"
        slot_start_time = datetime.datetime.combine(target_date, datetime.time(hour, 0, 0))
        slot_end_time = slot_start_time + datetime.timedelta(hours=1)
        
        # Check for existing bookings in this time slot
        existing_booking = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.status.in_(["confirmed", "pending_approval"]),
            Booking.start_time < slot_end_time,
            Booking.end_time > slot_start_time
        ).first()
        
        slot_info = {
            "time": time_str,
            "status": "available",
            "booking_id": None,
            "booked_by_current_user": False
        }
        
        if existing_booking:
            slot_info["status"] = existing_booking.status if existing_booking.status == "pending_approval" else "booked"
            slot_info["booking_id"] = existing_booking.id
            if current_user_id and existing_booking.user_id == current_user_id:
                slot_info["booked_by_current_user"] = True
        
        available_slots.append(slot_info)
    
    return jsonify({
        "court_id": court_id,
        "date": date_str,
        "operating_hours": operating_hours,
        "available_slots": available_slots
    }), 200

@courts_bp.route("/<int:court_id>/follow", methods=["POST"])
@jwt_required()
def follow_court(court_id):
    # This would be implemented in a real application
    return jsonify({"message": f"You are now following Court {court_id}"}), 200

@courts_bp.route("/<int:court_id>/unfollow", methods=["POST"])
@jwt_required()
def unfollow_court(court_id):
    # This would be implemented in a real application
    return jsonify({"message": f"You have unfollowed Court {court_id}"}), 200
