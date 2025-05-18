from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from src.extensions import db
from src.models.waitlist import WaitlistEntry
from src.models.court import Court
from src.models.user import User
from datetime import datetime, date as DDate, time as DTime
from sqlalchemy.exc import IntegrityError

waitlist_bp = Blueprint("waitlist", __name__, url_prefix="/api/waitlist")

@waitlist_bp.route("", methods=["POST"])
@jwt_required()
def add_to_waitlist():
    """Add the current user to a waitlist for a specific court and time slot."""
    current_user_obj = get_current_user()
    data = request.get_json()

    court_id = data.get("court_id")
    date_str = data.get("date") # YYYY-MM-DD
    start_time_str = data.get("start_time") # HH:MM
    end_time_str = data.get("end_time") # HH:MM

    if not all([court_id, date_str, start_time_str, end_time_str]):
        return jsonify({"error": "Court ID, date, start time, and end time are required."}), 400

    try:
        desired_date = DDate.fromisoformat(date_str)
        desired_start_time = DTime.fromisoformat(start_time_str)
        desired_end_time = DTime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"error": "Invalid date or time format. Use YYYY-MM-DD and HH:MM."}), 400

    court = Court.query.get(court_id)
    if not court:
        return jsonify({"error": "Court not found."}), 404

    # Optional: Add checks for valid time slots based on court operating hours or standard slots
    # For now, we assume the requested time is valid in terms of format.

    # Check if a booking already exists for this slot (should ideally be done before adding to waitlist)
    # This is a basic check; a more robust system would handle overlapping times.
    from src.models.booking import Booking # Avoid circular import if possible
    existing_booking = Booking.query.filter(
        Booking.court_id == court_id,
        Booking.start_time == datetime.combine(desired_date, desired_start_time),
        Booking.end_time == datetime.combine(desired_date, desired_end_time),
        Booking.status.in_(["confirmed", "pending_approval"])
    ).first()

    if existing_booking:
         # If a booking exists, the slot is not truly unavailable for waitlisting.
         # This scenario might indicate a UI issue where waitlist is offered for booked slots.
         # However, if the intent is to waitlist for *any* opening, this check might be different.
         # For now, let's allow waitlisting even if booked, assuming user wants to be notified of cancellations.
         pass # Or return an error if waitlisting is only for truly empty slots
         # return jsonify({"error": "This slot is already booked or pending approval."}), 409


    new_waitlist_entry = WaitlistEntry(
        user_id=current_user_obj.id,
        court_id=court_id,
        desired_date=desired_date,
        desired_start_time=desired_start_time,
        desired_end_time=desired_end_time,
        status="active"
    )

    try:
        db.session.add(new_waitlist_entry)
        db.session.commit()
        return jsonify({
            "message": "Added to waitlist successfully.",
            "waitlist_entry": new_waitlist_entry.to_dict()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "You are already on the waitlist for this slot."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error adding to waitlist.", "details": str(e)}), 500


@waitlist_bp.route("", methods=["GET"])
@jwt_required()
def get_user_waitlist_entries():
    """Get waitlist entries for the current user."""
    current_user_id = get_jwt_identity()

    # Optional query parameters for filtering (e.g., by status, court)
    status_filter = request.args.get("status")
    court_id_filter = request.args.get("court_id", type=int)

    query = WaitlistEntry.query.filter_by(user_id=current_user_id)

    if status_filter:
        query = query.filter(WaitlistEntry.status == status_filter)
    if court_id_filter:
        query = query.filter(WaitlistEntry.court_id == court_id_filter)

    # Order by desired date and start time
    waitlist_entries = query.order_by(WaitlistEntry.desired_date, WaitlistEntry.desired_start_time).all()

    return jsonify([entry.to_dict() for entry in waitlist_entries]), 200

@waitlist_bp.route("/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def remove_from_waitlist(entry_id):
    """Remove a waitlist entry for the current user."""
    current_user_id = get_jwt_identity()

    waitlist_entry = WaitlistEntry.query.get(entry_id)

    if not waitlist_entry:
        return jsonify({"message": "Waitlist entry not found."}), 404

    # Ensure the user owns the waitlist entry or is an admin (optional admin check)
    if waitlist_entry.user_id != int(current_user_id):
        # Optional: Add admin check here if needed
        # user = User.query.get(current_user_id)
        # if user.role != 'admin':
        return jsonify({"message": "Unauthorized to remove this waitlist entry."}), 403

    try:
        db.session.delete(waitlist_entry)
        db.session.commit()
        return jsonify({"message": "Waitlist entry removed successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error removing waitlist entry.", "details": str(e)}), 500

# TODO: Add routes for notifying users when a slot becomes available, etc.
