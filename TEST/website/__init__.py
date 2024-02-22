from flask import Flask
import pandas as pd
from os import path
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .create_plot import create_plot


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(create_plot, url_prefix='/')


    return app