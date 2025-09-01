#!/usr/bin/env python3
"""
Simple production server for STA without gunicorn dependency.
Use this when gunicorn is not available or causing issues.
"""

import os
import sys
from werkzeug.serving import run_simple
from production_app import app

def main():
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting STA Server on {host}:{port}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    # Use Werkzeug's built-in server (more reliable than Flask dev server)
    run_simple(
        hostname=host,
        port=port,
        application=app,
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )

if __name__ == '__main__':
    main()