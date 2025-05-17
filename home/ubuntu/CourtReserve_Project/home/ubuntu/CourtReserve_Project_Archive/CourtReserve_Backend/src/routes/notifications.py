from flask import Blueprint, request, jsonify
from src.models.notification import Notification
from src.models.user import User # यूज़र जानकारी के लिए
from src.extensions import db, socketio # db और socketio को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import join_room # SocketIO रूम्स के लिए
import datetime

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("", methods=["GET"])
@jwt_required()
def get_user_notifications():
    current_user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 15, type=int)

    query = Notification.query.filter_by(user_id=current_user_id).order_by(Notification.created_at.desc())
    
    paginated_notifications = query.paginate(page=page, per_page=per_page, error_out=False)
    notifications_data = [notification.to_dict() for notification in paginated_notifications.items]

    return jsonify({
        "message": "Notifications retrieved successfully",
        "notifications": notifications_data,
        "total_pages": paginated_notifications.pages,
        "current_page": paginated_notifications.page,
        "total_notifications": paginated_notifications.total
    }), 200

@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_notification_as_read(notification_id):
    current_user_id = get_jwt_identity()
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({"message": "Notification not found"}), 404

    if notification.user_id != current_user_id:
        return jsonify({"message": "Unauthorized to update this notification"}), 403

    if notification.is_read:
        return jsonify({"message": "Notification already marked as read"}), 200

    notification.is_read = True
    try:
        db.session.commit()
        return jsonify({"message": "Notification marked as read", "notification": notification.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error marking notification as read", "error": str(e)}), 500

@notifications_bp.route("/read-all", methods=["PUT"])
@jwt_required()
def mark_all_notifications_as_read():
    current_user_id = get_jwt_identity()
    
    try:
        updated_count = Notification.query.filter_by(user_id=current_user_id, is_read=False).update({"is_read": True})
        db.session.commit()
        return jsonify({"message": f"{updated_count} notifications marked as read"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error marking all notifications as read", "error": str(e)}), 500

# SocketIO इवेंट्स सूचनाओं के लिए
@socketio.on("connect", namespace="/notifications")
@jwt_required(optional=True) # कनेक्शन के लिए JWT वैकल्पिक हो सकता है
def handle_notification_connect():
    current_user_id = get_jwt_identity()
    if current_user_id:
        user = User.query.get(current_user_id)
        if user:
            join_room(f"user_{current_user_id}", namespace="/notifications")
            print(f"User {user.email} (ID: {current_user_id}) connected to notifications and joined room user_{current_user_id}")
        else:
            print(f"User with ID {current_user_id} not found during notification connect.")
            return False # कनेक्शन अस्वीकार करें
    else:
        print("Anonymous user connected to notifications namespace.")
        # यदि प्रमाणीकरण आवश्यक है, तो यहाँ कनेक्शन अस्वीकार करें
        # return False

@socketio.on("disconnect", namespace="/notifications")
def handle_notification_disconnect():
    print(f"Client {request.sid} disconnected from notifications namespace.")

# `new_notification` इवेंट को अन्य भागों (जैसे बुकिंग, मैसेजिंग) से एमिट किया जाएगा
# जब सर्वर-साइड पर कोई सूचना बनती है।
# उदाहरण के लिए, बुकिंग अप्रूव होने पर:
# notification = Notification(user_id=..., type="booking_approved", ...)
# db.session.add(notification)
# db.session.commit()
# socketio.emit("new_notification", notification.to_dict(), room=f"user_{notification.user_id}", namespace="/notifications")

