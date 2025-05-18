import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Correct path to the database file relative to the script's execution directory
# The script will be run from /home/ubuntu, and the DB is in 
# /home/ubuntu/project_files/home/ubuntu/CourtReserve_Project/home/ubuntu/CourtReserve_Project_Archive/CourtReserve_Backend/instance/courtreserve.db

DB_PATH = os.path.join("/home/ubuntu/project_files/home/ubuntu/CourtReserve_Project/home/ubuntu/CourtReserve_Project_Archive/CourtReserve_Backend/instance/courtreserve.db")
USER_EMAIL = "player@example.com"
TEST_PASSWORD = "password123"

def verify_password():
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (USER_EMAIL,))
        result = cursor.fetchone()
        
        if result:
            stored_hash = result[0]
            print(f"Stored hash for {USER_EMAIL}: {stored_hash}")
            
            # Generate a new hash for the test password
            # new_generated_hash = generate_password_hash(TEST_PASSWORD)
            # print(f"Newly generated hash for '{TEST_PASSWORD}': {new_generated_hash}")
            
            # Check if the stored hash matches the test password
            is_correct_password = check_password_hash(stored_hash, TEST_PASSWORD)
            print(f"Verification of '{TEST_PASSWORD}' against stored hash: {is_correct_password}")
            
        else:
            print(f"User {USER_EMAIL} not found in the database.")
            
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_password()

