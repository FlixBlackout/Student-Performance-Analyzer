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
        
        # Initialize ML model with synthetic data
        initialize_model()
        print("✅ ML Model initialized successfully!")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize ML model: {e}")
        print("The application will work without ML predictions.")

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)