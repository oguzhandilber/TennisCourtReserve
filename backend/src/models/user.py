from src.extensions import db # db इंस्टेंस को main.py से इम्पोर्ट करें
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    skill_level = db.Column(db.String(50), nullable=True)
    profile_picture_url = db.Column(db.String(512), nullable=True)
    communication_preferences = db.Column(db.JSON, nullable=True) # PostgreSQL में JSONB के लिए, SQLAlchemy में db.JSON का उपयोग करें
    role = db.Column(db.String(50), nullable=False, default="player") # e.g., player, tutor, court_responsible, admin
    oauth_provider = db.Column(db.String(50), nullable=True)
    oauth_id = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    bookings = db.relationship("Booking", foreign_keys="Booking.user_id", back_populates="user", lazy="dynamic")
    notifications = db.relationship("Notification", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")
    # The court_followers_association table will be defined elsewhere (e.g., in court.py or a new model file)
    # followed_courts = db.relationship("Court", secondary=court_followers_association, back_populates="followers", lazy="dynamic")

    # sent_messages = db.relationship("Message", foreign_keys=\"Message.sender_id\", backref="sender", lazy=True)
    # received_messages = db.relationship("Message", foreign_keys=\"Message.receiver_id\", backref="receiver", lazy=True)
    
    def __init__(self, email, password, full_name=None, role="player", phone_number=None, skill_level=None, profile_picture_url=None, communication_preferences=None, oauth_provider=None, oauth_id=None):
        self.email = email.lower()
        self.set_password(password) # पासवर्ड को कंस्ट्रक्टर में हैश करें यदि यह सादा टेक्स्ट है
        self.full_name = full_name
        self.role = role
        self.phone_number = phone_number
        self.skill_level = skill_level
        self.profile_picture_url = profile_picture_url
        self.communication_preferences = communication_preferences
        self.oauth_provider = oauth_provider
        self.oauth_id = oauth_id

    def set_password(self, password):
        if password: # OAuth यूज़र्स के लिए पासवर्ड नहीं हो सकता है
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = None # या एक डिफ़ॉल्ट अप्राप्य हैश

    def check_password(self, password):
        if self.password_hash and password:
            return check_password_hash(self.password_hash, password)
        return False

    def to_dict(self, include_sensitive=False):
        user_data = {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "skill_level": self.skill_level,
            "profile_picture_url": self.profile_picture_url,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            # यहाँ संवेदनशील डेटा जोड़ें यदि आवश्यक हो, लेकिन आमतौर पर API में इसे एक्सपोज़ नहीं किया जाता है
            pass
        return user_data

    def __repr__(self):
        return f"<User {self.email}>"

