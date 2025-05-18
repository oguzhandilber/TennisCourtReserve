import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24).hex())
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(24).hex())
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"mysql+pymysql://{os.getenv("DB_USERNAME", "root")}:{os.getenv("DB_PASSWORD", "password")}@{os.getenv("DB_HOST", "localhost")}:{os.getenv("DB_PORT", "3306")}/{os.getenv("DB_NAME", "courtreserve_db")}")
    # Switching to SQLite for local development due to MySQL server unavailability
    SQLALCHEMY_DATABASE_URI = "sqlite:///courtreserve.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

