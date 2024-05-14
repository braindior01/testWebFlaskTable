# from . import db
# import sqlite3
# from sqlalchemy.sql import func

# # class create_table_1(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     BCode = db.Column(db.VARCHAR(1000))
# #     BVal = db.Column(db.Float)
# #     unix_date = db.Column(db.Date)

# # class create_table_2(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     SCode = db.Column(db.VARCHAR(1000))
# #     SVal = db.Column(db.Float)
# #     unix_date = db.Column(db.Date)

import sqlite3

conn = sqlite3.connect('instance/database.db', check_same_thread=False)

# *********************************************
# langkah awal import library sqlite, kemudian membuat data tmp.db dalam folder data


def create_table_1():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS Buy (id INTEGER PRIMARY KEY AUTOINCREMENT, EmitenBuy char, BuyVal float, unix_date date)""")
    conn.commit()

# *********************************************


def create_table_2():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS Sell (id INTEGER PRIMARY KEY AUTOINCREMENT, EmitenSell char, SellVal float, unix_date date)""")
    conn.commit()

# *********************************************
    
def create_table_3():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS harga_wajar (id INTEGER PRIMARY KEY AUTOINCREMENT, Emiten char, Harga_Wajar float)""")
    conn.commit()

def create_table_4():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS harga_closing (id INTEGER PRIMARY KEY AUTOINCREMENT, Emiten char, Close_Price float, unix_date date)""")
    conn.commit()

def create_table_5():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS stock_screener (id INTEGER PRIMARY KEY AUTOINCREMENT, Emiten char, Market_Cap float, Revenue_Act float, Revenue_Anl float, NetProfit_Act float, NetProfit_Anl float, EBITDA_Act float, EBITDA_Anl float, PER_Act float, PER_Anl float, EPS_Act float, EPS_Anl float, PBV_Act float, PBV_Anl float, ROA_Act float, ROA_Anl float, ROE_Act float, ROE_Anl float, EVEBITDA_Act float, EVEBITDA_Anl float, DebtEquity_Act float)""")
    conn.commit()


# langkah selanjutnya membuat table dalam database untuk dapat di isi oleh data dari API


def insert_to_table_1(value_1, value_2, value_3):
    query = f"INSERT INTO Buy (EmitenBuy,BuyVal,unix_date) VALUES (?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3))
    conn.commit()

# *********************************************


def insert_to_table_2(value_1, value_2, value_3):
    query = f"INSERT INTO Sell (EmitenSell,SellVal, unix_date) VALUES (?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3))
    conn.commit()


def read_table():
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = '2024-02-01' AND Sell.unix_date = '2024-02-01'"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)


def insert_to_table_3(value_1, value_2):
    query = f"INSERT INTO harga_wajar (Emiten,Harga_Wajar) VALUES (?, ?);"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()

def insert_to_table_4(value_1, value_2, value_3):
    query = f"INSERT INTO harga_closing (Emiten,Close_Price, unix_date) VALUES (?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3))
    conn.commit()

def insert_to_table_5(value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9, value_10, value_11, value_12, value_13, value_14, value_15, value_16, value_17, value_18, value_19, value_20, value_21):
    query = f"INSERT INTO stock_screener (Emiten, Market_Cap, Revenue_Act, Revenue_Anl, NetProfit_Act, NetProfit_Anl, EBITDA_Act, EBITDA_Anl, PER_Act, PER_Anl, EPS_Act, EPS_Anl, PBV_Act, PBV_Anl, ROA_Act, ROA_Anl, ROE_Act, ROE_Anl, EVEBITDA_Act, EVEBITDA_Anl, DebtEquity_Act) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9, value_10, value_11, value_12, value_13, value_14, value_15, value_16, value_17, value_18, value_19, value_20, value_21))
    conn.commit()