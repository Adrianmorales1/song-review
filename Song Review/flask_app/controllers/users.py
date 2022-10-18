from flask_app import app
from flask import Flask, request, redirect, session, render_template, flash
from flask_app.models.review import Review
from flask_app.models.user import User
from flask_app.controllers import reviews
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('reg_log.html')

@app.route('/reg/user', methods = ['POST'])
def register_user():
    if not User.validate_reg(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    register_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.save_user(register_data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login_user():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Email/Password Combination is incorrect', 'login')
            return redirect('/')

        session['user_id'] = user.id
        flash("login was successful!")
        return redirect('/dashboard')

    flash('email is not tied to an account', 'login')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not User.validate_session(session):
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('dashboard.html', user = User.get_user_by_id(data), all_reviews = Review.get_all_review_with_user())

@app.route('/reset')
def log_out():
    session.clear()
    return redirect('/')