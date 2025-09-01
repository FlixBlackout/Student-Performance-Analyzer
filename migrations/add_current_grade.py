import sys
import os
import sqlalchemy as sa

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app and db after setting up the path
from app import create_app, db
from app.models.user import StudentPerformance

def upgrade():
    """Add current_grade column to student_performance table"""
    # Get the inspector
    inspector = sa.inspect(db.engine)
    
    # Check if the column already exists
    columns = [col['name'] for col in inspector.get_columns('student_performance')]
    
    # Only add the column if it doesn't exist
    if 'current_grade' not in columns:
        with db.engine.begin() as conn:
            conn.execute(sa.text(
                'ALTER TABLE student_performance ADD COLUMN current_grade FLOAT'
            ))
        print("Added current_grade column to student_performance table")
    else:
        print("current_grade column already exists in student_performance table")

if __name__ == "__main__":
    # Create application context
    app = create_app()
    with app.app_context():
        upgrade()
