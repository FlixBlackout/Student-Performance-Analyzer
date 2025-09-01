import os
from app import create_app
from app.models.ml_model import initialize_model

# Create the Flask application
app = create_app()

# Configure for production
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///production.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    WTF_CSRF_ENABLED=True,
    FLASK_ENV='production'
)

# Add health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'STA application is running'}, 200

# Initialize the ML model
with app.app_context():
    try:
        # Create database tables
        from app.models.user import db
        db.create_all()
        
        # Initialize ML model with version handling
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*Trying to unpickle estimator.*")
            from app.models.ml_model import initialize_model
            initialize_model()
        
        print("✅ Application initialized successfully!")
        print("🤖 ML Model ready for predictions!")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize ML model: {e}")
        print("📝 The application will work with heuristic predictions.")
        print("🔧 To fix ML predictions, run: python fix_model_version.py")

if __name__ == '__main__':
    # Get port from environment with fallback
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting STA on {host}:{port}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    # For development and fallback
    app.run(host=host, port=port, debug=False)