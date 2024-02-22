from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    print('test lapet kelen')

    return render_template("home.html")

@views.route('/create-plot')
def lapet():
    print('test lapet kelen')

    return render_template("lari.html")