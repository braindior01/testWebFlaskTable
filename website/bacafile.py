from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
from .models import create_table_1, create_table_2, insert_to_table_1, insert_to_table_2, read_table, create_table_3, insert_to_table_3, insert_to_table_4, create_table_4, create_table_5, insert_to_table_5
from datetime import timedelta
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, Buy.unix_date FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date WHERE Buy.unix_date = ? AND Sell.unix_date = ? AND Balance > 1000000000 ORDER BY Ratio DESC"
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


# @bacafile.route('/input-hargawajar', methods=['GET', 'POST'])
# def input_file_harga_wajar():
#     if request.method == 'POST':
#         input_file = request.files['inputFile']
#         df = pd.read_excel(input_file)
#         if ('Bcode' in df.columns):
#             BCode = df['Bcode']
#             Harga_Wajar = df['Harga_Wajar']
#             create_table_3()
#             for Emiten, Harga_Wajar in zip(BCode, Harga_Wajar):
#                 insert_to_table_3(value_1=Emiten,
#                                   value_2=Harga_Wajar)

#             json_response = {'response': "SUCCESS",
#                              'total emiten': 'Ok',
#                              'total val': 'Ok'
#                              }
#             json_response = jsonify(json_response)
#             return json_response
#         else:
#             json_response = {
#                 'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
#             json_response = jsonify(json_response)
#             return json_response
#         return json_response
#     else:
#         return render_template("input_harga_wajar.html")

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

# @bacafile.route('/test-input-txt', methods=['GET', 'POST'])
# def test_input_txt():
#     if request.method == 'POST':
#         lapet = request.form['inputEmiten']
#         bakpao = request.form['input_PER']
#         sampai = request.form['input_PBV']

#         print(lapet)
#         json_response = {'response': bakpao,
#                              'total emiten': lapet,
#                              'date_inputed': sampai
#                              }
#         json_response = jsonify(json_response)
#         return json_response
#     else:
#         return render_template("test_per.html")
    
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
            query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio, harga_closing.Close_Price, harga_wajar.Harga_Wajar, Buy.unix_date, Buy.margin FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell AND Buy.unix_date = Sell.unix_date INNER JOIN harga_closing ON Buy.EmitenBuy = harga_closing.Emiten AND Buy.unix_date = harga_closing.unix_date INNER JOIN harga_wajar ON Buy.EmitenBuy = harga_wajar.Emiten WHERE Buy.unix_date = Sell.unix_date AND Buy.EmitenBuy= ? AND Sell.EmitenSell = ? ORDER BY Buy.unix_date ASC"
            cursor.execute(query, (emiten_input, emiten_input))
            data = cursor.fetchall()
            num_rows = len(data)
            x_values = [row[7] for row in data]
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in x_values]
            buy_values = [row[1] for row in data]
            sell_values = [row[2] for row in data]
            y_values = [row[4] for row in data]
            closing_values = [row[5] for row in data]
            plot_y = [row[8] for row in data]

            title = [row[0] for row in data][0]

            fig, axs = plt.subplots(3, 1, figsize=(12, 8))
            axs[2].plot(dates,buy_values,marker='o')
            axs[2].plot(dates,sell_values,marker='o')
            axs[2].grid(True)
            axs[2].legend_drawn_flag = True
            axs[2].legend(['Buy', 'Sell'], loc=2)
            axs[2].xaxis.set_major_locator(mdates.DayLocator(interval=7))
            axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            axs[1].plot(dates,y_values,marker='o')
            axs[1].plot(dates,plot_y,linestyle='--', color='k')
            # axs[1].set_yticks(np.arange(-5, 6, 1))
            # axs[1].set_ylim(-10,10)
            axs[1].grid(True)
            axs[1].legend_drawn_flag = True
            axs[1].legend(['Ratio'], loc=2)
            axs[1].xaxis.set_major_locator(mdates.DayLocator(interval=7))
            axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            axs[0].plot(dates,closing_values,marker='o')
            axs[0].grid(True)
            axs[0].set_title(title)
            axs[0].legend_drawn_flag = True
            axs[0].legend(['Close Price'], loc=2)
            axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=7))
            axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
           
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

