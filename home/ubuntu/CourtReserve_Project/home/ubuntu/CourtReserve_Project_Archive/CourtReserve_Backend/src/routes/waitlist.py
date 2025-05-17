from flask import Blueprint, request, jsonify
from src.models.waitlist import WaitlistEntry
from src.models.user import User
from src.models.court import Court
from src.extensions import db, socketio # db और socketio को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

waitlist_bp = Blueprint("waitlist", __name__)

@waitlist_bp.route("", methods=["POST"])
@jwt_required()
def add_to_waitlist():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    court_id = data.get("court_id")
    desired_date_str = data.get("desired_date") # YYYY-MM-DD
    desired_start_time_str = data.get("desired_start_time") # HH:MM:SS or HH:MM
    desired_end_time_str = data.get("desired_end_time") # HH:MM:SS or HH:MM

    if not all([court_id, desired_date_str, desired_start_time_str, desired_end_time_str]):
        return jsonify({"message": "Court ID, desired date, start time, and end time are required"}), 400

    try:
        desired_date = datetime.datetime.strptime(desired_date_str, "%Y-%m-%d").date()
        desired_start_time = datetime.datetime.strptime(desired_start_time_str, "%H:%M:%S").time() if len(desired_start_time_str) > 5 else datetime.datetime.strptime(desired_start_time_str, "%H:%M").time()
        desired_end_time = datetime.datetime.strptime(desired_end_time_str, "%H:%M:%S").time() if len(desired_end_time_str) > 5 else datetime.datetime.strptime(desired_end_time_str, "%H:%M").time()
    except ValueError as e:
        return jsonify({"message": f"Invalid date or time format: {e}"}), 400

    if desired_start_time >= desired_end_time:
        return jsonify({"message": "Desired start time must be before end time"}), 400

    # कोर्ट की वैधता की जाँच करें
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    
    # जाँच करें कि क्या यूज़र पहले से ही इस स्लॉट के लिए वेटलिस्ट में है
    existing_entry = WaitlistEntry.query.filter_by(
        user_id=current_user_id,
        court_id=court_id,
        desired_date=desired_date,
        desired_start_time=desired_start_time
    ).first()
    if existing_entry:
        return jsonify({"message": "You are already on the waitlist for this slot.", "waitlist_entry": existing_entry.to_dict()}), 409

    new_entry = WaitlistEntry(
        user_id=current_user_id,
        court_id=court_id,
        desired_date=desired_date,
        desired_start_time=desired_start_time,
        desired_end_time=desired_end_time,
        status="active"
    )

    try:
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Successfully added to waitlist", "waitlist_entry": new_entry.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        # यूनिक कंस्ट्रेंट वायलेशन के लिए विशेष हैंडलिंग
        if "UniqueViolation" in str(e) or "UNIQUE constraint failed" in str(e):
             return jsonify({"message": "You are already on the waitlist for this slot (constraint violation)."}), 409
        return jsonify({"message": "Error adding to waitlist", "error": str(e)}), 500

@waitlist_bp.route("", methods=["GET"])
@jwt_required()
def get_user_waitlist_entries():
    current_user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = WaitlistEntry.query.filter_by(user_id=current_user_id, status="active").order_by(WaitlistEntry.created_at.desc())
    
    paginated_entries = query.paginate(page=page, per_page=per_page, error_out=False)
    entries_data = [entry.to_dict() for entry in paginated_entries.items]

    return jsonify({
        "message": "Active waitlist entries retrieved successfully",
        "waitlist_entries": entries_data,
        "total_pages": paginated_entries.pages,
        "current_page": paginated_entries.page,
        "total_entries": paginated_entries.total
    }), 200

@waitlist_bp.route("/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def remove_from_waitlist(entry_id):
    current_user_id = get_jwt_identity()
    entry = WaitlistEntry.query.get(entry_id)

    if not entry:
        return jsonify({"message": "Waitlist entry not found"}), 404

    if entry.user_id != current_user_id:
        return jsonify({"message": "Unauthorized to remove this waitlist entry"}), 403

    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Successfully removed from waitlist"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error removing from waitlist", "error": str(e)}), 500

# वेटलिस्ट स्लॉट उपलब्ध होने पर यूज़र को सूचित करने का लॉजिक
# यह आमतौर पर तब ट्रिगर होगा जब कोई बुकिंग कैंसिल हो जाती है।
# बुकिंग कैंसलेशन लॉजिक में, हम संबंधित वेटलिस्ट एंट्रीज़ की जाँच करेंगे
# और यदि कोई मेल खाता है, तो यूज़र को सूचित करेंगे (SocketIO और Notification मॉडल के माध्यम से)।
# उदा. (bookings.py में cancel_booking के अंदर):
# if booking_was_approved_and_cancelled:
#   check_waitlist_and_notify(booking.court_id, booking.start_time.date(), booking.start_time.time())

def check_waitlist_and_notify(court_id, cancelled_date, cancelled_start_time):
    # इस स्लॉट के लिए वेटलिस्ट एंट्रीज़ खोजें
    waitlist_entries = WaitlistEntry.query.filter_by(
        court_id=court_id,
        desired_date=cancelled_date,
        desired_start_time=cancelled_start_time,
        status="active"
    ).order_by(WaitlistEntry.created_at.asc()).all() # FIFO

    for entry in waitlist_entries:
        # यूज़र को सूचित करें
        user_to_notify = User.query.get(entry.user_id)
        court_info = Court.query.get(entry.court_id)
        if user_to_notify and court_info:
            notification_content = f"A slot has opened up for {court_info.name} on {entry.desired_date.strftime('%Y-%m-%d')} at {entry.desired_start_time.strftime('%H:%M')}! Book now."
            
            from src.models.notification import Notification
            new_notification = Notification(
                user_id=entry.user_id,
                type="waitlist_slot_available",
                related_entity_id=entry.id, # वेटलिस्ट एंट्री ID
                related_entity_type="waitlist_entry",
                content=notification_content
            )
            db.session.add(new_notification)
            entry.status = "notified" # स्थिति को अपडेट करें
            db.session.commit()

            socketio.emit("new_notification", new_notification.to_dict(), room=f"user_{entry.user_id}", namespace="/notifications")
            socketio.emit("waitlist_slot_notification", 
                          {"message": notification_content, "court_id": court_id, "date": entry.desired_date.isoformat(), "time": entry.desired_start_time.isoformat()},
                          room=f"user_{entry.user_id}", namespace="/notifications") # एक अधिक विशिष्ट इवेंट भी
            
            # वैकल्पिक: केवल पहले यूज़र को सूचित करें और लूप को ब्रेक करें, या सभी को सूचित करें
            # break # यदि केवल पहले यूज़र को सूचित करना है
    pass

