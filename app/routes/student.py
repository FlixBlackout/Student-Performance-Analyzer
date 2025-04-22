from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
import pandas as pd
import numpy as np
from app import db
from app.models.user import StudentProfile, Subject, StudentSubject, StudentPerformance
from app.models.ml_model import StudentPerformancePredictor

student = Blueprint('student', __name__)

@student.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    # Get student profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Get student subjects
    student_subjects = StudentSubject.query.filter_by(student_id=profile.id).all()
    subjects = [s.subject for s in student_subjects]
    
    # Get student performance data
    performances = StudentPerformance.query.filter_by(student_id=profile.id).all()
    
    return render_template('student/dashboard.html', 
                          profile=profile, 
                          subjects=subjects, 
                          performances=performances)

@student.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        roll_number = request.form.get('roll_number')
        
        if not profile:
            # Create new profile
            profile = StudentProfile(
                user_id=current_user.id,
                first_name=first_name,
                last_name=last_name,
                roll_number=roll_number
            )
            db.session.add(profile)
        else:
            # Update existing profile
            profile.first_name = first_name
            profile.last_name = last_name
            profile.roll_number = roll_number
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/profile.html', profile=profile)

@student.route('/subjects', methods=['GET'])
@login_required
def subjects():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Get all available subjects
    all_subjects = Subject.query.all()
    
    # Get student's enrolled subjects
    student_subjects = StudentSubject.query.filter_by(student_id=profile.id).all()
    enrolled_subject_ids = [s.subject_id for s in student_subjects]
    
    return render_template('student/subjects.html', 
                          all_subjects=all_subjects, 
                          enrolled_subject_ids=enrolled_subject_ids,
                          profile=profile)

@student.route('/subjects/add', methods=['POST'])
@login_required
def add_subject():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    name = request.form.get('name')
    code = request.form.get('code')
    
    # Check if subject with code already exists
    existing_subject = Subject.query.filter_by(code=code).first()
    if existing_subject:
        flash('A subject with this code already exists.')
        return redirect(url_for('student.subjects'))
    
    # Create new subject
    subject = Subject(name=name, code=code)
    db.session.add(subject)
    db.session.commit()
    
    # Automatically enroll the student in the subject they created
    enrollment = StudentSubject(
        student_id=profile.id,
        subject_id=subject.id
    )
    db.session.add(enrollment)
    db.session.commit()
    
    flash(f'Subject "{name}" added and enrolled successfully!')
    return redirect(url_for('student.subjects'))

@student.route('/subjects/enroll/<int:subject_id>', methods=['POST'])
@login_required
def enroll_subject(subject_id):
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Check if subject exists
    subject = Subject.query.get_or_404(subject_id)
    
    # Check if already enrolled
    existing_enrollment = StudentSubject.query.filter_by(
        student_id=profile.id, 
        subject_id=subject_id
    ).first()
    
    if existing_enrollment:
        flash(f'You are already enrolled in {subject.name}.')
    else:
        # Enroll student in subject
        enrollment = StudentSubject(
            student_id=profile.id,
            subject_id=subject_id
        )
        db.session.add(enrollment)
        db.session.commit()
        flash(f'Successfully enrolled in {subject.name}.')
    
    return redirect(url_for('student.subjects'))

@student.route('/subjects/unenroll/<int:subject_id>', methods=['POST'])
@login_required
def unenroll_subject(subject_id):
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Find enrollment
    enrollment = StudentSubject.query.filter_by(
        student_id=profile.id, 
        subject_id=subject_id
    ).first()
    
    if enrollment:
        # Also delete any performance data for this subject
        performances = StudentPerformance.query.filter_by(
            student_id=profile.id,
            subject_id=subject_id
        ).all()
        
        for performance in performances:
            db.session.delete(performance)
        
        db.session.delete(enrollment)
        db.session.commit()
        flash('Successfully unenrolled from subject.')
    else:
        flash('You are not enrolled in this subject.')
    
    return redirect(url_for('student.subjects'))

@student.route('/performance', methods=['GET'])
@login_required
def performance():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Get student's enrolled subjects
    student_subjects = StudentSubject.query.filter_by(student_id=profile.id).all()
    subjects = [s.subject for s in student_subjects]
    
    # Get performance data
    performances = StudentPerformance.query.filter_by(student_id=profile.id).all()
    
    return render_template('student/performance.html', 
                          profile=profile,
                          subjects=subjects,
                          performances=performances)

@student.route('/performance/add', methods=['GET', 'POST'])
@login_required
def add_performance():
    if current_user.role != 'student':
        flash('Access denied. You are not a student.')
        return redirect(url_for('auth.index'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your profile first.')
        return redirect(url_for('student.profile'))
    
    # Get student's enrolled subjects
    student_subjects = StudentSubject.query.filter_by(student_id=profile.id).all()
    subjects = [s.subject for s in student_subjects]
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        previous_grade = float(request.form.get('previous_grade'))
        attendance = float(request.form.get('attendance'))
        study_hours = float(request.form.get('study_hours'))
        
        # Validate input
        if previous_grade < 0 or previous_grade > 100:
            flash('Previous grade must be between 0 and 100.')
            return redirect(url_for('student.add_performance'))
        
        if attendance < 0 or attendance > 100:
            flash('Attendance must be between 0 and 100.')
            return redirect(url_for('student.add_performance'))
        
        if study_hours < 0:
            flash('Study hours cannot be negative.')
            return redirect(url_for('student.add_performance'))
        
        # Check if performance data already exists for this subject
        existing_performance = StudentPerformance.query.filter_by(
            student_id=profile.id,
            subject_id=subject_id
        ).first()
        
        # Predict performance using ML model
        predictor = StudentPerformancePredictor()
        features = np.array([[previous_grade, attendance, study_hours]])
        predicted_score = predictor.predict(features)
        
        if existing_performance:
            # Update existing performance data
            existing_performance.previous_grade = previous_grade
            existing_performance.attendance_percentage = attendance
            existing_performance.study_hours = study_hours
            existing_performance.predicted_score = predicted_score
        else:
            # Create new performance data
            performance = StudentPerformance(
                student_id=profile.id,
                subject_id=subject_id,
                previous_grade=previous_grade,
                attendance_percentage=attendance,
                study_hours=study_hours,
                predicted_score=predicted_score
            )
            db.session.add(performance)
        
        db.session.commit()
        flash('Performance data saved successfully!')
        return redirect(url_for('student.performance'))
    
    return render_template('student/add_performance.html', 
                          profile=profile,
                          subjects=subjects)
