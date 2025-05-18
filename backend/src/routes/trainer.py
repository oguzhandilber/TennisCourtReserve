from flask import Blueprint, request, jsonify
from src.models.booking import Booking
from src.models.court import Court
from src.models.user import User
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

trainer_bp = Blueprint("trainer", __name__)

@trainer_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_trainer_bookings():
    """Get bookings for courts managed by the trainer/court responsible."""
    current_user_id = get_jwt_identity()
    
    # Check if user is a court responsible
    user = User.query.get(current_user_id)
    if not user or user.role != "court_responsible":
        return jsonify({"message": "Unauthorized. Only court responsible users can access this endpoint"}), 403
    
    # Get courts managed by this court responsible
    managed_courts = Court.query.join(Court.court_trainers).filter_by(trainer_user_id=current_user_id).all()
    if not managed_courts:
        return jsonify({"message": "You are not responsible for any courts"}), 404
    
    managed_court_ids = [court.id for court in managed_courts]
    
    # Optional query parameters
    status = request.args.get("status")
    date_str = request.args.get("date")
    
    query = Booking.query.filter(Booking.court_id.in_(managed_court_ids))
    
    # Filter by status if provided
    if status:
        query = query.filter(Booking.status == status)
    
    # Filter by date if provided
    if date_str:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            next_date = date_obj + datetime.timedelta(days=1)
            query = query.filter(
                Booking.start_time >= datetime.datetime.combine(date_obj, datetime.time.min),
                Booking.start_time < datetime.datetime.combine(next_date, datetime.time.min)
            )
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Order by start time
    query = query.order_by(Booking.start_time)
    
    bookings = query.all()
    bookings_data = [booking.to_dict() for booking in bookings]
    
    return jsonify(bookings_data), 200

@trainer_bp.route("/bookings/<int:booking_id>/approve", methods=["PUT"])
@jwt_required()
def approve_booking(booking_id):
    """Approve a pending booking request."""
    current_user_id = get_jwt_identity()
    
    # Check if user is a court responsible
    user = User.query.get(current_user_id)
    if not user or user.role != "court_responsible":
        return jsonify({"message": "Unauthorized. Only court responsible users can approve bookings"}), 403
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    # Check if the booking is for a court managed by this court responsible
    court = Court.query.get(booking.court_id)
    if not court or not any(trainer.trainer_user_id == current_user_id for trainer in court.court_trainers):
        return jsonify({"message": "Unauthorized. You are not responsible for this court"}), 403
    
    # Check if the booking is in a pending state
    if booking.status != "pending_approval":
        return jsonify({"message": f"Cannot approve a booking with status: {booking.status}"}), 400
    
    # Update booking status
    booking.status = "confirmed"
    booking.approved_by_user_id = current_user_id
    booking.updated_at = datetime.datetime.utcnow()
    
    db.session.commit()
    
    # TODO: Notify the user who made the booking
    
    return jsonify({
        "message": "Booking approved successfully.",
        "booking": booking.to_dict()
    }), 200

@trainer_bp.route("/bookings/<int:booking_id>/decline", methods=["PUT"])
@jwt_required()
def decline_booking(booking_id):
    """Decline a pending booking request."""
    current_user_id = get_jwt_identity()
    
    # Check if user is a court responsible
    user = User.query.get(current_user_id)
    if not user or user.role != "court_responsible":
        return jsonify({"message": "Unauthorized. Only court responsible users can decline bookings"}), 403
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    # Check if the booking is for a court managed by this court responsible
    court = Court.query.get(booking.court_id)
    if not court or not any(trainer.trainer_user_id == current_user_id for trainer in court.court_trainers):
        return jsonify({"message": "Unauthorized. You are not responsible for this court"}), 403
    
    # Check if the booking is in a pending state
    if booking.status != "pending_approval":
        return jsonify({"message": f"Cannot decline a booking with status: {booking.status}"}), 400
    
    # Get reason from request body
    data = request.get_json() or {}
    reason = data.get("reason", "")
    
    # Update booking status
    booking.status = "rejected"
    booking.approved_by_user_id = current_user_id
    booking.court_responsible_note = reason
    booking.updated_at = datetime.datetime.utcnow()
    
    db.session.commit()
    
    # TODO: Notify the user who made the booking, including reason if provided
    
    return jsonify({
        "message": "Booking declined.",
        "booking": booking.to_dict()
    }), 200
