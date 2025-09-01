#!/usr/bin/env python3
"""
Local deployment test script for STA (Student Performance Analyzer)
This script helps you test the full application locally before deploying to production.
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 STA Full Application Local Deployment Test")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version
    print(f"🐍 Python Version: {python_version}")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required for ML dependencies")
        return
    
    # Install full requirements
    print("\n1. Installing Full Requirements (including ML libraries)...")
    if not run_command("pip install -r requirements-full.txt", "Installing dependencies"):
        print("💡 Tip: Consider creating a virtual environment first:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # On Windows")
        print("   source venv/bin/activate  # On Linux/Mac")
        return
    
    # Set environment variables
    print("\n2. Setting up environment variables...")
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SECRET_KEY'] = 'development-secret-key-change-in-production'
    print("✅ Environment variables set")
    
    # Test the application
    print("\n3. Testing the full application...")
    print("🔄 Starting Flask development server...")
    print("📱 Open your browser to: http://127.0.0.1:5000")
    print("🧠 ML features will be available!")
    print("\n⭐ Features to test:")
    print("   - Student registration and login")
    print("   - Faculty dashboard")
    print("   - Performance data entry")
    print("   - ML-powered predictions")
    print("   - Analytics and charts")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the production app
        from production_app import app
        app.run(host='127.0.0.1', port=5000, debug=True)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the STA project directory")
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Application test completed!")
        print("\n🚀 Ready for production deployment!")
        print("📖 See FULL_DEPLOYMENT_GUIDE.md for deployment instructions")

if __name__ == "__main__":
    main()