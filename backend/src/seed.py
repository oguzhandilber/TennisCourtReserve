from src.extensions import db
from src.models.user import User
from src.models.court import Court
from src.models.booking import Booking # Import Booking if needed for seeding
import datetime

def seed_data():
    print("Checking for existing data...")
    try:
        Booking.query.delete()
        # Assuming court_trainers is handled by cascade or is not critical for user seeding
        # If Court.approving_trainers uses a secondary table that needs explicit clearing:
        # db.session.execute(court_followers_association.delete()) # or similar for court_trainers
        Court.query.delete()
        User.query.delete()
        db.session.commit()
        print("Cleared existing users, courts, and bookings for fresh seeding.")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing existing data: {e}")
        return # Stop if clearing fails

    print("Seeding initial user data...")
    try:
        player_user = User(
            email="player@example.com",
            password="password123",
            full_name="Regular Player",
            role="player",
            phone_number="555-0001",
            skill_level="Intermediate"
        )
        db.session.add(player_user)
        print(f"Added user: {player_user.email} with role {player_user.role}")

        tutor_user = User(
            email="tutor@example.com",
            password="password123",
            full_name="Tennis Tutor",
            role="tutor",
            phone_number="555-0002",
            skill_level="Advanced Coach"
        )
        db.session.add(tutor_user)
        print(f"Added user: {tutor_user.email} with role {tutor_user.role}")

        court_responsible_user = User(
            email="responsible@example.com",
            password="password123",
            full_name="Court Manager",
            role="court_responsible",
            phone_number="555-0003"
        )
        db.session.add(court_responsible_user)
        print(f"Added user: {court_responsible_user.email} with role {court_responsible_user.role}")
        
        test_user_signup = User.query.filter_by(email="test@example.com").first()
        if not test_user_signup:
            test_user_signup = User(
                email="test@example.com", 
                password="password123", 
                full_name="Test User", 
                role="player"
            )
            db.session.add(test_user_signup)
            print(f"Added user: {test_user_signup.email} with role {test_user_signup.role}")
        else:
            print(f"User test@example.com already exists.")

        db.session.commit() # Commit after adding all users
        print("Users committed successfully.")

    except Exception as e:
        print(f"Error adding or committing users: {e}")
        db.session.rollback()
        return # Stop if user seeding fails

    print("Seeding initial court data...")
    courts_to_create = [
        {"name": "Cerciler", "surface_type": "Hard", "setting": "Outdoor", "description": "Cerciler hard court."},
        {"name": "Marina", "surface_type": "Hard", "setting": "Outdoor", "description": "Marina hard court with a sea view."},
        {"name": "Yarimada", "surface_type": "Hard", "setting": "Outdoor", "description": "Yarimada peninsula hard court."},
        {"name": "Akcagerme", "surface_type": "Hard", "setting": "Outdoor", "description": "Akcagerme hard court near the beach."}
    ]

    try:
        # Fetch the court_responsible_user again in case the session was rolled back or for clarity
        court_responsible_user = User.query.filter_by(email="responsible@example.com").first()
        if not court_responsible_user:
            print("Court responsible user not found, cannot assign to courts.")
            # Decide if this is a critical error

        for court_data in courts_to_create:
            court = Court(
                name=court_data["name"],
                address=f"{court_data['name']} Tennis Club",
                surface_type=court_data["surface_type"],
                setting=court_data["setting"],
                description=court_data["description"],
                operating_hours={"default": ["07:00", "22:00"]},
                status="active",
                thumbnail_url=f"/static/images/{court_data['name'].lower().replace(' ', '_')}.jpg"
            )
            db.session.add(court)
            print(f"Added court: {court.name}")
            
            if court_responsible_user:
                # Check if already associated to prevent IntegrityError if script is run multiple times without full clear
                # This specific error (UNIQUE constraint) suggests the association table (court_trainers)
                # might not be cleared or the logic allows duplicate appends before commit.
                # For now, we rely on the initial clear. If the error persists, this logic needs refinement.
                if court_responsible_user not in court.approving_trainers:
                    court.approving_trainers.append(court_responsible_user)
                    print(f"Assigned {court_responsible_user.email} to manage court {court.name}")
                else:
                    print(f"{court_responsible_user.email} already assigned to manage court {court.name}")
        
        db.session.commit() # Commit after adding all courts and associations
        print("Courts and assignments committed successfully.")
        print("Initial data seeded successfully!")

    except Exception as e:
        print(f"Error adding courts, assigning responsible user, or committing: {e}")
        db.session.rollback()
        return # Stop if court seeding fails

if __name__ == "__main__":
    pass

