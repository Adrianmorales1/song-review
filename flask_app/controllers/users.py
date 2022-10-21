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
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register2.html')

@app.route('/reg/user', methods = ['POST'])
def register_user():
    if not User.validate_reg(request.form):
        flash('Incorrect Email')
        return redirect('/register')

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
    data = {
        'id' : session['user_id']
    }
    user_data = User.get_user_by_id(data)
    all_reviews1 = Review.get_all_review_with_user()
    all_tracks1 = []
    for review in all_reviews1:
        print(Track.get_one_track_by_id(review.track_id))
        all_tracks1.append(Track.get_one_track_by_id(review.track_id))
    return render_template('home_page.html', all_reviews = all_reviews1, all_tracks = all_tracks1, user = user_data)

@app.route('/edit_profile/<int:user_id>') #This is going to be the route for the Render of the Edit html
def edit_profile_page(user_id): 
    if not User.validate_session(session):
       return redirect('/')
    data = {
        'id': user_id
    }
    user = User.get_user_by_id(data)
    return render_template('edit_profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    User.update_user(data)
    return redirect('/profile/page')

@app.route('/profile/page')
def profile_page():
    if not User.validate_session(session):
       return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user_data = User.get_user_by_id(data)
    all_reviews1 = Review.get_all_reviews_with_one_user(data)
    all_tracks1 = []
    for review in all_reviews1:
        print(Track.get_one_track_by_id(review.track_id))
        all_tracks1.append(Track.get_one_track_by_id(review.track_id))
    return render_template('profile_page.html', user = user_data, all_reviews = all_reviews1, all_tracks = all_tracks1)

@app.route('/profile/user/<int:id>')
def user_profile_page(id):
    if not User.validate_session(session):
       return redirect('/')
    data = {
        'id' : id
    }
    user_data = User.get_user_by_id(data)
    all_reviews1 = Review.get_all_reviews_with_one_user(data)
    all_tracks1 = []
    for review in all_reviews1:
        print(Track.get_one_track_by_id(review.track_id))
        all_tracks1.append(Track.get_one_track_by_id(review.track_id))
    return render_template('user_profile.html', user = user_data, all_reviews = all_reviews1, all_tracks = all_tracks1)

@app.route('/reset')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/testing')
def testing2():
    return render_template('register2.html')
@app.route('/testing2')
def testing3():
    return render_template('login.html')