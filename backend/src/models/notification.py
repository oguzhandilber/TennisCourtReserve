from src.extensions import db
import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False, index=True)  # booking_status, court_update, etc.
    content = db.Column(db.Text, nullable=False)
    related_id = db.Column(db.Integer, nullable=True)  # Optional ID of related entity (booking_id, court_id, etc.)
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime, nullable=True)

    # Relationship
    user = db.relationship("User", back_populates="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "content": self.content,
            "related_id": self.related_id,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),
            "read_at": self.read_at.isoformat() if self.read_at else None
        }

    def __repr__(self):
        return f"<Notification {self.id} for User {self.user_id} - {self.type}>"
