#!/bin/bash
# railway-start.sh - Railway deployment startup script

# Set default port if not provided
export PORT=${PORT:-5000}

# Print environment info
echo "🚀 Starting STA on Railway"
echo "📍 Port: $PORT"
echo "🌍 Environment: $FLASK_ENV"

# Start the application
python -m gunicorn production_app:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --max-requests 100 \
    --access-logfile - \
    --error-logfile -