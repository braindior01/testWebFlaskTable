from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    print('test lapet kelen')

    return render_template("home.html")


@views.route('/file-processing')
def lapet():
    print('test lapet kelen')

    return render_template("test_file_input.html")


@views.route('/read-table')
def kentut():
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Date']

    return render_template("test_table.html", columns=columns)

# @views.route('/read-table2')
# def asem():
#     columns = ['Code','BVal','SVal','Balance','Ratio', 'Date']

#     return render_template("table_2.html", columns=columns)

# @views.route('/input-PER')
# def mamam():

#     return render_template("input_PER_PBV.html")