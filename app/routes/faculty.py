from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from app import db
from app.models.user import User, StudentProfile, FacultyProfile, Subject, StudentPerformance, StudentSubject

faculty = Blueprint('faculty', __name__)

@faculty.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    # Get faculty profile
    profile = FacultyProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('faculty.profile'))
    
    # Get all subjects
    subjects = Subject.query.all()
    
    # Get all students
    students = StudentProfile.query.all()
    
    # Get overall performance stats
    performance_data = StudentPerformance.query.all()
    
    # Count of students with performance data
    students_with_data = db.session.query(StudentPerformance.student_id).distinct().count()
    
    # Average predicted score across all students and subjects
    avg_predicted_score = 0
    if performance_data:
        valid_scores = [p.predicted_score for p in performance_data if p.predicted_score is not None]
        avg_predicted_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    
    return render_template('faculty/dashboard.html', 
                          profile=profile,
                          subjects=subjects,
                          students=students,
                          students_with_data=students_with_data,
                          avg_predicted_score=avg_predicted_score)

@faculty.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    profile = FacultyProfile.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        department = request.form.get('department')
        
        if not profile:
            # Create new profile
            profile = FacultyProfile(
                user_id=current_user.id,
                first_name=first_name,
                last_name=last_name,
                department=department
            )
            db.session.add(profile)
        else:
            # Update existing profile
            profile.first_name = first_name
            profile.last_name = last_name
            profile.department = department
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('faculty.dashboard'))
    
    return render_template('faculty/profile.html', profile=profile)

@faculty.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        
        # Check if subject with code already exists
        existing_subject = Subject.query.filter_by(code=code).first()
        if existing_subject:
            flash('A subject with this code already exists.')
            return redirect(url_for('faculty.subjects'))
        
        # Create new subject
        subject = Subject(name=name, code=code)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!')
        return redirect(url_for('faculty.subjects'))
    
    # Get all subjects
    subjects = Subject.query.all()
    
    return render_template('faculty/subjects.html', subjects=subjects)

@faculty.route('/students')
@login_required
def students():
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    # Get faculty profile
    profile = FacultyProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('faculty.profile'))
    
    # Get all students with their related data
    students = StudentProfile.query.all()
    
    # For each student, get their subjects and performance data
    for student in students:
        student.subject_count = StudentSubject.query.filter_by(student_id=student.id).count()
        student.performance_count = StudentPerformance.query.filter_by(student_id=student.id).count()
    
    return render_template('faculty/students.html', students=students, profile=profile)

@faculty.route('/student/<int:student_id>')
@login_required
def student_details(student_id):
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    # Get faculty profile
    profile = FacultyProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('faculty.profile'))
    
    # Get student profile
    student = StudentProfile.query.get_or_404(student_id)
    
    # Get student's performance data
    performances = StudentPerformance.query.filter_by(student_id=student_id).all()
    
    # Generate performance charts
    charts = []
    if performances:
        # Prepare data for charts
        subjects = [p.subject.name for p in performances if p.subject]
        predicted_scores = [p.predicted_score for p in performances]
        previous_grades = [p.previous_grade for p in performances]
        attendance = [p.attendance_percentage for p in performances]
        study_hours = [p.study_hours for p in performances]
        
        # Create bar chart comparing predicted scores with previous grades
        plt.figure(figsize=(10, 6))
        x = np.arange(len(subjects))
        width = 0.35
        
        plt.bar(x - width/2, previous_grades, width, label='Previous Grade')
        plt.bar(x + width/2, predicted_scores, width, label='Predicted Score')
        
        plt.xlabel('Subjects')
        plt.ylabel('Score')
        plt.title('Previous Grades vs Predicted Scores')
        plt.xticks(x, subjects, rotation=45)
        plt.legend()
        plt.tight_layout()
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        comparison_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Grades Comparison', comparison_chart))
        plt.close()
        
        # Create scatter plot of attendance vs predicted score
        plt.figure(figsize=(8, 6))
        plt.scatter(attendance, predicted_scores)
        
        for i, subject in enumerate(subjects):
            plt.annotate(subject, (attendance[i], predicted_scores[i]))
            
        plt.xlabel('Attendance (%)')
        plt.ylabel('Predicted Score')
        plt.title('Attendance vs Predicted Score')
        plt.grid(True)
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        attendance_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Attendance Impact', attendance_chart))
        plt.close()
        
        # Create scatter plot of study hours vs predicted score
        plt.figure(figsize=(8, 6))
        plt.scatter(study_hours, predicted_scores)
        
        for i, subject in enumerate(subjects):
            plt.annotate(subject, (study_hours[i], predicted_scores[i]))
            
        plt.xlabel('Study Hours per Week')
        plt.ylabel('Predicted Score')
        plt.title('Study Hours vs Predicted Score')
        plt.grid(True)
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        study_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Study Hours Impact', study_chart))
        plt.close()
    
    return render_template('faculty/student_details.html', 
                          student=student,
                          performances=performances,
                          charts=charts,
                          profile=profile)

@faculty.route('/analytics')
@login_required
def analytics():
    if current_user.role != 'faculty':
        flash('Access denied. You are not a faculty member.')
        return redirect(url_for('auth.index'))
    
    # Get all performance data
    performances = StudentPerformance.query.all()
    
    # Generate analytics charts
    charts = []
    if performances:
        # Prepare data
        data = pd.DataFrame([
            {
                'student_id': p.student_id,
                'student_name': f"{p.student.first_name} {p.student.last_name}",
                'subject_id': p.subject_id,
                'subject_name': p.subject.name,
                'previous_grade': p.previous_grade,
                'attendance': p.attendance_percentage,
                'study_hours': p.study_hours,
                'predicted_score': p.predicted_score
            }
            for p in performances
        ])
        
        # Overall distribution of predicted scores
        plt.figure(figsize=(10, 6))
        plt.hist(data['predicted_score'], bins=10, alpha=0.7)
        plt.xlabel('Predicted Score')
        plt.ylabel('Number of Students')
        plt.title('Distribution of Predicted Scores')
        plt.grid(True)
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        score_dist_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Score Distribution', score_dist_chart))
        plt.close()
        
        # Correlation between factors and predicted scores
        plt.figure(figsize=(10, 6))
        
        # Calculate correlations
        correlations = [
            data['previous_grade'].corr(data['predicted_score']),
            data['attendance'].corr(data['predicted_score']),
            data['study_hours'].corr(data['predicted_score'])
        ]
        
        factors = ['Previous Grade', 'Attendance', 'Study Hours']
        
        plt.bar(factors, correlations)
        plt.xlabel('Factors')
        plt.ylabel('Correlation with Predicted Score')
        plt.title('Impact of Different Factors on Predicted Score')
        plt.grid(True)
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        correlation_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Factor Impact', correlation_chart))
        plt.close()
        
        # Average predicted score by subject
        subject_avg = data.groupby('subject_name')['predicted_score'].mean().reset_index()
        
        plt.figure(figsize=(12, 6))
        plt.bar(subject_avg['subject_name'], subject_avg['predicted_score'])
        plt.xlabel('Subject')
        plt.ylabel('Average Predicted Score')
        plt.title('Average Predicted Score by Subject')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        subject_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(('Subject Performance', subject_chart))
        plt.close()
    
    return render_template('faculty/analytics.html', charts=charts)
