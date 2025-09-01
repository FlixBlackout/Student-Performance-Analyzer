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
                # Try to load model and catch version warnings
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    self.model = joblib.load(self.model_path)
                    self.scaler = joblib.load(self.scaler_path)
                    
                # Check if model loaded successfully
                if self.model is not None:
                    print("✅ ML Model loaded successfully")
                    return True
                else:
                    print("⚠️ Model file corrupted, will retrain")
                    return False
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            print("🔄 Will retrain model with current scikit-learn version")
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
        X : DataFrame with features (previous_grade, current_grade, attendance_percentage, study_hours)
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
        features : DataFrame with columns [previous_grade, current_grade, attendance_percentage, study_hours]
        
        Returns:
        predicted_score : float
        """
        if self.model is None:
            # If no model is trained, use a simple heuristic
            return self._heuristic_prediction(features)
        
        # Check if the model was trained with or without current_grade
        # If model expects 3 features but we have 4, use only the required ones
        if hasattr(self.model, 'n_features_in_') and self.model.n_features_in_ == 3 and features.shape[1] == 4:
            # Extract only previous_grade, attendance, study_hours
            features_to_use = np.array([[features[0, 0], features[0, 2], features[0, 3]]])
            # Scale features
            features_scaled = self.scaler.transform(features_to_use)
        else:
            # Scale features as is
            try:
                features_scaled = self.scaler.transform(features)
            except ValueError:
                # If there's a dimension mismatch, fall back to heuristic
                print("Dimension mismatch in model prediction. Using heuristic instead.")
                return self._heuristic_prediction(features)
        
        # Make prediction
        return self.model.predict(features_scaled)[0]
    
    def _heuristic_prediction(self, features):
        """Simple heuristic for prediction when no model is available"""
        # Extract features
        previous_grade = features[0, 0]
        current_grade = features[0, 1] if features.shape[1] > 3 else previous_grade  # Use previous grade if current not provided
        attendance = features[0, 2] if features.shape[1] > 3 else features[0, 1]
        study_hours = features[0, 3] if features.shape[1] > 3 else features[0, 2]
        
        # Base prediction on mean of input values with emphasis on current grade
        # For good current grades (>= 80), ensure prediction tends toward 80+
        if current_grade >= 80:
            # For high current grades, prediction should be at least 80
            # and influenced by other factors
            base_score = 80
            # Other factors can push it higher but with diminishing returns
            additional_score = min(15, (current_grade - 80) * 0.5)
            
            # Attendance and study hours can add up to 5 points
            attendance_bonus = min(3, (attendance - 80) * 0.15) if attendance > 80 else 0
            study_bonus = min(2, study_hours * 0.1)
            
            predicted_score = base_score + additional_score + attendance_bonus + study_bonus
        else:
            # For lower current grades, use weighted mean with current grade having highest weight
            weights = [0.2, 0.5, 0.2, 0.1] if features.shape[1] > 3 else [0.6, 0.3, 0.1]
            
            # Normalize attendance (0-100) to 0-100 scale
            attendance_normalized = attendance
            
            # Normalize study hours (assuming max of 40 hours/week) to 0-100 scale
            study_hours_normalized = min(study_hours * 2.5, 100)
            
            # Calculate weighted score
            if features.shape[1] > 3:
                predicted_score = (
                    weights[0] * previous_grade + 
                    weights[1] * current_grade +
                    weights[2] * attendance_normalized + 
                    weights[3] * study_hours_normalized
                )
            else:
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
    
    # Generate random features with more realistic distributions
    # Previous grades with normal distribution around 75
    previous_grades = np.clip(np.random.normal(75, 10, n_samples), 40, 100)
    
    # Current grades with normal distribution around 78
    current_grades = np.clip(np.random.normal(78, 12, n_samples), 40, 100)
    
    # Attendance with skewed distribution toward higher values (most students attend)
    attendance = np.clip(np.random.beta(7, 2, n_samples) * 100, 50, 100)
    
    # Study hours with normal distribution around 15 hours/week
    study_hours = np.clip(np.random.normal(15, 8, n_samples), 1, 40)
    
    # Create a synthetic relationship that centers around 80 for good students
    actual_scores = np.zeros(n_samples)
    
    for i in range(n_samples):
        if current_grades[i] >= 80:
            # For high current grades, base score is 80 with bonuses
            base_score = 80
            additional_score = min(15, (current_grades[i] - 80) * 0.5)
            attendance_bonus = min(3, (attendance[i] - 80) * 0.15) if attendance[i] > 80 else 0
            study_bonus = min(2, study_hours[i] * 0.1)
            
            score = base_score + additional_score + attendance_bonus + study_bonus
        else:
            # For lower current grades, weighted average
            score = (
                0.2 * previous_grades[i] +
                0.5 * current_grades[i] +
                0.2 * attendance[i] +
                0.1 * min(study_hours[i] * 2.5, 100)
            )
        
        # Add some random noise
        actual_scores[i] = score + np.random.normal(0, 3)
    
    # Ensure scores are within reasonable bounds
    actual_scores = np.clip(actual_scores, 0, 100)
    
    # Create DataFrame
    data = pd.DataFrame({
        'previous_grade': previous_grades,
        'current_grade': current_grades,
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
        X = data[['previous_grade', 'current_grade', 'attendance_percentage', 'study_hours']]
        y = data['actual_score']
        
        metrics = predictor.train(X, y)
        print(f"Initialized model with synthetic data. Metrics: {metrics}")
    
    return predictor
