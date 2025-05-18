from flask import Blueprint, request, jsonify
from src.models.message import Message
from src.models.user import User # यूज़र जानकारी के लिए
from src.extensions import db, socketio # db और socketio को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
import datetime

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/chats", methods=["GET"])
@jwt_required()
def get_user_chats():
    current_user_id = get_jwt_identity()
    # उन सभी यूज़र्स की सूची प्राप्त करें जिनके साथ वर्तमान यूज़र ने चैट की है
    # यह सभी संदेशों को क्वेरी करके और अद्वितीय प्रेषकों/प्राप्तकर्ताओं को निकालकर किया जा सकता है
    # या एक अलग "ChatSession" मॉडल बनाकर

    # सरल दृष्टिकोण: सभी संदेशों से अद्वितीय संपर्क प्राप्त करें
    sent_to_users = db.session.query(Message.receiver_id).filter(Message.sender_id == current_user_id).distinct()
    received_from_users = db.session.query(Message.sender_id).filter(Message.receiver_id == current_user_id).distinct()
    
    contact_ids = {r_id for (r_id,) in sent_to_users}.union({s_id for (s_id,) in received_from_users})

    chats = []
    for user_id in contact_ids:
        contact_user = User.query.get(user_id)
        if contact_user:
            # इस चैट के लिए अंतिम संदेश प्राप्त करें
            last_message = Message.query.filter(
                or_(
                    and_(Message.sender_id == current_user_id, Message.receiver_id == user_id),
                    and_(Message.sender_id == user_id, Message.receiver_id == current_user_id)
                )
            ).order_by(Message.sent_at.desc()).first()
            
            chats.append({
                "contact_id": contact_user.id,
                "contact_name": contact_user.full_name,
                "contact_profile_picture_url": contact_user.profile_picture_url,
                "last_message_content": last_message.content if last_message else None,
                "last_message_sent_at": last_message.sent_at.isoformat() if last_message else None,
                "unread_count": 0 # अपठित गणना के लिए अतिरिक्त लॉजिक की आवश्यकता होगी
            })
    
    # अंतिम संदेश के समय के अनुसार चैट्स को सॉर्ट करें
    chats.sort(key=lambda x: x["last_message_sent_at"] or datetime.datetime.min.isoformat(), reverse=True)

    return jsonify({"message": "Chats retrieved successfully", "chats": chats}), 200

@messages_bp.route("/chats/<int:other_user_id>", methods=["GET"])
@jwt_required()
def get_message_history(other_user_id):
    current_user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    messages_query = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user_id, Message.receiver_id == other_user_id),
            and_(Message.sender_id == other_user_id, Message.receiver_id == current_user_id)
        )
    ).order_by(Message.sent_at.desc())
    
    paginated_messages = messages_query.paginate(page=page, per_page=per_page, error_out=False)
    messages_data = [message.to_dict() for message in paginated_messages.items]
    messages_data.reverse() # कालानुक्रमिक क्रम के लिए (सबसे नया सबसे नीचे)

    # संदेशों को पढ़ते ही उन्हें पढ़ा हुआ चिह्नित करें (वैकल्पिक)
    # Message.query.filter(
    #     Message.receiver_id == current_user_id,
    #     Message.sender_id == other_user_id,
    #     Message.read_at.is_(None)
    # ).update({"read_at": datetime.datetime.utcnow()}, synchronize_session=False)
    # db.session.commit()

    return jsonify({
        "message": "Message history retrieved successfully",
        "messages": messages_data,
        "total_pages": paginated_messages.pages,
        "current_page": paginated_messages.page,
        "total_messages": paginated_messages.total
    }), 200

