import sys
import os
import click

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS # Import CORS
from src.config import Config
from src.extensions import db, jwt, socketio, migrate # Import from extensions

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}}) # Initialize CORS

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, async_mode='eventlet', cors_allowed_origins="*")
    migrate.init_app(app, db)

    from src.models import user, court, booking, message, notification, waitlist

    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from src.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from src.routes.courts import courts_bp
    app.register_blueprint(courts_bp, url_prefix='/courts')

    from src.routes.bookings import bookings_bp
from src.routes.health import health_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')

    from src.routes.trainer import trainer_bp
    app.register_blueprint(trainer_bp, url_prefix='/trainer')

    from src.routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix='/messages')

    from src.routes.notifications import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    from src.routes.waitlist import waitlist_bp
    app.register_blueprint(waitlist_bp, url_prefix='/waitlist')

    @app.route('/')
    def index():
        return "Welcome to CourtReserve API!"

    @app.cli.command("seed-db")
    def seed_db_command():
        """Seeds the database with initial data."""
        from src.seed import seed_data
        with app.app_context():
            seed_data()
        click.echo("Database seeded.")

    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting SocketIO server on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=True)

