#!/usr/bin/env python3
"""
Universal deployment script for STA (Student Performance Analyzer)
Works on any platform with proper port and environment handling.
"""

import os
import sys
import subprocess

def get_port():
    """Get port with multiple fallback strategies"""
    # Try to get PORT from environment
    port_str = os.environ.get('PORT', '5000')
    
    # Handle different port variable formats
    if port_str.startswith('$'):
        # Remove $ prefix if present
        port_str = port_str[1:]
        port_str = os.environ.get(port_str, '5000')
    
    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError("Port out of range")
        return port
    except (ValueError, TypeError):
        print(f"⚠️ Warning: Invalid PORT value '{port_str}', using default 5000")
        return 5000

def main():
    # Get configuration
    port = get_port()
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("🚀 STA Universal Deployment Script")
    print(f"📍 Host: {host}")
    print(f"📍 Port: {port}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    print(f"🐍 Python: {sys.version}")
    
    # Try gunicorn first
    try:
        print("🔄 Attempting to start with gunicorn...")
        cmd = [
            sys.executable, '-m', 'gunicorn',
            'production_app:app',
            '--bind', f'{host}:{port}',
            '--workers', '2',
            '--timeout', '120',
            '--max-requests', '100',
            '--access-logfile', '-',
            '--error-logfile', '-'
        ]
        
        print(f"📝 Command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Gunicorn failed: {e}")
        print("🔄 Falling back to simple server...")
        
        # Fallback to simple server
        try:
            from simple_server import main as simple_main
            os.environ['PORT'] = str(port)
            os.environ['HOST'] = host
            simple_main()
        except ImportError:
            print("❌ Simple server not available")
            print("🔄 Using production app directly...")
            
            # Final fallback to production app
            from production_app import app
            app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()