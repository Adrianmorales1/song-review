from flask_app import app
from flask import Flask, request, redirect, session, render_template, flash
from flask_app.models.review import Review
from flask_app.models.user import User
from flask_app.controllers import users
from flask_app.models.track import Track


@app.route('/add/review/one', methods = ['POST'])
def add_reviews():
    data_review = {
        'user_id' : session['user_id'],
        'content' : request.form['content'],
        'rating' : request.form['rating'],
        'track_id' : request.form['track_id'],
        'content' : request.form['content']
    }
    Review.save_review(data_review)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    if not User.validate_session(session):
        return redirect('/')
    review_data = {
        'id' : id
    } 
    Review.delete_review(review_data)
    return redirect('/profile/page')

@app.route('/reviews/favorite', methods = ['POST'])
def favorite_review():
    Review.favorite(request.form)
    return redirect('/dashboard')
@app.route('/reviews/unfavorite', methods = ['POST'])
def unfavorite_review():
    Review.unfavorite(request.form)
    return redirect('/dashboard')

@app.route('/track/search')
def testing():
    if session.get('track_list') == None:
        return render_template('search_song.html')
    else :
        track_list1 = session['track_list']
        session.pop('track_list')
        return render_template('search_song.html', track_list = track_list1)
    

@app.route('/searching', methods = ['POST'])
def track_search():
    query = request.form['query']
    if len(query) < 1:
        flash("Search must have at least one character")
        return redirect('/track/search')
    track_list = Track.search_query(query)
    session['track_list'] = track_list
    return redirect('/track/search')

@app.route('/track/review/<string:track_id>')
def review_track(track_id):
    track_data = Track.get_one_track_by_id(track_id)
    return render_template('add_review.html', track = track_data)

@app.route('/profile/user/<int:user_id>')
def user_profile(user_id):
    data = {
        'id' : user_id
    }
    user_data = User.get_user_by_id(data)
    all_reviews1 = Review.get_all_reviews_with_one_user(data)
    all_tracks1 = []
    for review in all_reviews1:
        print(Track.get_one_track_by_id(review.track_id))
        all_tracks1.append(Track.get_one_track_by_id(review.track_id))
    return render_template("user_profile.html", user = user_data, all_reviews = all_reviews1, all_tracks = all_tracks1)