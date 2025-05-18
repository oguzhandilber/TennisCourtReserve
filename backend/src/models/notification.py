from src.extensions import db
import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    # For PostgreSQL, use UUID type. For SQLite, String is fine for UUIDs.
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    link = db.Column(db.String(512), nullable=True) # Optional link, e.g., to a booking or court
    type = db.Column(db.String(50), nullable=True) # e.g., booking_approved, booking_cancelled, slot_available

    # Relationships
    user = db.relationship("User", back_populates="notifications")

    def __init__(self, user_id, message, link=None, type=None):
        self.user_id = user_id
        self.message = message
        self.link = link
        self.type = type

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "link": self.link,
            "type": self.type
        }

    def __repr__(self):
        return f"<Notification {self.id} for User {self.user_id}>"

