import sqlite3
import os
import csv

def join_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Stocks_High JOIN Stocks_Low ON Stocks_High.Symbol = Stocks_Low.Symbol")

    return (cur.fetchall())

#print(join_database("stocks_db.sqlite"))

def calculate_net_price(db_lst):

    net_price_lst = []
    for i in db_lst:
        net_price_lst.append((i[0], round(float(i[1]) - float(i[2]), 2), round(float(i[4]) - float(i[5]), 2)))

    return net_price_lst


def write_csv(net_lst):

    with open('stock_net_prices.csv', 'w') as stock_file:
        write_prices = csv.writer(stock_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["Symbol", "Net High Price", "Net Low Price"])

        for i in net_lst:
            write_prices.writerow([i[0], i[1], i[2]])

write_csv(calculate_net_price(join_database("stocks_db.sqlite")))