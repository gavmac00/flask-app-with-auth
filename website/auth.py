from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
"""
The werkzeug.security module provides facilities for hashing passwords.
It supports PBKDF2, SHA256, SHA1, MD5, BCRYPT, and more.
"""

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the email exists in the database
        user = User.query.filter_by(email=email).first() # first() returns the first result, all() returns all results
        if user:
            if check_password_hash(user.password, password): # check if the password is correct
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # remember=True means that the user will stay logged in even after closing the browser
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required # the user must be logged in to access this route
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first-name')
        password = request.form.get('password')
        
        # check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 15:
            flash('Password must be greater than 14 characters.', category='error')
        else:
            new_user = User(first_name=firstName, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user) # add the new user to the database
            db.session.commit() # commit the changes to the database
            login_user(new_user, remember=True) # remember=True means that the user will stay logged in even after closing the browser
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)