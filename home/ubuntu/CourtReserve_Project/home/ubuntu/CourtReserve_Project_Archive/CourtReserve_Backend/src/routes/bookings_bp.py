from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from src.models import db, Booking, Court, User, Notification # Assuming User, Court, Notification models are in src.models
from datetime import datetime, timedelta, date as DDate
from sqlalchemy import or_

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/api/bookings")

def create_notification(user_id, message, link=None, type=None):
    """Helper function to create and save a notification."""
    notification = Notification(user_id=user_id, message=message, link=link, type=type)
    db.session.add(notification)
    # db.session.commit() # Commit should happen at the end of the request or a logical unit of work
    return notification

@bookings_bp.route("/request", methods=["POST"])
@jwt_required()
def request_booking():
    data = request.get_json()
    current_user_obj = get_current_user()

    court_id = data.get("court_id")
    date_str = data.get("date") # YYYY-MM-DD
    time_str = data.get("time") # HH:MM
    user_note = data.get("note")

    if not all([court_id, date_str, time_str]):
        return jsonify({"error": "Court ID, date, and time are required."}), 400

    try:
        target_date = DDate.fromisoformat(date_str)
        slot_start_time = datetime.strptime(time_str, "%H:%M").time()
        booking_start_datetime = datetime.combine(target_date, slot_start_time)
        booking_end_datetime = booking_start_datetime + timedelta(hours=1) # Standard 1-hour slots
    except ValueError:
        return jsonify({"error": "Invalid date or time format."}), 400

    court = Court.query.get(court_id)
    if not court:
        return jsonify({"error": "Court not found."}), 404

    # Check court operating hours (simplified)
    operating_hours_today = court.operating_hours.get("default", ["07:00", "22:00"])
    open_time = datetime.strptime(operating_hours_today[0], "%H:%M").time()
    close_time = datetime.strptime(operating_hours_today[1], "%H:%M").time()

    if not (open_time <= booking_start_datetime.time() < close_time and 
            open_time < booking_end_datetime.time() <= close_time):
        return jsonify({"error": "Booking time is outside of court operating hours."}), 400
    
    if booking_start_datetime < datetime.utcnow():
         return jsonify({"error": "Cannot book slots in the past."}), 400

    # Check for conflicting bookings
    conflicting_booking = Booking.query.filter(
        Booking.court_id == court_id,
        Booking.start_time < booking_end_datetime, # New booking starts before old one ends
        Booking.end_time > booking_start_datetime,  # New booking ends after old one starts
        Booking.status.in_(["confirmed", "pending_approval"])
    ).first()

    if conflicting_booking:
        return jsonify({"error": "This time slot is already booked or pending approval."}), 409

    new_booking = Booking(
        user_id=current_user_obj.id,
        court_id=court_id,
        start_time=booking_start_datetime,
        end_time=booking_end_datetime,
        user_note=user_note,
        status="pending_approval"
    )
    db.session.add(new_booking)
    
    # Notify court responsible users
    # Assuming court.approving_trainers are the court_responsible users for this court
    # In a more complex system, you might have a dedicated CourtManager role or similar
    notified_responsibles = set()
    for responsible_user in court.approving_trainers: # This relationship needs to be correctly defined and populated
        if responsible_user.id not in notified_responsibles:
            create_notification(
                user_id=responsible_user.id,
                message=f"New booking request for {court.name} on {date_str} at {time_str} by {current_user_obj.full_name or current_user_obj.email}.",
                link=f"/admin/bookings/{new_booking.id}", # Example link
                type="booking_request"
            )
            notified_responsibles.add(responsible_user.id)
    
    # If no specific approving_trainers, perhaps notify a general admin or fallback
    if not court.approving_trainers:
        # This logic needs refinement: who to notify if no direct court responsible?
        # For now, let's assume there's always someone or this needs to be handled by system admins.
        pass 

    db.session.commit()

    return jsonify({
        "message": "Booking request created successfully. Awaiting approval.",
        "booking": new_booking.to_dict()
    }), 201

