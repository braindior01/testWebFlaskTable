from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
from .models import create_table_1, create_table_2, insert_to_table_1, insert_to_table_2, read_table, create_table_3, insert_to_table_3, insert_to_table_4, create_table_4
from datetime import timedelta
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

bacafile = Blueprint('bacafile', __name__)


@bacafile.route('/file-processing', methods=['GET', 'POST'])
def input_file():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, sep=';')
        today = request.form['inputDate']
        print(today)
        if ('BVal' in df.columns):
            BCode = df['BCode']
            BVal = df['BVal']
            SCode = df['SCode']
            SVal = df['SVal']
            # today = date.today()
            # yesterday = today - timedelta(days=1)
            # date_input = datetime.strptime(today, '%d/%m/%y')
            total_emiten = len(set(BCode))
            create_table_1()
            create_table_2()
            for EmitenBuy, BuyVal in zip(BCode, BVal):
                insert_to_table_1(value_1=EmitenBuy,
                                  value_2=BuyVal, value_3=today)

            for EmitenSell, SellVal in zip(SCode, SVal):
                insert_to_table_2(value_1=EmitenSell,
                                  value_2=SellVal, value_3=today)

            json_response = {'response': "SUCCESS",
                             'total emiten': total_emiten,
                             'total val': today
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            json_response = {
                'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("input_buysell_val.html")


@bacafile.route('/read-table', methods=['GET', 'POST'])
def read_table():
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Close Price','Date']
    if request.method == 'POST':
        # submit = request.form['inputText']
        date_input = request.form['inputDate']
        emiten_input = request.form['inputEmiten']
        print(date_input)
        if emiten_input == "":
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date WHERE Buy.unix_date = ? AND Sell.unix_date = ? ORDER BY RATIO DESC"
            cursor.execute(query, (date_input, date_input))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)
        elif date_input == "" :
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date WHERE Buy.unix_date = Sell.unix_date AND buy.EmitenBuy = ? ORDER BY Buy.unix_date DESC"
            cursor.execute(query, (emiten_input,))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)
        else:
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date WHERE Buy.unix_date = ? AND Sell.unix_date = ? AND Buy.EmitenBuy= ?"
            cursor.execute(query, (date_input, date_input, emiten_input))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)


    return render_template("read_table.html", columns=columns, data=data, date_input=date_input, num_rows=num_rows)


@bacafile.route('/input-hargawajar', methods=['GET', 'POST'])
def input_file_harga_wajar():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_excel(input_file)
        if ('Bcode' in df.columns):
            BCode = df['Bcode']
            Harga_Wajar = df['Harga_Wajar']
            create_table_3()
            for Emiten, Harga_Wajar in zip(BCode, Harga_Wajar):
                insert_to_table_3(value_1=Emiten,
                                  value_2=Harga_Wajar)

            json_response = {'response': "SUCCESS",
                             'total emiten': 'Ok',
                             'total val': 'Ok'
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            json_response = {
                'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("input_harga_wajar.html")

@bacafile.route('/input-hargaclosing', methods=['GET', 'POST'])
def input_file_closing():
    if request.method == 'POST':
        input_file = request.files['inputFile_Closing']
        df = pd.read_excel(input_file)
        today = request.form['inputDate']
        if ('Kode Saham' in df.columns):
            BCode = df['Kode Saham']
            Close = df['Penutupan']
            total_emiten = len(set(BCode))
            create_table_4()
            for Emiten, Close_Price in zip(BCode, Close):
                insert_to_table_4(value_1=Emiten,
                                  value_2=Close_Price, value_3=today)

            json_response = {'response': "SUCCESS",
                             'total emiten': total_emiten,
                             'date_inputed': today
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            json_response = {
                'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("input_harga_closing.html")

@bacafile.route('/test-input-txt', methods=['GET', 'POST'])
def test_input_txt():
    if request.method == 'POST':
        lapet = request.form['inputEmiten']
        bakpao = request.form['input_PER']
        sampai = request.form['input_PBV']

        print(lapet)
        json_response = {'response': bakpao,
                             'total emiten': lapet,
                             'date_inputed': sampai
                             }
        json_response = jsonify(json_response)
        return json_response
    else:
        return render_template("test_per.html")
    
@bacafile.route('/read-harga-wajar', methods=['GET', 'POST'])
def baca_harga_wajar():
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Close Price', 'Harga Wajar', 'Date']
    if request.method == 'POST':
        # submit = request.form['inputText']
        date_input = request.form['inputDate']
        emiten_input = request.form['inputEmiten']
        print(date_input)
        if emiten_input == "":
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, harga_wajar.Harga_Wajar, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell AND Buy.unix_date = Sell.unix_date INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date INNER JOIN harga_wajar ON Buy.EmitenBuy = harga_wajar.Emiten WHERE Buy.unix_date = ? AND Sell.unix_date = ? ORDER BY BuyVal DESC"
            cursor.execute(query, (date_input, date_input))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)
        elif date_input == "" :
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, harga_wajar.Harga_Wajar, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell AND Buy.unix_date = Sell.unix_date INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date INNER JOIN harga_wajar ON Buy.EmitenBuy = harga_wajar.Emiten WHERE Buy.unix_date = Sell.unix_date AND Buy.EmitenBuy= ? AND Sell.EmitenSell = ? ORDER BY Buy.unix_date ASC"
            cursor.execute(query, (emiten_input, emiten_input))
            data = cursor.fetchall()
            num_rows = len(data)
            x_values = [row[7] for row in data]
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in x_values]
            buy_values = [row[1] for row in data]
            sell_values = [row[2] for row in data]
            y_values = [row[4] for row in data]
            closing_values = [row[5] for row in data]

            title = [row[0] for row in data][0]

            fig, axs = plt.subplots(3, 1, figsize=(12, 8))
            axs[0].plot(dates,buy_values,marker='o')
            axs[0].plot(dates,sell_values,marker='o')
            axs[0].grid(True)
            axs[0].set_title(title)
            axs[0].legend_drawn_flag = True
            axs[0].legend(['Buy', 'Sell'], loc=2)
            axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=3))
            axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            axs[1].plot(dates,y_values,marker='o')
            axs[1].grid(True)
            axs[1].legend_drawn_flag = True
            axs[1].legend(['Ratio'], loc=2)
            axs[1].xaxis.set_major_locator(mdates.DayLocator(interval=3))
            axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            axs[2].plot(dates,closing_values,marker='o')
            axs[2].grid(True)
            axs[2].legend_drawn_flag = True
            axs[2].legend(['Close Price'], loc=2)
            axs[2].xaxis.set_major_locator(mdates.DayLocator(interval=3))
            axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
           
            plot_file = "website/static/plot.png"
            plt.savefig(plot_file, dpi=100)
        else:
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, harga_wajar.Harga_Wajar, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell AND Buy.unix_date = Sell.unix_date INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date INNER JOIN harga_wajar ON Buy.EmitenBuy = harga_wajar.Emiten WHERE Buy.unix_date = ? AND Sell.unix_date = ? AND Buy.EmitenBuy= ? AND Sell.EmitenSell = ?"
            cursor.execute(query, (date_input, date_input, emiten_input, emiten_input))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)

    return render_template("read_table_HW.html", columns=columns, data=data, date_input=date_input, num_rows=num_rows)


