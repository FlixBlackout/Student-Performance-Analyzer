#!/usr/bin/env python3
"""
Fix ML Model Version Compatibility
Retrains the model with the current scikit-learn version to resolve version mismatch warnings.
"""

import os
import sys
import warnings

def retrain_model():
    """Retrain the ML model with current scikit-learn version"""
    
    print("🔄 Retraining ML Model for Version Compatibility")
    print("=" * 50)
    
    try:
        # Import the ML model
        from app.models.ml_model import StudentPerformancePredictor, generate_synthetic_data
        
        print("📊 Generating synthetic training data...")
        # Generate training data
        data = generate_synthetic_data(n_samples=500)
        
        # Prepare features and target
        X = data[['previous_grade', 'current_grade', 'attendance_percentage', 'study_hours']]
        y = data['actual_score']
        
        print("🧠 Training new model...")
        # Create and train predictor
        predictor = StudentPerformancePredictor()
        
        # Train the model
        results = predictor.train(X, y)
        
        print("✅ Model Training Complete!")
        print(f"📈 Model Performance:")
        print(f"   - R² Score: {results['r2']:.3f}")
        print(f"   - MSE: {results['mse']:.3f}")
        print(f"   - Test Samples: {results['test_size']}")
        
        # Test a prediction
        print("\n🧪 Testing prediction...")
        test_features = [[85, 88, 92, 20]]  # [prev_grade, curr_grade, attendance, study_hours]
        prediction = predictor.predict(test_features)
        print(f"   Test prediction: {prediction:.1f}")
        
        print("\n🎉 Model successfully retrained with current scikit-learn version!")
        return True
        
    except Exception as e:
        print(f"❌ Error retraining model: {e}")
        print("💡 The application will use heuristic predictions as fallback")
        return False

if __name__ == "__main__":
    success = retrain_model()
    sys.exit(0 if success else 1)