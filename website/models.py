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
        """CREATE TABLE IF NOT EXISTS join_balance (id INTEGER PRIMARY KEY AUTOINCREMENT, Emiten char, Buy_Val float, Sell_Val float, Balance float, unix_date date)""")
    conn.commit()


# langkah selanjutnya membuat table dalam database untuk dapat di isi oleh data dari API


def insert_to_table_1(value_1, value_2, value_3):
    query = f"INSERT INTO Buy (EmitenBuy,BuyVal,unix_date) VALUES (?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3))
    conn.commit()

# *********************************************


def insert_to_table_2(value_1, value_2, value_3):
    query = f"INSERT INTO Sell (EmitenSell,SellVal,unix_date) VALUES (?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3))
    conn.commit()


def read_table():
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    query = r"SELECT Buy.EmitenBuy, Buy.BuyVal, Sell.SellVal, Buy.BuyVal - Sell.SellVal AS Balance, ROUND(Buy.BuyVal / Sell.SellVal,2) AS Ratio FROM Buy INNER JOIN Sell ON Buy.EmitenBuy = Sell.EmitenSell WHERE Buy.unix_date = '2024-02-01' AND Sell.unix_date = '2024-02-01'"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)


def insert_to_table_3(value_1, value_2, value_3, value_4, value_5):
    query = f"INSERT INTO join_balance (Emiten,Buy_Val,Sell_Val,Balance,unix_date) VALUES (?, ?, ?, ?, ?);"
    cursors = conn.execute(query, (value_1, value_2, value_3, value_4, value_5))
    conn.commit()