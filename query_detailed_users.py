from app import create_app
from app.models.user import User, StudentProfile, FacultyProfile

app = create_app()

with app.app_context():
    users = User.query.all()
    print("\nUser Accounts:")
    print("-" * 100)
    print(f"{'Username':<15} {'Email':<35} {'Role':<10} {'Name':<25} {'Details':<20}")
    print("-" * 100)
    
    for user in users:
        name = ""
        details = ""
        
        if user.role == 'student' and user.student_profile:
            name = f"{user.student_profile.first_name} {user.student_profile.last_name}"
            details = f"Roll: {user.student_profile.roll_number}"
        elif user.role == 'faculty' and user.faculty_profile:
            name = f"{user.faculty_profile.first_name} {user.faculty_profile.last_name}"
            details = f"Dept: {user.faculty_profile.department}"
            
        print(f"{user.username:<15} {user.email:<35} {user.role:<10} {name:<25} {details:<20}")
    
    print("-" * 100)
    print("Note: Passwords cannot be retrieved as they are securely hashed in the database.")
