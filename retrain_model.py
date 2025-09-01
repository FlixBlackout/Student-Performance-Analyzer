from app import create_app
from app.models.ml_model import initialize_model

app = create_app()
with app.app_context():
    print("Retraining the ML model with improved prediction algorithm...")
    model = initialize_model()
    print("Model training complete!")
