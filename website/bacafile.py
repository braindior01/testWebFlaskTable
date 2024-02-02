from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
from .models import create_table_1, create_table_2, insert_to_table_1, insert_to_table_2, read_table
from datetime import date
from datetime import timedelta
import sqlite3

bacafile = Blueprint('bacafile', __name__)


@bacafile.route('/file-processing', methods=['GET', 'POST'])
def input_file():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, sep=';')
        print(df)
        if ('BVal' in df.columns):
            BCode = df['BCode']
            BVal = df['BVal']
            SCode = df['SCode']
            SVal = df['SVal']
            today = date.today()
            yesterday = today - timedelta(days=15)
            print(BCode)
            create_table_1()
            create_table_2()
            for EmitenBuy, BuyVal in zip(BCode, BVal):
                insert_to_table_1(value_1=EmitenBuy,
                                  value_2=BuyVal, value_3=today)

            for EmitenSell, SellVal in zip(SCode, SVal):
                insert_to_table_2(value_1=EmitenSell,
                                  value_2=SellVal, value_3=today)

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
        return render_template("test_file_input.html")


@bacafile.route('/read-table', methods=['GET', 'POST'])
def read_table():
    columns = ['Code','BVal','SVal','Balance','Ratio']
    if request.method == 'POST':
        go_to_page = request.form['inputText']
        if go_to_page == "1":
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = '2024-02-01' AND Sell.unix_date = '2024-02-01' LIMIT 100"
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)

    return render_template("test_table.html", columns=columns, data=data)
