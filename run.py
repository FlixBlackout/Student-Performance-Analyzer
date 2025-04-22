from app import create_app
from app.models.ml_model import initialize_model

app = create_app()

# Initialize the ML model with synthetic data when the app starts
with app.app_context():
    initialize_model()

if __name__ == '__main__':
    app.run(debug=True)
