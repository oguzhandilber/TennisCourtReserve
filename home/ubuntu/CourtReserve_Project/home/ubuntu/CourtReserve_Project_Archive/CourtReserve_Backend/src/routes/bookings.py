from flask import Blueprint, request, jsonify
from src.models.booking import Booking
from src.models.court import Court
from src.models.user import User
from src.extensions import db, socketio # db और socketio को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("", methods=["POST"])
@jwt_required()
def request_booking():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    court_id = data.get("court_id")
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    user_notes = data.get("user_notes")

    if not all([court_id, start_time_str, end_time_str]):
        return jsonify({"message": "Court ID, start time, and end time are required"}), 400

    try:
        start_time = datetime.datetime.fromisoformat(start_time_str)
        end_time = datetime.datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"message": "Invalid datetime format. Use ISO format."}), 400

    if start_time >= end_time:
        return jsonify({"message": "Start time must be before end time"}), 400
    
    if start_time < datetime.datetime.utcnow() + datetime.timedelta(minutes=5): # कम से कम 5 मिनट भविष्य में
        return jsonify({"message": "Booking must be at least 5 minutes in the future"}), 400

    # 3 सप्ताह की बुकिंग सीमा की जाँच करें
    if start_time > datetime.datetime.utcnow() + datetime.timedelta(weeks=3):
        return jsonify({"message": "Cannot book more than 3 weeks in advance"}), 400

    # कोर्ट की वैधता की जाँच करें
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404

    # स्लॉट उपलब्धता की जाँच करें (यह courts.py में get_court_availability के समान लॉजिक है)
    existing_booking = Booking.query.filter(
        Booking.court_id == court_id,
        Booking.status.in_(["approved", "pending"]), # केवल अप्रूव्ड या पेंडिंग बुकिंग्स स्लॉट को ब्लॉक करती हैं
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    if existing_booking:
        return jsonify({"message": "Selected time slot is already booked or pending approval"}), 409
    
    # उपयोगकर्ता की पेंडिंग बुकिंग्स की संख्या की जाँच करें
    pending_user_bookings_count = Booking.query.filter_by(user_id=current_user_id, status="pending").count()
    if pending_user_bookings_count >= 20:
        return jsonify({"message": "You have reached the maximum limit of 20 pending booking requests."}), 403

    new_booking = Booking(
        user_id=current_user_id,
        court_id=court_id,
        start_time=start_time,
        end_time=end_time,
        user_notes=user_notes,
        status="pending" # डिफ़ॉल्ट स्थिति
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
        
        # ट्रेनर(रों) को सूचित करें (SocketIO के माध्यम से)
        # पहले इस कोर्ट के लिए जिम्मेदार ट्रेनर्स को खोजें
        # यह Court_Trainers एसोसिएशन टेबल के माध्यम से किया जाएगा
        # अभी के लिए, हम मानते हैं कि हमारे पास ट्रेनर IDs की एक सूची है
        # उदा. court.approving_trainers से ट्रेनर IDs प्राप्त करें
        # for trainer_user in court.approving_trainers:
        #    socketio.emit("new_booking_request", new_booking.to_dict(), room=f"user_{trainer_user.id}")
        #    # एक Notification ऑब्जेक्ट भी बनाएँ

        return jsonify({"message": "Booking requested successfully", "booking": new_booking.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error requesting booking", "error": str(e)}), 500

@bookings_bp.route("", methods=["GET"])
@jwt_required()
def get_user_bookings():
    current_user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status_filter = request.args.get("status")

    query = Booking.query.filter_by(user_id=current_user_id).order_by(Booking.start_time.desc())
    if status_filter:
        query = query.filter(Booking.status == status_filter)
        
    paginated_bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    bookings_data = [booking.to_dict() for booking in paginated_bookings.items]

    return jsonify({
        "message": "Bookings retrieved successfully",
        "bookings": bookings_data,
        "total_pages": paginated_bookings.pages,
        "current_page": paginated_bookings.page,
        "total_bookings": paginated_bookings.total
    }), 200

@bookings_bp.route("/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking_details(booking_id):
    current_user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    # सुनिश्चित करें कि यूज़र अपनी बुकिंग या ट्रेनर संबंधित बुकिंग देख रहा है
    # अभी के लिए, केवल यूज़र अपनी बुकिंग देख सकता है
    if booking.user_id != current_user_id:
        # यदि ट्रेनर को भी देखने की अनुमति है, तो यहाँ अतिरिक्त लॉजिक जोड़ें
        # उदा. if not (booking.user_id == current_user_id or is_trainer_for_court(current_user_id, booking.court_id)):
        return jsonify({"message": "Unauthorized to view this booking"}), 403

    return jsonify(booking.to_dict()), 200

@bookings_bp.route("/<int:booking_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_booking(booking_id):
    current_user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.user_id != current_user_id:
        return jsonify({"message": "Unauthorized to cancel this booking"}), 403 # केवल बुकिंग करने वाला यूज़र ही कैंसिल कर सकता है

    if booking.status not in ["pending", "approved"]:
        return jsonify({"message": f"Cannot cancel booking with status: {booking.status}"}), 400
    
    # यहाँ कैंसलेशन पॉलिसी लॉजिक जोड़ा जा सकता है (e.g., बुकिंग से X घंटे पहले तक)

    booking.status = "cancelled_by_user"
    try:
        db.session.commit()
        # यदि यह एक अप्रूव्ड बुकिंग थी, तो वेटलिस्ट में यूज़र्स को सूचित करें (यदि लागू हो)
        # ट्रेनर को भी सूचित करें
        # socketio.emit("booking_cancelled", booking.to_dict(), room=f"user_{booking.trainer_id}") # यदि ट्रेनर असाइन किया गया था
        return jsonify({"message": "Booking cancelled successfully", "booking": booking.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error cancelling booking", "error": str(e)}), 500

