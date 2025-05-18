from src.extensions import db # db इंस्टेंस को main.py से इम्पोर्ट करें
import datetime

# कोर्ट और ट्रेनर्स के बीच मेनी-टू-मेनी रिलेशनशिप के लिए एसोसिएशन टेबल
court_trainers_association = db.Table("court_trainers",
    db.Column("court_id", db.Integer, db.ForeignKey("courts.id"), primary_key=True),
    db.Column("trainer_user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True) # यह Users टेबल के trainer रोल वाले यूज़र को रेफर करेगा
)

# कोर्ट और फॉलोअर्स (Users) के बीच मेनी-टू-मेनी रिलेशनशिप के लिए एसोसिएशन टेबल
court_followers_association = db.Table("court_followers",
    db.Column("court_id", db.Integer, db.ForeignKey("courts.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)
)

class Court(db.Model):
    __tablename__ = "courts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(512), nullable=True)
    # location_coordinates = db.Column(db.Point, nullable=True) # PostGIS की आवश्यकता होगी, अभी के लिए इसे छोड़ दें या टेक्स्ट के रूप में स्टोर करें
    location_latitude = db.Column(db.Float, nullable=True)
    location_longitude = db.Column(db.Float, nullable=True)
    surface_type = db.Column(db.String(50))
    setting = db.Column(db.String(50)) # e.g., Indoor, Outdoor
    thumbnail_url = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)
    operating_hours = db.Column(db.JSON, nullable=True) # e.g., { "monday": ["08:00", "22:00"], ... }
    status = db.Column(db.String(20), default="active") # e.g., active, maintenance, closed
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    bookings = db.relationship("Booking", back_populates="court", lazy="dynamic", cascade="all, delete-orphan")
    # ट्रेनर्स जो इस कोर्ट के लिए बुकिंग्स को अप्रूव कर सकते हैं
    approving_trainers = db.relationship(
        "User", 
        secondary=court_trainers_association,
        backref=db.backref("managed_courts", lazy="dynamic"),
        lazy="dynamic"
    )
    followers = db.relationship(
        "User",
        secondary=court_followers_association,
        backref=db.backref("followed_courts", lazy="dynamic"), # Changed from back_populates to backref for User model
        lazy="dynamic"
    )

    def to_dict(self, current_user_id=None):
        data = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "location_latitude": self.location_latitude,
            "location_longitude": self.location_longitude,
            "surface_type": self.surface_type,
            "setting": self.setting,
            "thumbnail_url": self.thumbnail_url,
            "description": self.description,
            "operating_hours": self.operating_hours,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if current_user_id:
            data["is_followed_by_current_user"] = any(follower.id == current_user_id for follower in self.followers)
        return data

    def __repr__(self):
        return f"<Court {self.name}>"

# Trainer प्रोफाइल, यदि Users मॉडल से अलग रखना है
# हमारे schema के अनुसार, Trainer Users मॉडल का एक हिस्सा है (role=\"trainer\")
# Court_Trainers एसोसिएशन टेबल Users (role=\"trainer\") और Courts को लिंक करता है।
# यदि Trainer की अपनी अलग प्रोफ़ाइल जानकारी है जो User मॉडल में फिट नहीं होती है,
# तो हम एक अलग TrainerProfile मॉडल बना सकते हैं जो User से वन-टू-वन लिंक हो।
# अभी के लिए, हम मानते हैं कि User मॉडल में trainer की सभी आवश्यक जानकारी है।
