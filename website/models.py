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

conn = sqlite3.connect('testWebFlaskTable/instance/database.db', check_same_thread=False)

# *********************************************
# langkah awal import library sqlite, kemudian membuat data tmp.db dalam folder data

def create_table_1():
    conn.execute("""CREATE TABLE IF NOT EXISTS Buy (id INTEGER PRIMARY KEY AUTOINCREMENT, EmitenBuy char, BuyVal float, unix_date date)""")
    conn.commit()

# *********************************************

def create_table_2():
    conn.execute("""CREATE TABLE IF NOT EXISTS Sell (id INTEGER PRIMARY KEY AUTOINCREMENT, EmitenSell char, SellVal float, unix_date date)""")
    conn.commit()

# *********************************************
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