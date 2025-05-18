#!/bin/bash
# Health check endpoint for backend
echo "Creating health check endpoint for backend..."

cat > /home/ubuntu/projects/TennisCourtReserve/clean_project/backend/src/routes/health.py << 'EOF'
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("", methods=["GET"])
def health_check():
    """Health check endpoint for Docker healthcheck."""
    return jsonify({
        "status": "healthy",
        "message": "TennisCourtReserve API is running"
    }), 200
EOF

# Update main.py to register the health blueprint
echo "Updating main.py to register health blueprint..."

# Check if the health blueprint is already registered
if ! grep -q "from src.routes.health import health_bp" /home/ubuntu/projects/TennisCourtReserve/clean_project/backend/src/main.py; then
    # Add import for health blueprint
    sed -i '/from src.routes.bookings import bookings_bp/a from src.routes.health import health_bp' /home/ubuntu/projects/TennisCourtReserve/clean_project/backend/src/main.py
    
    # Register health blueprint
    sed -i '/app.register_blueprint(bookings_bp, url_prefix="\/api\/bookings")/a \ \ \ \ app.register_blueprint(health_bp, url_prefix="\/api\/health")' /home/ubuntu/projects/TennisCourtReserve/clean_project/backend/src/main.py
fi

echo "Health check endpoint setup complete."
