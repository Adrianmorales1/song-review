from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "song_review"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.reviews = []
    
    @classmethod
    def save_user(cls,data):
        query = 'INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s"
        result = connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user
        
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user

    @classmethod
    def follow(cls,data):
        query = "INSERT INTO followers(user_id, follower_id) VALUES (%(user_id)s,%(id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unfollow(cls,data):
        query = "DELETE FROM followers WHERE user_id = %(user_id)s AND follower_id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    #validation static methods
    @staticmethod
    def validate_reg(data):
        is_valid = True
        user_id = User.get_user_by_email(data)
        if user_id:
            flash('Email is already registered!', 'register')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters', 'register')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be at least 3 characters', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match!', 'register')
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_user_by_email(data)
        if not user_in_db:
            flash('Email is not associated with an account!','login')
            is_valid = False
            return is_valid
        if not User.get_user_by_email(data):
            flash('Invalid Email address','login')
            is_valid = False
            return is_valid
        if len(data['password']) < 8:
            flash('password must be at least 8 characters long','login')
            is_valid = False
        return is_valid
        
    @staticmethod
    def validate_session(data):
        is_valid = True
        if "user_id" not in data:
            flash('must be logged in', 'session')
            is_valid = False
        return is_valid

    def validate_update(data):
        is_valid = True
        user_id = User.get_user_by_email(data)
        if user_id:
            if user_id.email != data['email']:
                flash('Email is already registered!', 'update')
                is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters', 'update')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be at least 3 characters', 'update')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'update')
            is_valid = False
        if is_valid:
            flash("Changes Made!", "completed")
        return is_valid