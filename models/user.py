from flask_login import UserMixin
"""
Code adapted from "Your User Class" section
“Flask-Login,” Read the Docs. [Online]. Available: https://flask-login.readthedocs.io/en/latest/. [Accessed: 10-Mar-2023]. 
"""
class User(UserMixin):
    
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.id = email
        self.password = password