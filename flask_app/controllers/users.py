from flask_app import app
from flask import Flask, request, redirect, session, render_template, flash
from flask_app.models.track import Track
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.controllers import reviews
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/reg/user', methods = ['POST'])
def register_user():
    if not User.validate_reg(request.form):
        flash('Incorrect Email')
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    register_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    print(register_data)
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
    user_data = session['user_id']
    all_reviews1 = Review.get_all_review_with_user()
    all_review_tracks1 = []
    for review in all_reviews1:
        print(Track.get_one_track_by_id(review.track_id))
        all_review_tracks1.append(Track.get_one_track_by_id(review.track_id))
    return render_template('home_page.html', all_reviews = all_reviews1, all_review_tracks = all_review_tracks1)

@app.route('/edit_profile/<int:user_id>') #This is going to be the route for the Render of the Edit html
def edit_profile_page(user_id): 
    data = {
        'id': user_id
    }
    user = User.get_user_by_id(data)
    print(user)
    return render_template('edit_profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    User.update_user(data)
    return redirect('/edit_profile/<id:user_id>')

@app.route('/profile/page')
def profile_page():
    user_data = User.get_user_by_id(session['user_id'])
    return render_template('profile_page.html', user = user_data)

@app.route('/reset')
def log_out():
    session.clear()
    return redirect('/')