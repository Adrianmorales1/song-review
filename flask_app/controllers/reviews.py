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
    return redirect('/dashboard')

@app.route('/reviews/<int:id>/favorite', methods = ['POST'])
def favorite_review(id):
    Review.favorite(request.form)
    return redirect('/dashboard')
@app.route('/reviews/<int:id>/unfavorite', methods = ['POST'])
def unfavorite_review(id):
    Review.unfavorite(request.form)
    return redirect('/dashboard')

@app.route('/track/search')
def testing():
    if session.get('track_list') == None:
        return render_template('search_song.html')
    else :
        return render_template('search_song.html', track_list = session['track_list'])
    

@app.route('/searching', methods = ['POST'])
def track_search():
    query = request.form['query']
    track_list = Track.search_query(query)
    session['track_list'] = track_list
    return redirect('/track/search')

@app.route('/track/review/<string:track_id>')
def review_track(track_id):
    track_data = Track.get_one_track_by_id(track_id)
    return render_template('add_review.html', track = track_data)