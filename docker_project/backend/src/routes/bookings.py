from flask import Blueprint, request, jsonify
from src.models.booking import Booking
from src.models.court import Court
from src.models.user import User
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("", methods=["GET"])
@jwt_required()
def get_user_bookings():
    """Get bookings for the current user."""
    current_user_id = get_jwt_identity()
    
    # Optional query parameters
    status = request.args.get("status")
    period = request.args.get("period")
    
    query = Booking.query.filter(Booking.user_id == current_user_id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Booking.status == status)
    
    # Filter by period if provided
    if period == "upcoming":
        query = query.filter(Booking.start_time >= datetime.datetime.utcnow())
    elif period == "past":
        query = query.filter(Booking.start_time < datetime.datetime.utcnow())
    
    # Order by start time
    query = query.order_by(Booking.start_time)
    
    bookings = query.all()
    bookings_data = [booking.to_dict() for booking in bookings]
    
    return jsonify(bookings_data), 200

@bookings_bp.route("/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking_details(booking_id):
    """Get details for a specific booking."""
    current_user_id = get_jwt_identity()
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    # Check if the user is authorized to view this booking
    if booking.user_id != current_user_id:
        # Check if the user is a court responsible for this court
        user = User.query.get(current_user_id)
        if not user or user.role != "court_responsible":
            return jsonify({"message": "Unauthorized to view this booking"}), 403
    
    return jsonify(booking.to_dict()), 200

@bookings_bp.route("/request", methods=["POST"])
@jwt_required()
def request_booking():
    """Create a new booking request."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["court_id", "date", "time"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    court_id = data.get("court_id")
    date_str = data.get("date")
    time_str = data.get("time")
    note = data.get("note", "")
    
    # Validate court exists
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    
    # Parse date and time
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
        start_time = datetime.datetime.combine(date_obj, time_obj)
        end_time = start_time + datetime.timedelta(hours=1)  # 1-hour slot
    except ValueError:
        return jsonify({"message": "Invalid date or time format"}), 400
    
    # Check if the slot is in the future
    if start_time <= datetime.datetime.utcnow():
        return jsonify({"message": "Cannot book slots in the past"}), 400
    
    # Check if the slot is already booked
    existing_booking = Booking.query.filter(
        Booking.court_id == court_id,
        Booking.status.in_(["confirmed", "pending_approval"]),
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()
    
    if existing_booking:
        return jsonify({"message": "This time slot is already booked or pending approval"}), 409
    
    # Create new booking
    new_booking = Booking(
        user_id=current_user_id,
        court_id=court_id,
        start_time=start_time,
        end_time=end_time,
        status="pending_approval",
        user_note=note
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        "message": "Booking request created successfully. Awaiting approval.",
        "booking": new_booking.to_dict()
    }), 201

@bookings_bp.route("/<int:booking_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking."""
    current_user_id = get_jwt_identity()
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    # Check if the user is authorized to cancel this booking
    user = User.query.get(current_user_id)
    is_court_responsible = user and user.role == "court_responsible"
    
    if booking.user_id != current_user_id and not is_court_responsible:
        return jsonify({"message": "Unauthorized to cancel this booking"}), 403
    
    # Check if the booking is already cancelled or completed
    if booking.status in ["cancelled", "completed"]:
        return jsonify({"message": f"Cannot cancel a booking with status: {booking.status}"}), 400
    
    # Check cancellation policy (1 hour before start time) for regular users
    if not is_court_responsible and booking.start_time <= datetime.datetime.utcnow() + datetime.timedelta(hours=1):
        return jsonify({"message": "Cannot cancel bookings less than 1 hour before start time"}), 400
    
    # Update booking status
    booking.status = "cancelled"
    booking.updated_at = datetime.datetime.utcnow()
    
    db.session.commit()
    
    # TODO: Notify followers of the court if slot becomes available
    
    return jsonify({
        "message": "Booking cancelled successfully.",
        "booking": booking.to_dict()
    }), 200
