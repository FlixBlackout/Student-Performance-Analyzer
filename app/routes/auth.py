from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User, StudentProfile, FacultyProfile

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('faculty.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        
        if user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('faculty.dashboard'))
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(email=email, username=username, role=role)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        if role == 'student':
            return redirect(url_for('auth.register_student', user_id=new_user.id))
        else:
            return redirect(url_for('auth.register_faculty', user_id=new_user.id))
    
    return render_template('register.html')

@auth.route('/register/student/<int:user_id>', methods=['GET', 'POST'])
def register_student(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        roll_number = request.form.get('roll_number')
        
        # Check if roll number already exists
        existing_profile = StudentProfile.query.filter_by(roll_number=roll_number).first()
        if existing_profile:
            flash('Roll number already exists')
            return redirect(url_for('auth.register_student', user_id=user_id))
        
        # Create student profile
        student_profile = StudentProfile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            roll_number=roll_number
        )
        
        db.session.add(student_profile)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    
    return render_template('register_student.html', user=user)

@auth.route('/register/faculty/<int:user_id>', methods=['GET', 'POST'])
def register_faculty(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        department = request.form.get('department')
        
        # Create faculty profile
        faculty_profile = FacultyProfile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            department=department
        )
        
        db.session.add(faculty_profile)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    
    return render_template('register_faculty.html', user=user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = user.generate_reset_token()
            db.session.commit()
            
            # In a real application, you would send an email with the reset link
            # For this demo, we'll just display the reset link
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Password reset link: {reset_url}')
            
            # Redirect to login page with success message
            flash('Password reset instructions have been sent to your email.')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email address.')
    
    return render_template('forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    # Find user with this token
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset link. Please try again.')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('reset_password.html', token=token)
        
        user.set_password(password)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Your password has been reset successfully. Please login with your new password.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', token=token)
