from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_jwt_extended import decode_token
from flask import request
import functools

# Initialize SocketIO instance
socketio = SocketIO()

# Store active connections
active_connections = {}

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # Check if the request has a valid JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            disconnect()
            return
        
        try:
            token = auth_header.split(' ')[1]
            decoded = decode_token(token)
            user_id = decoded.get('sub')
            if not user_id:
                disconnect()
                return
            
            # Add user_id to the function call
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Socket authentication error: {e}")
            disconnect()
            
    return wrapped

def init_socketio(app):
    """Initialize SocketIO with the Flask app and register event handlers."""
    socketio.init_app(app, cors_allowed_origins="*")
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        print("Client connected:", request.sid)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print("Client disconnected:", request.sid)
        
        # Remove from active connections
        for user_id, connections in list(active_connections.items()):
            if request.sid in connections:
                connections.remove(request.sid)
                if not connections:
                    del active_connections[user_id]
                break
    
    @socketio.on('authenticate')
    def handle_authentication(data):
        """Handle client authentication."""
        token = data.get('token')
        if not token:
            emit('authentication_error', {'message': 'No token provided'})
            return
        
        try:
            decoded = decode_token(token)
            user_id = decoded.get('sub')
            
            if not user_id:
                emit('authentication_error', {'message': 'Invalid token'})
                return
            
            # Add to user's room
            user_room = f"user_{user_id}"
            join_room(user_room)
            
            # Track connection
            if user_id not in active_connections:
                active_connections[user_id] = []
            active_connections[user_id].append(request.sid)
            
            emit('authenticated', {'user_id': user_id})
            print(f"User {user_id} authenticated")
            
        except Exception as e:
            print(f"Authentication error: {e}")
            emit('authentication_error', {'message': 'Invalid token'})
    
    return socketio

def send_notification_to_user(user_id, notification_data):
    """Send a notification to a specific user."""
    user_room = f"user_{user_id}"
    socketio.emit('notification', notification_data, room=user_room)
