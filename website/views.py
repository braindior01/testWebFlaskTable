from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    print('test lapet kelen')

    return render_template("home.html")


# @views.route('/file-processing')
# def lapet():
#     print('test lapet kelen')

#     return render_template("input_buysell_val.html")


@views.route('/read-table')
def kentut():
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Date']

    return render_template("read_table.html", columns=columns)

# @views.route('/read-table2')
# def asem():
#     columns = ['Code','BVal','SVal','Balance','Ratio', 'Date']

#     return render_template("table_2.html", columns=columns)

# @views.route('/input-hargawajar')
# def mamam():

#     return render_template("input_harga_wajar.html")

# @views.route('/input-hargaclosing')
# def enak():

#     return render_template("input_harga_closing.html")

# @views.route('/test-input-txt')
# def good():

#     return render_template("test_per.html")

@views.route('/read-harga-wajar')
def balsem():
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Close Price', 'Harga Wajar', 'Date']

    return render_template("read_table_HW.html", columns=columns)
