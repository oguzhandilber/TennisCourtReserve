from src.extensions import db # db इंस्टेंस को main.py से इम्पोर्ट करें
import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"), nullable=False, index=True)
    # Stores the ID of the user (e.g., court_responsible) who approved/managed this booking
    approved_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    # Aligned with API design: pending_approval, confirmed, rejected, cancelled, completed
    status = db.Column(db.String(50), nullable=False, default="pending_approval", index=True) 
    user_note = db.Column(db.Text, nullable=True) # Renamed from user_notes for consistency
    court_responsible_note = db.Column(db.Text, nullable=True) # For rejection reasons or other notes by approver
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = db.relationship("User", foreign_keys=[user_id], back_populates="bookings")
    court = db.relationship("Court", back_populates="bookings")
    # User who approved this booking (could be a court_responsible)
    approved_by_user = db.relationship("User", foreign_keys=[approved_by_user_id], backref=db.backref("approved_bookings", lazy="dynamic"))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "court_id": self.court_id,
            "approved_by_user_id": self.approved_by_user_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "status": self.status,
            "user_note": self.user_note,
            "court_responsible_note": self.court_responsible_note,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_full_name": self.user.full_name if self.user else None,
            "court_name": self.court.name if self.court else None,
            "approved_by_user_name": self.approved_by_user.full_name if self.approved_by_user else None
        }

    def __repr__(self):
        return f"<Booking {self.id} - Court {self.court_id} by User {self.user_id} at {self.start_time}>"
