#!/usr/bin/env python3
"""
Student Performance Analyzer - Railway Deployment
Author: FlixBlackout
Repository: https://github.com/FlixBlackout/Student-Performance-Analyzer

Railway-specific production app that properly handles Railway's PORT requirements
"""

import os
import warnings
from app import create_app, db

# Suppress scikit-learn warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

app = create_app()

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

# Railway health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'STA Railway App'}, 200

# Railway-specific configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Railway app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