@bookings_bp.route("", methods=["GET"])
@jwt_required()
def get_user_bookings():
    current_user_obj = get_current_user()
    status_filter = request.args.get("status")
    period_filter = request.args.get("period") # upcoming, past

    query = Booking.query.filter_by(user_id=current_user_obj.id)

    if status_filter:
        query = query.filter(Booking.status == status_filter)
    
    now = datetime.utcnow()
    if period_filter == "upcoming":
        query = query.filter(Booking.start_time >= now)
    elif period_filter == "past":
        query = query.filter(Booking.start_time < now)

    bookings = query.order_by(Booking.start_time.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@bookings_bp.route("/court/<int:court_id>", methods=["GET"])
@jwt_required()
def get_court_bookings(court_id):
    current_user_obj = get_current_user()
    court = Court.query.get_or_404(court_id)

    # Check if current user is a responsible for this court
    if current_user_obj.role != "court_responsible" or court not in current_user_obj.managed_courts:
        # A more specific check might be needed if managed_courts is not directly on User or if role isn't enough
        # For now, a simple role check or a check against court.approving_trainers
        is_responsible = False
        for trainer in court.approving_trainers:
            if trainer.id == current_user_obj.id:
                is_responsible = True
                break
        if not is_responsible and current_user_obj.role != "admin": # Allow admin to see all
             return jsonify({"error": "You are not authorized to view bookings for this court."}), 403

    status_filter = request.args.get("status")
    date_filter_str = request.args.get("date")

    query = Booking.query.filter_by(court_id=court_id)

    if status_filter:
        query = query.filter(Booking.status == status_filter)
    
    if date_filter_str:
        try:
            target_date = DDate.fromisoformat(date_filter_str)
            day_start = datetime.combine(target_date, datetime.min.time())
            day_end = datetime.combine(target_date, datetime.max.time())
            query = query.filter(Booking.start_time >= day_start, Booking.start_time <= day_end)
        except ValueError:
            return jsonify({"error": "Invalid date format for filter. Use YYYY-MM-DD."}), 400

    bookings = query.order_by(Booking.start_time.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@bookings_bp.route("/<int:booking_id>/approve", methods=["POST"])
@jwt_required()
def approve_booking(booking_id):
    current_user_obj = get_current_user()
    booking = Booking.query.get_or_404(booking_id)
    court = Court.query.get_or_404(booking.court_id)

    is_responsible = False
    for trainer in court.approving_trainers:
        if trainer.id == current_user_obj.id:
            is_responsible = True
            break
    if not is_responsible and current_user_obj.role != "admin":
        return jsonify({"error": "You are not authorized to approve bookings for this court."}), 403

    if booking.status != "pending_approval":
        return jsonify({"error": "Booking is not pending approval."}), 400

    booking.status = "confirmed"
    booking.approved_by_user_id = current_user_obj.id
    
    # Notify the user who made the booking
    create_notification(
        user_id=booking.user_id,
        message=f"Your booking for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been approved.",
        link=f"/my-bookings/{booking.id}",
        type="booking_approved"
    )
    db.session.commit()
    return jsonify({"message": "Booking approved successfully.", "booking": booking.to_dict()}), 200

@bookings_bp.route("/<int:booking_id>/reject", methods=["POST"])
@jwt_required()
def reject_booking(booking_id):
    current_user_obj = get_current_user()
    booking = Booking.query.get_or_404(booking_id)
    court = Court.query.get_or_404(booking.court_id)
    data = request.get_json()
    rejection_reason = data.get("reason", "No reason provided.")

    is_responsible = False
    for trainer in court.approving_trainers:
        if trainer.id == current_user_obj.id:
            is_responsible = True
            break
    if not is_responsible and current_user_obj.role != "admin":
        return jsonify({"error": "You are not authorized to reject bookings for this court."}), 403

    if booking.status != "pending_approval":
        return jsonify({"error": "Booking is not pending approval."}), 400

    booking.status = "rejected"
    booking.approved_by_user_id = current_user_obj.id
    booking.court_responsible_note = rejection_reason

    create_notification(
        user_id=booking.user_id,
        message=f"Your booking request for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been rejected. Reason: {rejection_reason}",
        link=f"/my-bookings/{booking.id}",
        type="booking_rejected"
    )
    db.session.commit()
    return jsonify({"message": "Booking rejected.", "booking": booking.to_dict()}), 200

@bookings_bp.route("/<int:booking_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_booking(booking_id):
    current_user_obj = get_current_user()
    booking = Booking.query.get_or_404(booking_id)
    court = Court.query.get_or_404(booking.court_id)

    can_cancel = False
    is_court_responsible_for_this_court = False
    for trainer in court.approving_trainers:
        if trainer.id == current_user_obj.id:
            is_court_responsible_for_this_court = True
            break

    if booking.user_id == current_user_obj.id:
        # User is cancelling their own booking
        if booking.status not in ["confirmed", "pending_approval"]:
             return jsonify({"error": "Booking cannot be cancelled in its current state."}), 400
        # 1-hour cancellation policy
        if booking.start_time - datetime.utcnow() < timedelta(hours=1):
            if not is_court_responsible_for_this_court and current_user_obj.role != "admin": # Court responsible or admin can override
                return jsonify({"error": "Cannot cancel booking less than 1 hour before start time."}), 403
        can_cancel = True
    elif is_court_responsible_for_this_court or current_user_obj.role == "admin":
        # Court responsible or admin is cancelling
        if booking.status not in ["confirmed", "pending_approval"]:
             return jsonify({"error": "Booking cannot be cancelled in its current state."}), 400
        can_cancel = True
    else:
        return jsonify({"error": "You are not authorized to cancel this booking."}), 403

    if not can_cancel:
         return jsonify({"error": "Cancellation conditions not met."}), 400 # Should be caught by earlier checks

    original_status = booking.status
    booking.status = "cancelled"
    # Note: We might want different statuses like 'cancelled_by_user', 'cancelled_by_responsible'
    # For now, a single 'cancelled' status is used.

    # Notify original booker if cancelled by someone else (court responsible/admin)
    if booking.user_id != current_user_obj.id:
        create_notification(
            user_id=booking.user_id,
            message=f"Your booking for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been cancelled by the court management.",
            link=f"/my-bookings/{booking.id}",
            type="booking_cancelled_by_admin"
        )
    
    # Notify followers of the court that a slot has become available
    # Only if the booking was previously 'confirmed' or 'pending_approval' and now 'cancelled'
    if original_status in ["confirmed", "pending_approval"]:
        for follower in court.followers:
            if follower.id != booking.user_id: # Don't notify the person whose booking it was, if they cancelled it themselves
                create_notification(
                    user_id=follower.id,
                    message=f"A slot has become available at {court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')}.",
                    link=f"/courts/{court.id}/availability?date={booking.start_time.strftime('%Y-%m-%d')}",
                    type="slot_available"
                )

db.session.commit()
    return jsonify({"message": "Booking cancelled successfully.", "booking": booking.to_dict()}), 200

