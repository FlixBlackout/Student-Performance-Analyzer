from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'faculty'
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    faculty_profile = db.relationship('FacultyProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.now() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        if self.reset_token != token:
            return False
        if datetime.now() > self.reset_token_expiry:
            return False
        return True
    
    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expiry = None
    
    def __repr__(self):
        return f'<User {self.username}>'


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    subjects = db.relationship('StudentSubject', backref='student', cascade='all, delete-orphan')
    performances = db.relationship('StudentPerformance', backref='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<StudentProfile {self.first_name} {self.last_name}>'


class FacultyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<FacultyProfile {self.first_name} {self.last_name}>'


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    student_subjects = db.relationship('StudentSubject', backref='subject', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class StudentSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    def __repr__(self):
        return f'<StudentSubject {self.id}>'


class StudentPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    previous_grade = db.Column(db.Float, nullable=False)  # Previous grade in the subject
    current_grade = db.Column(db.Float, nullable=True)    # Current grade in the subject
    attendance_percentage = db.Column(db.Float, nullable=False)  # Attendance percentage
    study_hours = db.Column(db.Float, nullable=False)  # Weekly study hours
    predicted_score = db.Column(db.Float, nullable=True)  # ML predicted score
    
    # Relationship
    subject = db.relationship('Subject')
    
    def __repr__(self):
        return f'<StudentPerformance {self.id}>'
