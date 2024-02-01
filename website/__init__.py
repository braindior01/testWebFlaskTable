from flask import Flask
import pandas as pd
from os import path
import sqlite3

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .bacafile import bacafile

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(bacafile, url_prefix='/')

    return app