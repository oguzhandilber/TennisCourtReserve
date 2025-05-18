from src.extensions import db
import datetime

class CourtFollower(db.Model):
    __tablename__ = "court_followers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref=db.backref("followed_courts", lazy="dynamic"))
    court = db.relationship("Court", backref=db.backref("followers", lazy="dynamic"))

    def __repr__(self):
        return f"<CourtFollower: User {self.user_id} follows Court {self.court_id}>"
