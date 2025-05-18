from flask import Blueprint, request, jsonify
from src.models.notification import Notification
from src.models.user import User
from src.models.court import Court
from src.extensions import db, socketio
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("", methods=["GET"])
@jwt_required()
def get_user_notifications():
    """Get notifications for the current user."""
    current_user_id = get_jwt_identity()
    
    # Optional query parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    unread_only = request.args.get("unread_only", False, type=bool)
    
    query = Notification.query.filter(Notification.user_id == current_user_id)
    
    # Filter by read status if requested
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    # Order by creation time (newest first)
    query = query.order_by(Notification.created_at.desc())
    
    # Paginate results
    paginated_notifications = query.paginate(page=page, per_page=per_page, error_out=False)
    
    notifications_data = [notification.to_dict() for notification in paginated_notifications.items]
    
    return jsonify({
        "notifications": notifications_data,
        "total_pages": paginated_notifications.pages,
        "current_page": paginated_notifications.page,
        "total_notifications": paginated_notifications.total,
        "unread_count": Notification.query.filter_by(user_id=current_user_id, is_read=False).count()
    }), 200

@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_notification_as_read(notification_id):
    """Mark a specific notification as read."""
    current_user_id = get_jwt_identity()
    
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"message": "Notification not found"}), 404
    
    # Check if the notification belongs to the current user
    if notification.user_id != current_user_id:
        return jsonify({"message": "Unauthorized to access this notification"}), 403
    
    # Mark as read if not already
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.datetime.utcnow()
        db.session.commit()
    
    return jsonify({"message": "Notification marked as read"}), 200

@notifications_bp.route("/read-all", methods=["PUT"])
@jwt_required()
def mark_all_notifications_as_read():
    """Mark all notifications for the current user as read."""
    current_user_id = get_jwt_identity()
    
    # Find all unread notifications for this user
    unread_notifications = Notification.query.filter_by(
        user_id=current_user_id,
        is_read=False
    ).all()
    
    # Mark all as read
    now = datetime.datetime.utcnow()
    for notification in unread_notifications:
        notification.is_read = True
        notification.read_at = now
    
    db.session.commit()
    
    return jsonify({
        "message": "All notifications marked as read",
        "count": len(unread_notifications)
    }), 200

# Helper functions for creating and sending notifications

def create_notification(user_id, notification_type, content, related_id=None):
    """
    Create a new notification for a user.
    
    Args:
        user_id: ID of the user to notify
        notification_type: Type of notification (e.g., 'booking_status', 'court_update')
        content: Text content of the notification
        related_id: Optional ID of related entity (booking_id, court_id, etc.)
    
    Returns:
        The created notification object
    """
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        content=content,
        related_id=related_id,
        is_read=False,
        created_at=datetime.datetime.utcnow()
    )
    
    db.session.add(notification)
    db.session.commit()
    
    # Send real-time notification via WebSocket
    send_realtime_notification(notification)
    
    return notification

def send_realtime_notification(notification):
    """
    Send a notification to the user via WebSocket.
    
    Args:
        notification: The notification object to send
    """
    socketio.emit(
        'notification',
        notification.to_dict(),
        room=f"user_{notification.user_id}"
    )

def notify_booking_status_change(booking):
    """
    Notify a user about a booking status change.
    
    Args:
        booking: The booking object that changed status
    """
    status_messages = {
        "confirmed": f"Your booking for {booking.court.name} on {booking.start_time.strftime('%b %d')} has been approved!",
        "rejected": f"Your booking for {booking.court.name} on {booking.start_time.strftime('%b %d')} has been declined.",
        "cancelled": f"Your booking for {booking.court.name} on {booking.start_time.strftime('%b %d')} has been cancelled."
    }
    
    if booking.status in status_messages:
        create_notification(
            user_id=booking.user_id,
            notification_type="booking_status",
            content=status_messages[booking.status],
            related_id=booking.id
        )

def notify_court_followers(court_id, message, exclude_user_id=None):
    """
    Notify all followers of a court.
    
    Args:
        court_id: ID of the court
        message: Notification message
        exclude_user_id: Optional user ID to exclude from notifications
    """
    # Get all users following this court
    court = Court.query.get(court_id)
    if not court:
        return
    
    for follower in court.followers:
        if exclude_user_id and follower.user_id == exclude_user_id:
            continue
        
        create_notification(
            user_id=follower.user_id,
            notification_type="court_update",
            content=message,
            related_id=court_id
        )
