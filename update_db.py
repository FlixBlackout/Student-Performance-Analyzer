from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Add the new columns to the User table
    db.engine.execute('ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)')
    db.engine.execute('ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME')
    
    print("Database updated successfully with password reset fields.")
