from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_migrate import Migrate

# Initialize extensions here to be imported by the app and models
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
migrate = Migrate()

