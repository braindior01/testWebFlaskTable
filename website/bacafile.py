from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
from .models import create_table_1, create_table_2, insert_to_table_1, insert_to_table_2, read_table, create_table_3, insert_to_table_3, insert_to_table_4, create_table_4
from datetime import date
from datetime import timedelta
import sqlite3
from datetime import datetime

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
    columns = ['Code','BVal','SVal','Balance','Ratio', 'Date']
    if request.method == 'POST':
        # submit = request.form['inputText']
        date_input = request.form['inputDate']
        emiten_input = request.form['inputEmiten']
        print(date_input)
        if emiten_input == "":
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = ? AND Sell.unix_date = ? LIMIT 100"
            cursor.execute(query, (date_input, date_input))
            data = cursor.fetchall()
            # print(data)
        elif date_input == "" :
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = Sell.unix_date AND buy.EmitenBuy = ?"
            cursor.execute(query, (emiten_input,))
            data = cursor.fetchall()
            # print(data)
        else:
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = ? AND Sell.unix_date = ? AND Buy.EmitenBuy= ?"
            cursor.execute(query, (date_input, date_input, emiten_input))
            data = cursor.fetchall()
            # print(data)


    return render_template("read_table.html", columns=columns, data=data)


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
