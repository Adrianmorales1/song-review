from flask_app import app
from flask import Flask, request, redirect, session, render_template, flash
from flask_app.models.review import Review
from flask_app.models.user import User
from flask_app.controllers import users


@app.route('/add/review')
def add_review():
    return render_template("add_review.html")

@app.route('/add/review/one', methods = ['POST'])
def add_reviews():
    data_review = {
        'user_id' : session['user_id'],
        'title' : request.form['title'],
        'rating' : request.form['rating'],
        'date_watched' : request.form['date_watched'],
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