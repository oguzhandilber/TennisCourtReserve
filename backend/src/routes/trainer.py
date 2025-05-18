from flask import Blueprint, request, jsonify
from src.models.booking import Booking
from src.models.court import Court
from src.extensions import db, socketio # db और socketio को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity

trainer_bp = Blueprint("trainer", __name__)

# यह एंडपॉइंट ट्रेनर को उनके द्वारा मैनेज किए जा रहे कोर्ट्स के लिए बुकिंग अनुरोधों को देखने की अनुमति देगा
@trainer_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_trainer_bookings():
    current_user_id = get_jwt_identity()
    # पहले जाँचें कि क्या यूज़र एक ट्रेनर है
    from src.models.user import User
    trainer_user = User.query.get(current_user_id)
    if not trainer_user or trainer_user.role != "trainer":
        return jsonify({"message": "Unauthorized. Only trainers can access this endpoint."}), 403

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status_filter = request.args.get("status", "pending") # डिफ़ॉल्ट रूप से पेंडिंग अनुरोध दिखाएँ

    # ट्रेनर द्वारा मैनेज किए जा रहे कोर्ट्स के लिए बुकिंग्स प्राप्त करें
    # यह Court_Trainers एसोसिएशन टेबल के माध्यम से किया जाएगा
    # query = Booking.query.join(Court).join(Court.approving_trainers.and_(User.id == current_user_id))
    # उपरोक्त जॉइन SQLAlchemy में थोड़ा जटिल हो सकता है, एक सरल तरीका है पहले ट्रेनर के कोर्ट्स प्राप्त करना
    
    managed_court_ids = [court.id for court in trainer_user.managed_courts]
    if not managed_court_ids:
        return jsonify({"message": "You are not managing any courts.", "bookings": [], "total_pages": 0, "current_page": 1, "total_bookings": 0}), 200

    query = Booking.query.filter(Booking.court_id.in_(managed_court_ids))
    
    if status_filter:
        query = query.filter(Booking.status == status_filter)
    
    query = query.order_by(Booking.created_at.asc()) # सबसे पुराने अनुरोध पहले
        
    paginated_bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    bookings_data = [booking.to_dict() for booking in paginated_bookings.items]

    return jsonify({
        "message": f"{status_filter.capitalize()} bookings for managed courts retrieved successfully",
        "bookings": bookings_data,
        "total_pages": paginated_bookings.pages,
        "current_page": paginated_bookings.page,
        "total_bookings": paginated_bookings.total
    }), 200

@trainer_bp.route("/bookings/<int:booking_id>/approve", methods=["PUT"])
@jwt_required()
def approve_booking(booking_id):
    current_user_id = get_jwt_identity()
    from src.models.user import User
    trainer_user = User.query.get(current_user_id)
    if not trainer_user or trainer_user.role != "trainer":
        return jsonify({"message": "Unauthorized"}), 403

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    # जाँचें कि क्या यह ट्रेनर इस बुकिंग के कोर्ट को मैनेज करता है
    if booking.court_id not in [court.id for court in trainer_user.managed_courts]:
        return jsonify({"message": "You are not authorized to manage this booking."}), 403

    if booking.status != "pending":
        return jsonify({"message": f"Booking is not pending (current status: {booking.status})"}), 400

    booking.status = "approved"
    booking.trainer_id = current_user_id # अप्रूव करने वाले ट्रेनर को असाइन करें
    trainer_notes = request.json.get("trainer_notes")
    if trainer_notes:
        booking.trainer_notes = trainer_notes

    try:
        db.session.commit()
        # यूज़र को सूचित करें
        # socketio.emit("booking_approved", booking.to_dict(), room=f"user_{booking.user_id}")
        # Notification ऑब्जेक्ट बनाएँ
        return jsonify({"message": "Booking approved successfully", "booking": booking.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error approving booking", "error": str(e)}), 500

@trainer_bp.route("/bookings/<int:booking_id>/decline", methods=["PUT"])
@jwt_required()
def decline_booking(booking_id):
    current_user_id = get_jwt_identity()
    from src.models.user import User
    trainer_user = User.query.get(current_user_id)
    if not trainer_user or trainer_user.role != "trainer":
        return jsonify({"message": "Unauthorized"}), 403

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.court_id not in [court.id for court in trainer_user.managed_courts]:
        return jsonify({"message": "You are not authorized to manage this booking."}), 403

    if booking.status != "pending":
        return jsonify({"message": f"Booking is not pending (current status: {booking.status})"}), 400

    booking.status = "declined"
    booking.trainer_id = current_user_id
    trainer_notes = request.json.get("trainer_notes")
    if trainer_notes:
        booking.trainer_notes = trainer_notes
        
    try:
        db.session.commit()
        # यूज़र को सूचित करें
        # socketio.emit("booking_declined", booking.to_dict(), room=f"user_{booking.user_id}")
        # Notification ऑब्जेक्ट बनाएँ
        return jsonify({"message": "Booking declined successfully", "booking": booking.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error declining booking", "error": str(e)}), 500

