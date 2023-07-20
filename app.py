import boto3
import secrets
from flask import Flask, render_template
from flask_login import LoginManager
from auth import auth
from home import home
from models.user import User

"""
code adapted from Registering Blueprints section
Pallets, “Modular Applications with Blueprints,” Flask. [Online]. Available: https://flask.palletsprojects.com/en/2.2.x/blueprints/. [Accessed: 22-Mar-2023]. 
"""

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex()
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # need to properly implement: return a user based on provided email
    @login_manager.user_loader
    def load_user(email):
        # create a user object based on email and db
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        user = dynamodb.Table('Login').get_item(Key={'Email': email})
        loaded_user = User(user["Item"].get("User_name"), user["Item"].get("Email"), user["Item"].get("Password"))
        return loaded_user
    
    @app.route('/')
    def default():
        return render_template("default.html")
    
    return app

