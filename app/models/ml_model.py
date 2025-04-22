import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class StudentPerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = os.path.join(os.path.dirname(__file__), 'performance_model.pkl')
        self.scaler_path = os.path.join(os.path.dirname(__file__), 'performance_scaler.pkl')
        
        # Try to load existing model if available
        self.load_model()
    
    def load_model(self):
        """Load model from disk if available"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False
    
    def save_model(self):
        """Save model to disk"""
        if self.model is not None:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
    
    def train(self, X, y):
        """
        Train the model on student performance data
        
        Parameters:
        X : DataFrame with features (previous_grade, attendance_percentage, study_hours)
        y : Series with target (actual_score)
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model
        self.save_model()
        
        return {
            'mse': mse,
            'r2': r2,
            'test_size': len(y_test)
        }
    
    def predict(self, features):
        """
        Predict student performance based on features
        
        Parameters:
        features : DataFrame with columns [previous_grade, attendance_percentage, study_hours]
        
        Returns:
        predicted_score : float
        """
        if self.model is None:
            # If no model is trained, use a simple heuristic
            return self._heuristic_prediction(features)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        return self.model.predict(features_scaled)[0]
    
    def _heuristic_prediction(self, features):
        """Simple heuristic for prediction when no model is available"""
        # Extract features
        previous_grade = features[0, 0]
        attendance = features[0, 1]
        study_hours = features[0, 2]
        
        # Simple weighted average
        weights = [0.5, 0.3, 0.2]
        
        # Normalize attendance (0-100) to 0-10 scale
        attendance_normalized = attendance / 10
        
        # Normalize study hours (assuming max of 40 hours/week) to 0-10 scale
        study_hours_normalized = min(study_hours, 40) / 4
        
        # Calculate weighted score
        predicted_score = (
            weights[0] * previous_grade + 
            weights[1] * attendance_normalized + 
            weights[2] * study_hours_normalized
        )
        
        # Ensure the score is within reasonable bounds (0-100)
        return max(0, min(100, predicted_score))


# Function to generate synthetic data for initial model training
def generate_synthetic_data(n_samples=100):
    np.random.seed(42)
    
    # Generate random features
    previous_grades = np.random.uniform(40, 100, n_samples)
    attendance = np.random.uniform(50, 100, n_samples)
    study_hours = np.random.uniform(1, 40, n_samples)
    
    # Create a synthetic relationship
    actual_scores = (
        0.6 * previous_grades + 
        0.25 * attendance / 10 + 
        0.15 * study_hours + 
        np.random.normal(0, 5, n_samples)
    )
    
    # Ensure scores are within reasonable bounds
    actual_scores = np.clip(actual_scores, 0, 100)
    
    # Create DataFrame
    data = pd.DataFrame({
        'previous_grade': previous_grades,
        'attendance_percentage': attendance,
        'study_hours': study_hours,
        'actual_score': actual_scores
    })
    
    return data


# Initialize and train model with synthetic data if no real data is available
def initialize_model():
    predictor = StudentPerformancePredictor()
    
    # If model doesn't exist, train with synthetic data
    if predictor.model is None:
        data = generate_synthetic_data(200)
        X = data[['previous_grade', 'attendance_percentage', 'study_hours']]
        y = data['actual_score']
        
        metrics = predictor.train(X, y)
        print(f"Initialized model with synthetic data. Metrics: {metrics}")
    
    return predictor
