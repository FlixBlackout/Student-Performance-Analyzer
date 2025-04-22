# Student Performance Analyzer

A web-based application that uses machine learning to predict student performance based on various factors such as previous grades, attendance, and study hours.

## Features

- **Separate Login Systems**: Different interfaces for students and faculty
- **Student Features**:
  - Register and create a profile
  - Enroll in subjects
  - Enter performance data (previous grades, attendance, study hours)
  - View predicted scores based on ML model
  - Track performance across different subjects
- **Faculty Features**:
  - View all registered students
  - Manage subjects
  - Analyze individual student performance
  - Access overall analytics and insights
- **Machine Learning Model**:
  - Predicts student scores based on previous grades, attendance, and study hours
  - Initialized with synthetic data and improves as more real data is added

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd STA
```

2. Create a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Run the application:
```
python run.py
```

5. Access the application in your web browser at `http://127.0.0.1:5000/`

## Project Structure

```
STA/
├── app/
│   ├── models/
│   │   ├── user.py          # Database models
│   │   └── ml_model.py      # Machine learning prediction model
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── student.py       # Student routes
│   │   └── faculty.py       # Faculty routes
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   │   ├── student/         # Student templates
│   │   ├── faculty/         # Faculty templates
│   │   └── base.html        # Base template
│   └── __init__.py          # Application factory
├── requirements.txt         # Dependencies
└── run.py                   # Application entry point
```

## Usage

### For Students:
1. Register as a student and complete your profile
2. Enroll in available subjects
3. Add your performance data (previous grades, attendance, study hours)
4. View your predicted scores and performance analytics

### For Faculty:
1. Register as faculty and complete your profile
2. Add subjects for students to enroll in
3. View student performance data and analytics
4. Analyze individual student performance and provide recommendations

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap, Chart.js
- **Database**: SQLite
- **Machine Learning**: scikit-learn (Random Forest Regressor)
- **Data Visualization**: Matplotlib, Chart.js

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deployment

### Deploying to Heroku

1. Create a Heroku account at [heroku.com](https://heroku.com) if you don't have one
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Login to Heroku from the terminal:
```
heroku login
```
4. Create a new Heroku app:
```
heroku create sta-performance-analyzer
```
5. Initialize a git repository (if not already done):
```
git init
git add .
git commit -m "Initial commit"
```
6. Add the Heroku remote:
```
heroku git:remote -a sta-performance-analyzer
```
7. Push to Heroku:
```
git push heroku main
```
8. Set up environment variables:
```
heroku config:set SECRET_KEY=your-secure-secret-key
```
9. Open the deployed application:
```
heroku open
```

### Deploying to PythonAnywhere

1. Sign up for a PythonAnywhere account at [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Upload your code to PythonAnywhere using Git or by uploading a ZIP file
3. Create a new web app from the Web tab
4. Set up a virtual environment and install dependencies:
```
mkvirtualenv --python=/usr/bin/python3.9 myenv
pip install -r requirements.txt
```
5. Configure your web app to point to your Flask application
6. Set environment variables in the WSGI configuration file
7. Reload your web app

### Deploying to Vercel

1. Install Vercel CLI:
```
npm i -g vercel
```
2. Create a `vercel.json` file in your project root:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ]
}
```
3. Deploy to Vercel:
```
vercel
```

## Important Notes for Production Deployment

1. Use a production-ready database like PostgreSQL instead of SQLite
2. Set up proper email functionality for password reset
3. Configure proper logging and error handling
4. Set up HTTPS for secure connections
5. Implement proper backup strategies for your database
6. Consider using a content delivery network (CDN) for static assets
