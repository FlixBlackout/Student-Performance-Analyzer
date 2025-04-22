from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("\nUser Accounts:")
    print("-" * 80)
    print(f"{'Username':<20} {'Email':<30} {'Role':<10}")
    print("-" * 80)
    for user in users:
        print(f"{user.username:<20} {user.email:<30} {user.role:<10}")
    print("-" * 80)
