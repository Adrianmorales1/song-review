from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import Flask, flash, session

class Review:
    db= "song_review"

    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.rating = data['rating']
        self.track_id = data['track_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.track_data = None
        self.creator = None
        self.user_who_liked= []
        self.user_ids_who_liked = []
    
    @classmethod
    def save_review(cls,data):
        query = "INSERT INTO reviews(user_id,content,rating,track_id) VALUES (%(user_id)s,%(content)s,%(rating)s,%(track_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_review(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def favorite(cls,data):
        query = "INSERT INTO likes(review_id, user_id) VALUES (%(id)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def unfavorite(cls,data):
        query = "DELETE FROM likes WHERE review_id = %(id)s AND user_id = %(user_id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all_reviews_with_one_user(cls, data):
        query = "SELECT * FROM reviews LEFT JOIN users ON reviews.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)

        all_reviews = []

        for row in results:
            one_review = cls(row)

            one_review_user_info = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }

            user_data = User(one_review_user_info)

            one_review.creator = user_data

            all_reviews.append(one_review)
        return all_reviews

    @classmethod
    def get_all_review_with_user(cls):
        #query = "SELECT * FROM reviews JOIN users ON reviews.user_id = users.id"
        query = """SELECT * FROM reviews JOIN users AS creators on reviews.user_id = creators.id
                LEFT JOIN likes ON reviews.id = likes.review_id
                LEFT JOIN users AS users_who_liked ON likes.user_id = users_who_liked.id
                ORDER BY reviews.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query)

        all_reviews = []
        for row in results:
            new_review = True
            user_who_liked_data = {
                "id" : row['users_who_liked.id'],
                "first_name" : row['users_who_liked.first_name'],
                "last_name" : row['users_who_liked.last_name'],
                "email" : row['users_who_liked.email'],
                "password" : row['users_who_liked.password'],
                "created_at" : row['users_who_liked.created_at'],
                "updated_at" : row['users_who_liked.updated_at']
            }

            number_of_reviews = len(all_reviews)
            if number_of_reviews > 0:
                last_review = all_reviews[number_of_reviews - 1]
                if last_review.id == row['id']:
                    last_review.user_ids_who_liked.append(row['users_who_liked.id'])
                    last_review.user_who_liked.append(User(user_who_liked_data))
                    new_review = False


            if new_review:

                one_review = cls(row)

                one_review_user_info = {
                    "id" : row['creators.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['creators.created_at'],
                    "updated_at" : row['creators.updated_at']
                }

                user_data = User(one_review_user_info)

                one_review.creator = user_data
                #check to see if anyone favorited 
                if row['users_who_liked.id']:
                    one_review.user_ids_who_liked.append(row['users_who_liked.id'])
                    one_review.user_who_liked.append(User(user_who_liked_data))

                all_reviews.append(one_review)
        return all_reviews

    #validation static methods
    @staticmethod
    def validate_review(data):
        is_valid = True
        if len(data['content']) < 2:
            flash('Title of Review must be at least 2 characters', 'review')
            is_valid = False
        if int(data['rating']) > 5 or int(data['rating']) < 0:
            flash('Rating of Review must be inbetween 0-10', 'review')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_delete(user, other_user):
        is_valid = True
        if user['id'] != other_user['id']:
            flash('Returned to Login form', 'session')
            is_valid = False
        return is_valid