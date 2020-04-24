from bs4 import BeautifulSoup 
import requests
import sqlite3
import os

used_stocks =[]
stocks = {}

def setUp_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Popular_Stocks (Symbol TEXT, Name TEXT, Price TEXT, Performance TEXT, Rating TEXT)''')

    cur.execute('SELECT Symbol FROM Popular_Stocks')
    rows = cur.fetchall()
    for i in rows:
        used_stocks.append(i[0])

    #print(len(used_stocks))

    count = 0
    for i in stocks:
        if i not in used_stocks:
            cur.execute('''INSERT INTO Popular_Stocks (Symbol, Name, Price, Performance, Rating)
            VALUES ( ?, ?, ?, ?, ? )''', (stocks[i][0], stocks[i][1], stocks[i][2], stocks[i][3], stocks[i][4]) )
            conn.commit()
            count += 1
        
        if count == 20:
            print('Finished loading data for 20 new stocks')
            break
    
    cur.close()


def robinhood_scraper(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    for i in soup.find_all("tr", {"class":"_3-Fg9lFlzey28mCJClXXxZ"}):
        name = i.div.div.div.text
        stuff = i.find_all("td", {"class":""})
        symbol = stuff[0].a.div.span.text
        price = stuff[1].a.div.text            
        sign = ""
        deep = str(stuff[2].svg)
        triangle = deep.split('"')
        if triangle[1] != '_3fIbQm1PGrsgP3ps-22twJ _2W5gCho3Ijf6U_qtTT_A4Y':
            sign = "-"
        else:
            sign = "+"
        todays_performance = sign + stuff[2].a.div.text
        ratings = stuff[-1].a.div.text

        stocks[symbol] = ((symbol, name, price, todays_performance, ratings))


def main():
    robinhood_scraper('https://robinhood.com/collections/100-most-popular')
    setUp_db('stocksDB.sqlite')

if __name__ == "__main__":
    main()