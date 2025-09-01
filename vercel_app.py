from flask import Flask, render_template, jsonify
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sta-secure-secret-key-2025')

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>STA - Student Performance Analyzer</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body text-center">
                            <h1 class="card-title">🎓 Student Performance Analyzer</h1>
                            <p class="card-text">Your application has been successfully deployed to Vercel!</p>
                            <p class="text-muted">This is a simplified deployment version for demonstration.</p>
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <div class="card bg-primary text-white">
                                        <div class="card-body">
                                            <h5>👨‍🎓 For Students</h5>
                                            <p>Track your performance and get ML-powered predictions</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card bg-success text-white">
                                        <div class="card-body">
                                            <h5>👨‍🏫 For Faculty</h5>
                                            <p>Monitor student progress and analytics</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-4">
                                <a href="/status" class="btn btn-primary">Check Deployment Status</a>
                                <a href="/features" class="btn btn-outline-secondary">View Features</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/status')
def status():
    return jsonify({
        'status': 'success',
        'message': 'STA Application deployed successfully on Vercel!',
        'features': [
            'Student Performance Tracking',
            'Faculty Analytics Dashboard',
            'ML-Powered Predictions',
            'Responsive Bootstrap UI'
        ],
        'deployment_platform': 'Vercel',
        'version': '1.0.0'
    })

@app.route('/features')
def features():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>STA Features</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>🚀 STA Features</h1>
            <div class="row">
                <div class="col-md-6">
                    <h3>Student Features</h3>
                    <ul class="list-group">
                        <li class="list-group-item">📊 Performance tracking</li>
                        <li class="list-group-item">🤖 ML-powered score predictions</li>
                        <li class="list-group-item">📚 Subject enrollment</li>
                        <li class="list-group-item">📈 Progress analytics</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h3>Faculty Features</h3>
                    <ul class="list-group">
                        <li class="list-group-item">👥 Student management</li>
                        <li class="list-group-item">📋 Subject management</li>
                        <li class="list-group-item">📊 Analytics dashboard</li>
                        <li class="list-group-item">📈 Performance insights</li>
                    </ul>
                </div>
            </div>
            <div class="mt-4">
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
