# app/__init__.py
import os
from flask import Flask
from flask_bootstrap import Bootstrap

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)