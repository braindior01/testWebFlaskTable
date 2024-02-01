from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
from .models import create_table_1, create_table_2, insert_to_table_1, insert_to_table_2
from datetime import date
from datetime import timedelta

bacafile = Blueprint('bacafile', __name__)

@bacafile.route('/file-processing',methods=['GET', 'POST'])
def input_file():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, sep=';')
        print(df)
        if('BVal' in df.columns):      
            BCode = df['BCode']
            BVal = df['BVal']
            SCode = df['SCode']
            SVal = df['SVal']
            today = date.today()
            yesterday = today - timedelta(days = 15)
            print(BCode)
            create_table_1()
            create_table_2()
            for EmitenBuy, BuyVal in zip(BCode, BVal):
                insert_to_table_1(value_1=EmitenBuy, value_2=BuyVal, value_3=yesterday)

            for EmitenSell, SellVal in zip(SCode, SVal):
                insert_to_table_2(value_1=EmitenSell, value_2=SellVal, value_3=yesterday)

            json_response={'response':"SUCCESS",
                           'total emiten': 'Ok',
                           'total val': 'Ok'
                          }
            json_response=jsonify(json_response)
            return json_response
        else:
            json_response={'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("test_file_input.html")