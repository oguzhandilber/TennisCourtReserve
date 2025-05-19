from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from src.models import db, Booking, Court, User, Notification, WaitlistEntry # Assuming User, Court, Notification, WaitlistEntry models are in src.models
from datetime import datetime, timedelta, date as DDate, time as DTime
from sqlalchemy import or_

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/api/bookings")

def create_notification(user_id, content, related_id=None, type=None): # Changed 'message' to 'content', 'link' to 'related_id'
    """Helper function to create and save a notification."""
    # Ensure 'type' is used for the notification type, and 'related_id' for linking
    notification = Notification(user_id=user_id, content=content, related_id=related_id, type=type)
    db.session.add(notification)
    # db.session.commit() # Commit should happen at the end of the request or a logical unit of work
    return notification

@bookings_bp.route("/request", methods=["POST"])
@jwt_required()
def request_booking():
    data = request.get_json()
    current_user_obj = get_current_user()

    errors = {}
    court_id = data.get("court_id")
    date_str = data.get("date") # YYYY-MM-DD
    time_str = data.get("time") # HH:MM
    user_note = data.get("note") # Optional

    if not court_id:
        errors["court_id"] = "Court ID is required."
    elif not isinstance(court_id, int):
        try:
            court_id = int(court_id)
        except ValueError:
            errors["court_id"] = "Court ID must be an integer."
            
    if not date_str:
        errors["date"] = "Date is required."
    if not time_str:
        errors["time"] = "Time is required."

    if user_note and len(user_note) > 500: # Example max length for user_note
        errors["user_note"] = "Note cannot exceed 500 characters."

    if errors:
        return jsonify({"message": "Input validation failed", "errors": errors}), 400

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
    notified_responsibles = set()
    for responsible_user in court.approving_trainers:
        if responsible_user.id not in notified_responsibles:
            create_notification(
                user_id=responsible_user.id,
                content=f"New booking request for {court.name} on {date_str} at {time_str} by {current_user_obj.full_name or current_user_obj.email}.",
                related_id=new_booking.id, # Using related_id for the booking ID
                type="booking_request"
            )
            notified_responsibles.add(responsible_user.id)

    if not court.approving_trainers:
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
        statuses = [status.strip() for status in status_filter.split(',')]
        query = query.filter(Booking.status.in_(statuses))

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

    if current_user_obj.role != "court_responsible" or court not in current_user_obj.managed_courts:
        is_responsible = False
        for trainer in court.approving_trainers:
            if trainer.id == current_user_obj.id:
                is_responsible = True
                break
        if not is_responsible and current_user_obj.role != "admin":
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

    create_notification(
        user_id=booking.user_id,
        content=f"Your booking for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been approved.",
        related_id=booking.id,
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
        content=f"Your booking request for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been rejected. Reason: {rejection_reason}",
        related_id=booking.id,
        type="booking_rejected"
    )
    db.session.commit()
    notify_waitlisted_users(booking)
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
        if booking.status not in ["confirmed", "pending_approval"]:
             return jsonify({"error": "Booking cannot be cancelled in its current state."}), 400
        if booking.start_time - datetime.utcnow() < timedelta(hours=1):
            if not is_court_responsible_for_this_court and current_user_obj.role != "admin":
                return jsonify({"error": "Cannot cancel booking less than 1 hour before start time."}), 403
        can_cancel = True
    elif is_court_responsible_for_this_court or current_user_obj.role == "admin":
        if booking.status not in ["confirmed", "pending_approval"]:
             return jsonify({"error": "Booking cannot be cancelled in its current state."}), 400
        can_cancel = True
    else:
        return jsonify({"error": "You are not authorized to cancel this booking."}), 403

    if not can_cancel:
         return jsonify({"error": "Cancellation conditions not met."}), 400

    original_status = booking.status
    booking.status = "cancelled"

    if booking.user_id != current_user_obj.id:
        create_notification(
            user_id=booking.user_id,
            content=f"Your booking for {booking.court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')} has been cancelled by the court management.",
            related_id=booking.id,
            type="booking_cancelled_by_admin"
        )

    if original_status in ["confirmed", "pending_approval"]:
        for follower in court.followers:
            if follower.id != booking.user_id:
                create_notification(
                    user_id=follower.id,
                    content=f"A slot has become available at {court.name} on {booking.start_time.strftime('%Y-%m-%d at %H:%M')}.",
                    related_id=court.id, # Link to court for slot available
                    type="slot_available"
                )

    db.session.commit()
    notify_waitlisted_users(booking)
    return jsonify({"message": "Booking cancelled successfully.", "booking": booking.to_dict()}), 200

def notify_waitlisted_users(booking):
    """Notify users on the waitlist for a specific booking slot."""
    waitlist_entries = WaitlistEntry.query.filter(
        WaitlistEntry.court_id == booking.court_id,
        WaitlistEntry.desired_date == booking.start_time.date(),
        WaitlistEntry.desired_start_time == booking.start_time.time(),
        WaitlistEntry.desired_end_time == booking.end_time.time(),
        WaitlistEntry.status == "active"
    ).all()

    if not waitlist_entries:
        return

    court = Court.query.get(booking.court_id)
    if not court:
        return

    slot_time_str = booking.start_time.strftime('%Y-%m-%d at %H:%M')
    message_content = f"A slot has become available at {court.name} on {slot_time_str}!"
    # Link to the court availability page, related_id should be court_id for this type of notification
    # Or related_id could be the booking.id if the notification is about a specific cancelled booking slot becoming free.
    # For now, let's use court.id as related_id for a general "slot_available" notification for the court.
    # The link in the notification content already points to the specific availability.

    for entry in waitlist_entries:
        if entry.user_id != booking.user_id: # Don't notify the user whose booking it was
            create_notification(
                user_id=entry.user_id,
                content=message_content, # The message already contains date/time
                related_id=court.id, # Relate to the court
                type="waitlist_available"
            )
            # entry.status = 'notified' # Consider if status should change
    # db.session.commit() # Commits are handled by the calling route
