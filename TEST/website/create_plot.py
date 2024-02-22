from flask import Blueprint, render_template, request, flash, jsonify
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

create_plot = Blueprint('create_plot', __name__)

@create_plot.route('/create-plot', methods=['GET', 'POST'])
def input_file():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_excel(input_file)
        if ('Code' in df.columns):
            print(df)
            y_1 = df['BVal']
            y_2 = df['SVal']
            # y_3 = df['Ratio']
            # y_4 = df['Balance']
            x = df['Date']
            plt.plot(x,y_1,marker='o')
            plt.plot(x,y_2,marker='o')
            # plt.plot(x,y_3,marker='o')
            # plt.plot(x,y_4,marker='o')
            plt.grid()
            plt.rcParams["figure.figsize"] = [15, 5]
            plt.rcParams["figure.autolayout"] = True
            legend_drawn_flag = True
            plt.legend(['BVal', 'SVal'], loc=0, frameon=legend_drawn_flag)
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
            plot_file = "plot.png"
            plt.savefig(plot_file)
            print('test lapet')

            json_response = {'response': "SUCCESS",
                             'total emiten': 'total_emiten',
                             'total val': 'today'
                             }
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("lari.html")