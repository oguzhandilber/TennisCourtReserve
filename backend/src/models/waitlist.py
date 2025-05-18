from src.extensions import db # db इंस्टेंस को main.py से इम्पोर्ट करें
import datetime

class WaitlistEntry(db.Model):
    __tablename__ = "waitlist_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"), nullable=False)
    desired_date = db.Column(db.Date, nullable=False)
    desired_start_time = db.Column(db.Time, nullable=False)
    desired_end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="active") # e.g., active, notified, booked, expired
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    # user = db.relationship("User", backref="waitlist_entries")
    # court = db.relationship("Court", backref="waitlist_entries")

    # एक ही यूज़र, कोर्ट, और समय के लिए डुप्लिकेट एंट्रीज़ को रोकने के लिए यूनिक कंस्ट्रेंट
    __table_args__ = (db.UniqueConstraint("user_id", "court_id", "desired_date", "desired_start_time", name="_user_court_time_uc"),)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "court_id": self.court_id,
            "desired_date": self.desired_date.isoformat(),
            "desired_start_time": self.desired_start_time.isoformat(),
            "desired_end_time": self.desired_end_time.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "user_email": self.user.email if self.user else None,
            "court_name": self.court.name if self.court else None
        }

    def __repr__(self):
        return f"<WaitlistEntry {self.id} for User {self.user_id} - Court {self.court_id} on {self.desired_date} at {self.desired_start_time}>"