@bacafile.route('/input-hargawajar', methods=['GET', 'POST'])
def input_file_harga_wajar():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_excel(input_file)
        if ('Stock' in df.columns):
            BCode = df['Stock']
            market_cap = df['Market Cap']
            revenue_act = df['Revenue Act']
            revenue_anl = df['Revenue Anl']
            net_profit_act = df['NetProfit Act']
            net_profit_anl = df['NetProfit Anl']
            ebitda_act = df['EBITDA Act']
            ebitda_anl = df['EBITDA Anl']
            per_act = df['PER Act']
            per_anl = df['PER Anl']
            eps_act = df['EPS Act']
            eps_anl = df['EPS Anl']
            pbv_act = df['PBV Act']
            pbv_anl = df['PBV Anl']
            roa_act = df['ROA Act']
            roa_anl = df['ROA Anl']
            roe_act = df['ROE Act']
            roe_anl = df['ROE Anl']
            evperebitda_act = df['EVEBITDA Act']
            evperebitda_anl = df['EVEBITDA Anl']
            debperequity_act = df['DebtEquity Act']
            create_table_5()
            for Emiten, Market_Cap, Revenue_Act, Revenue_Anl, NetProfit_Act, NetProfit_Anl, EBITDA_Act, EBITDA_Anl, PER_Act, PER_Anl, EPS_Act, EPS_Anl, PBV_Act, PBV_Anl, ROA_Act, ROA_Anl, ROE_Act, ROE_Anl, EVEBITDA_Act, EVEBITDA_Anl, DebtEquity_Act in zip(BCode, market_cap, revenue_act, revenue_anl, net_profit_act, net_profit_anl, ebitda_act, ebitda_anl, per_act, per_anl, eps_act, eps_anl, pbv_act, pbv_anl, roa_act, roa_anl, roe_act, roe_anl, evperebitda_act, evperebitda_anl, debperequity_act):
                insert_to_table_5(value_1=Emiten,
                                  value_2=Market_Cap,
                                  value_3=Revenue_Act,
                                  value_4=Revenue_Anl,
                                  value_5=NetProfit_Act,
                                  value_6=NetProfit_Anl,
                                  value_7=EBITDA_Act,
                                  value_8=EBITDA_Anl,
                                  value_9=PER_Act,
                                  value_10=PER_Anl,
                                  value_11=EPS_Act,
                                  value_12=EPS_Anl,
                                  value_13=PBV_Act,
                                  value_14=PBV_Anl,
                                  value_15=ROA_Act,
                                  value_16=ROA_Anl,
                                  value_17=ROE_Act,
                                  value_18=ROE_Anl,
                                  value_19=EVEBITDA_Act,
                                  value_20=EVEBITDA_Anl,
                                  value_21=DebtEquity_Act)

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

@bacafile.route('/read-stock-screener', methods=['GET', 'POST'])
def read_screener():
    columns = ['Stock','Close Price','Market Cap','Revenue Anl','NetProfit Anl','PER Anl','PBV Anl','ROE Anl']
    date_input = request.form['inputDate']
    print(date_input)
    if request.method == 'POST':
            connection = sqlite3.connect('instance/database.db')
            cursor = connection.cursor()
            query = r"SELECT stock_screener.Emiten, harga_closing.Close_Price, stock_screener.Market_Cap, stock_screener.Revenue_Anl, stock_screener.NetProfit_Anl, stock_screener.PER_Anl, stock_screener.PBV_Anl, stock_screener.ROE_Anl FROM stock_screener INNER JOIN harga_closing ON stock_screener.Emiten = harga_closing.Emiten AND harga_closing.unix_date = ? ORDER BY stock_screener.Market_Cap DESC"
            cursor.execute(query, (date_input,))
            data = cursor.fetchall()
            num_rows = len(data)
            # print(data)

    return render_template("stock_screener.html", columns=columns, data=data, date_input=date_input, num_rows=num_rows)