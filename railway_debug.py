#!/usr/bin/env python3
"""
Railway Deployment Debug Script
Helps diagnose common Railway deployment issues
"""

import os
import sys
import socket

def check_railway_environment():
    """Check Railway-specific environment variables and settings"""
    
    print("🚂 Railway Deployment Diagnostic")
    print("=" * 40)
    
    # Check critical environment variables
    port = os.environ.get('PORT')
    print(f"📍 PORT: {port}")
    
    if not port:
        print("❌ ERROR: PORT environment variable not set")
        print("💡 Railway requires PORT to be set automatically")
        return False
    
    try:
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            print(f"❌ ERROR: Invalid port number: {port_num}")
            return False
        print(f"✅ PORT is valid: {port_num}")
    except ValueError:
        print(f"❌ ERROR: PORT is not a number: {port}")
        return False
    
    # Check other environment variables
    env_vars = [
        'FLASK_ENV',
        'DATABASE_URL',
        'SECRET_KEY',
        'RAILWAY_ENVIRONMENT',
        'RAILWAY_PROJECT_ID'
    ]
    
    print("\n🔧 Environment Variables:")
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'SECRET' in var or 'DATABASE' in var:
                masked = value[:8] + "..." if len(value) > 8 else "***"
                print(f"   {var}: {masked}")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: Not set")
    
    # Test port binding
    print(f"\n🌐 Testing port binding on {port_num}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', port_num))
        sock.close()
        print(f"✅ Port {port_num} is available for binding")
    except OSError as e:
        print(f"❌ Cannot bind to port {port_num}: {e}")
        return False
    
    print("\n📊 System Information:")
    print(f"   Python: {sys.version}")
    print(f"   Platform: {sys.platform}")
    print(f"   Working Directory: {os.getcwd()}")
    
    return True

def test_app_import():
    """Test if the application can be imported"""
    print("\n🧪 Testing Application Import...")
    
    try:
        from railway_app import app
        print("✅ Railway app imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Cannot import railway_app: {e}")
        
        try:
            from production_app import app
            print("✅ Production app imported successfully")
            return True
        except ImportError as e2:
            print(f"❌ Cannot import production_app: {e2}")
            return False

def main():
    """Main diagnostic function"""
    
    env_ok = check_railway_environment()
    import_ok = test_app_import()
    
    print("\n📋 Diagnostic Summary:")
    print(f"   Environment: {'✅ OK' if env_ok else '❌ ISSUES'}")
    print(f"   App Import: {'✅ OK' if import_ok else '❌ ISSUES'}")
    
    if env_ok and import_ok:
        print("\n🎉 Deployment should work!")
        print("💡 If still getting 'train not arrived', check Railway dashboard for:")
        print("   - Build logs for errors")
        print("   - Service status (should be 'Active')")
        print("   - Domain configuration")
    else:
        print("\n❌ Issues detected. Fix the above problems and redeploy.")
    
    print(f"\n🔗 Test URLs to try:")
    port = os.environ.get('PORT', '5000')
    print(f"   Health: https://your-app-name.railway.app/health")
    print(f"   Status: https://your-app-name.railway.app/railway-status")

if __name__ == "__main__":
    main()