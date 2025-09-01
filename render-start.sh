#!/bin/bash
# render-start.sh - Render deployment startup script

# Set default port for Render (typically 10000)
export PORT=${PORT:-10000}

# Print environment info
echo "🚀 Starting STA on Render"
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