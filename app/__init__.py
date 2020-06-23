# app/__init__.py
import os
from flask import Flask
from flask_bootstrap import Bootstrap

import logging

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

logging.basicConfig(filename='nima.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S', level=logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)