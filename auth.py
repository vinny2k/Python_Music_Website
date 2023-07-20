# stores functions for login and register logic
# need to test each function before committing

import boto3
import logging
from botocore.exceptions import ClientError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models.user import User
"""
code adapted from:

    Registering Blueprints section
    Pallets, “Modular Applications with Blueprints,” Flask. [Online]. Available: https://flask.palletsprojects.com/en/2.2.x/blueprints/. [Accessed: 22-Mar-2023]. 

    Flask-Login sections
    “Flask-Login,” Read the Docs. [Online]. Available: https://flask-login.readthedocs.io/en/latest/. [Accessed: 10-Mar-2023]. 
    
    auth.py
    techwithtim, "Flask Web App Tutorial", Available: https://github.com/techwithtim/Flask-Web-App-Tutorial. [Accessed: 22-Mar-2023].
"""
auth = Blueprint('auth', __name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = dynamodb.Table('Login').get_item(Key={'Email': email})
        
        if next(iter(user)) != "Item":
            flash("Email or password is invalid.", category='error')
        else:
            if password == user["Item"].get("Password"):
                authed_user = User(user["Item"].get("User_name"), user["Item"].get(
                    "Email"), user["Item"].get("Password"))
                login_user(authed_user)
                return redirect(url_for('home.home1'))
            else:
                flash("Email or password is invalid.", category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# rearrange register function so that the return statements make more sense

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = dynamodb.Table('Login').get_item(Key={'Email': email})
        if next(iter(user)) != "Item":
            dynamodb.Table('Login').put_item(
                Item={
                    "Email": email,
                    "Password": password,
                    "User_name": user_name
                }
            )
            return redirect(url_for('auth.login'))
        else:
            flash('The email already exists.', category='error')
    return render_template('register.html')