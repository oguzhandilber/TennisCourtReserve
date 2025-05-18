#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the app directory if not already there (though WORKDIR should handle this)
# cd /app

echo "Applying database migrations..."
flask db upgrade

echo "Seeding database..."
flask seed-db

echo "Starting Flask application..."
exec flask run --host=0.0.0.0 --port=5000