# SocketIO इवेंट्स मैसेजिंग के लिए
@socketio.on("connect", namespace="/chat")
@jwt_required(optional=True) # कनेक्शन के लिए JWT वैकल्पिक हो सकता है, या टोकन पास किया जा सकता है
def handle_chat_connect():
    current_user_id = get_jwt_identity()
    if current_user_id:
        user = User.query.get(current_user_id)
        if user:
            # यूज़र को उनके अपने रूम में जॉइन कराएँ ताकि वे निजी संदेश प्राप्त कर सकें
            from flask_socketio import join_room
            join_room(f"user_{current_user_id}")
            print(f"User {user.email} (ID: {current_user_id}) connected to chat and joined room user_{current_user_id}")
        else:
            print(f"User with ID {current_user_id} not found during chat connect.")
            return False # कनेक्शन अस्वीकार करें
    else:
        print("Anonymous user connected to chat namespace.")
        # यदि प्रमाणीकरण आवश्यक है, तो यहाँ कनेक्शन अस्वीकार करें
        # return False

@socketio.on("send_message", namespace="/chat")
@jwt_required() # संदेश भेजने के लिए JWT आवश्यक है
def handle_send_message(data):
    sender_id = get_jwt_identity()
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    booking_id = data.get("booking_id") # वैकल्पिक

    if not receiver_id or not content:
        socketio.emit("message_error", {"error": "Receiver ID and content are required"}, room=request.sid) # केवल प्रेषक को त्रुटि भेजें
        return

    # सुनिश्चित करें कि प्राप्तकर्ता मौजूद है
    receiver_user = User.query.get(receiver_id)
    if not receiver_user:
        socketio.emit("message_error", {"error": "Receiver not found"}, room=request.sid)
        return

    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        booking_id=booking_id
    )
    try:
        db.session.add(new_message)
        db.session.commit()
        message_data = new_message.to_dict()
        
        # प्राप्तकर्ता को संदेश भेजें यदि वे कनेक्टेड हैं
        socketio.emit("new_message", message_data, room=f"user_{receiver_id}", namespace="/chat")
        # प्रेषक को भी पुष्टि भेजें (वैकल्पिक, क्योंकि वे UI में इसे तुरंत देखेंगे)
        socketio.emit("message_sent_confirmation", message_data, room=request.sid) # या room=f"user_{sender_id}"

        # प्राप्तकर्ता के लिए एक सूचना भी बनाएँ (यदि वे ऑफ़लाइन हैं या ऐप में नहीं हैं)
        from src.models.notification import Notification
        sender_user = User.query.get(sender_id)
        notification_content = f"You have a new message from {sender_user.full_name if sender_user else 'User {sender_id}'}: {content[:50]}..."
        new_notification = Notification(
            user_id=receiver_id,
            type="new_message",
            related_entity_id=new_message.id,
            related_entity_type="message",
            content=notification_content
        )
        db.session.add(new_notification)
        db.session.commit()
        # प्राप्तकर्ता को सूचना भेजें यदि वे सूचना रूम में कनेक्टेड हैं
        socketio.emit("new_notification", new_notification.to_dict(), room=f"user_{receiver_id}", namespace="/notifications") # अलग नेमस्पेस

    except Exception as e:
        db.session.rollback()
        socketio.emit("message_error", {"error": f"Error sending message: {str(e)}"}, room=request.sid)

@socketio.on("mark_as_read", namespace="/chat")
@jwt_required()
def handle_mark_as_read(data):
    current_user_id = get_jwt_identity()
    message_id = data.get("message_id") # या sender_id जिसके साथ चैट पढ़ी गई
    # यहाँ संदेशों को पढ़ा हुआ चिह्नित करने का लॉजिक होगा
    # उदा. Message.query.filter_by(id=message_id, receiver_id=current_user_id).update({"read_at": datetime.datetime.utcnow()})
    # db.session.commit()
    # प्रेषक को सूचित करें कि संदेश पढ़ा गया है (यदि आवश्यक हो)
    pass

@socketio.on("disconnect", namespace="/chat")
def handle_chat_disconnect():
    # current_user_id = get_jwt_identity() # डिस्कनेक्ट पर JWT उपलब्ध नहीं हो सकता है
    print(f"Client {request.sid} disconnected from chat namespace.")

