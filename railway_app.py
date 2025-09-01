#!/usr/bin/env python3
"""
Railway-specific production app for STA (Student Performance Analyzer)
Handles Railway's specific PORT and domain requirements
"""

import os
import sys
from app import create_app
from app.models.ml_model import initialize_model

# Create the Flask application
app = create_app()

# Railway-specific configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'railway-sta-secret-key'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///railway.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    WTF_CSRF_ENABLED=True,
    FLASK_ENV='production'
)

# Railway health check endpoint
@app.route('/health')
def health_check():
    """Health check for Railway"""
    return {
        'status': 'healthy',
        'message': 'STA application is running on Railway',
        'port': os.environ.get('PORT', 'not set'),
        'env': os.environ.get('FLASK_ENV', 'not set')
    }, 200

@app.route('/railway-status')
def railway_status():
    """Railway-specific status endpoint"""
    return {
        'platform': 'Railway',
        'status': 'operational',
        'port': os.environ.get('PORT'),
        'database': 'connected' if app.config['SQLALCHEMY_DATABASE_URI'] else 'not configured'
    }

# Initialize the application
def initialize_app():
    """Initialize the application for Railway"""
    with app.app_context():
        try:
            # Create database tables
            from app.models.user import db
            db.create_all()
            print("✅ Database initialized")
            
            # Initialize ML model with warning suppression
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message=".*Trying to unpickle estimator.*")
                initialize_model()
            print("✅ ML Model initialized")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Initialization warning: {e}")
            print("📝 Application will work with basic functionality")
            return False

# Railway startup
if __name__ == '__main__':
    # Get Railway's PORT (required)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚂 Starting STA on Railway")
    print(f"📍 Port: {port}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    # Initialize the app
    initialize_app()
    
    # Start the server - CRITICAL: Must bind to 0.0.0.0 for Railway
    app.run(
        host='0.0.0.0',  # MUST be 0.0.0.0 for Railway
        port=port,
        debug=False,
        threaded=True
    )