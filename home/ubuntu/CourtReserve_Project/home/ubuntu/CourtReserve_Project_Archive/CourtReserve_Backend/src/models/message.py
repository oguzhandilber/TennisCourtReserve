from src.extensions import db # db इंस्टेंस को main.py से इम्पोर्ट करें
import datetime

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=True) # वैकल्पिक लिंक
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    # sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    # receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    # booking = db.relationship("Booking", backref="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "booking_id": self.booking_id,
            "content": self.content,
            "sent_at": self.sent_at.isoformat(),
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "sender_name": self.sender.full_name if self.sender else None, # उदाहरण
            "receiver_name": self.receiver.full_name if self.receiver else None # उदाहरण
        }

    def __repr__(self):
        return f"<Message {self.id} from {self.sender_id} to {self.receiver_id}>"

