import json
import unittest
import os
import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup 
import sqlite3

#
# Your name: Shahbab Ahmed    
# Who you worked with: Amirul Miah
#


# Make sure you create an API key at alphavantage.co/support/#api-key
# Assign that to the variable API_KEY
API_KEY = "GC1SJ3IS4Y5SV6PJ"

# This contains the NASDAQ-100 (top 103 stocks from the NASDAQ sector, does not include financial stocks) index as a list
nasdaq_100 = ["MSFT", "AAPL", "AMZN", "GOOG", "GOOGL", "FB", "INTC", "PEP", "CSCO", "NFLX", "CMCSA", "NVDA", "ADBE", "COST", "AMGN", "PYPL", "TSLA", "AVGO", "CHTR", "TXN", "GILD", "QCOM", "SBUX", "MDLZ", "TMUS", 
"INTU", "VRTX", "FISV", "ADP", "AMD", "BKNG", "BIIB", "ISRG", "REGN", "MU", "CSX", "ATVI", "AMAT", "ILMN", "WBA", "JD", "LRCX", "EXC", "ADI", "ADSK", "XEL", "KHC", "MNST", "ROST", "EA", "CTSH", "EBAY", "BIDU", "MELI", "MAR",
 "ORLY", "NXPI", "WLTW", "KLAC", "LULU", "NTES", "VRSK", "WDAY", "SIRI", "VRSN", "PAYX", "CSGP", "PCAR", "IDXX", "SNPS", "ALXN", "CERN", "XLNX", "ANSS", "CDNS", "ASML", "SGEN", "CTAS", "SPLK", "FAST", "INCY", "MCHP", 
 "DLTR", "CTXS", "CPRT", "SWKS", "CHKP", "BMRN", "CDW", "ALGN", "MXIM", "TTWO", "WDC", "TCOM", "ULTA", "NTAP", "FOXA", "EXPE", "UAL", "LBTYK", "FOX", "AAL", "LBTYA"]

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn't exist, it returns an empty dictionary.
    """
    
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    path_to_file = os.path.join(os.path.dirname(__file__), CACHE_FNAME)
    with open(path_to_file, 'w') as f:
        f.write(json.dumps(CACHE_DICT))

# Creates the link for requesting the data by passing in the symbol of the stock
def create_request_url(symbol):

    #if symbol in nasdaq_100:
    return "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol="+ symbol + "&" + "apikey=" + API_KEY
    #else:
    #    print("This stock is not part of the NASQAD-100 Index. Please try a different symbol")
    #    return None

def get_weekly_price_data(symbols, CACHE_FNAME):

    new_dict = read_cache(CACHE_FNAME)
    #print(new_dict)
    for symbol in symbols:
        
        if symbol not in new_dict.keys():
            request_url = create_request_url(symbol)


            print("Fetching data for " + symbol)
            try:
                response = urlopen(request_url)
                data = json.load(response)
                if "Weekly Time Series" in data.keys():
                    latest_date = list(data["Weekly Time Series"].keys())[0]
                    oldest_high_price = ""
                    oldest_low_price = ""

                    for i in data["Weekly Time Series"].keys():
                        if i.split("-")[0] == "2020":
                            oldest_high_price = data["Weekly Time Series"][i]["2. high"]
                            oldest_low_price = data["Weekly Time Series"][i]["3. low"]

                    

                    new_dict[symbol] = (float(data["Weekly Time Series"][latest_date]["2. high"]), float(oldest_high_price), float(data["Weekly Time Series"][latest_date]["3. low"]), float(oldest_low_price))
                    write_cache(CACHE_FNAME, new_dict)
            except:
                print("None")
        else:
            print("The data for " + symbol + " has already been stored")

        '''for i in data["Weekly Time Series"].keys():
            if i.split("-")[0] == "2020":
                
                if 
                new_dict[symbol] = data["Weekly Time Series"][i]
                #print(new_dict)'''

        
                
    
            #else:
            #    print(data["Error"])
    print("Finished loading data for " + str(len(new_dict)) + " stocks")
    return new_dict


#conn = sqlite3.connect('/Users/shahbaba/Desktop/SI206/FinalProjectStock/stocks_database.sqlite')
#cur = conn.cursor()

#cur.execute('''
#CREATE TABLE IF NOT EXISTS Stocks (Symbol TEXT, LatestWeekPrice TEXT, OldestWeekPrice TEXT)''')


def create_high_database(stock_dict, db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Stocks_High (Symbol TEXT, LatestWeekPrice TEXT, OldestWeekPrice TEXT)''')

    for i in stock_dict:
        
        cur.execute('SELECT Symbol FROM Stocks_High')

        rows = cur.fetchall()

        #print(rows[])

        row_lst = []
        
        for i in rows:
            if i not in row_lst:
                row_lst.append(i)

        print(row_lst)

        if i not in row_lst:
            cur.execute('''INSERT INTO Stocks_High (Symbol, LatestWeekPrice, OldestWeekPrice)
                    VALUES ( ?, ?, ?)''', (i, stock_dict[i][0], stock_dict[i][1]) ) 
            conn.commit()
    
    cur.close()

def create_low_database(stock_dict, db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Stocks_Low (Symbol TEXT, LatestWeekPrice TEXT, OldestWeekPrice TEXT)''')

    for i in stock_dict:
        
        cur.execute('SELECT Symbol FROM Stocks_Low')

        rows = cur.fetchall()

        #print(rows[])

        row_lst = []
        
        for i in rows:
            if i not in row_lst:
                row_lst.append(i)

        print(row_lst)

        if i not in row_lst:
            cur.execute('''INSERT INTO Stocks_Low (Symbol, LatestWeekPrice, OldestWeekPrice)
                    VALUES ( ?, ?, ?)''', (i, stock_dict[i][2], stock_dict[i][3]) ) 
            conn.commit()
    
    cur.close()

def create_symbols():
    base_url = 'https://robinhood.com/collections/100-most-popular'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    symbols = []

    for i in soup.find_all("tr", {"class":"_3-Fg9lFlzey28mCJClXXxZ"}):
        stuff = i.find_all("td", {"class":""})
        symbol = stuff[0].a.div.span.text
        symbols.append(symbol)
    
    return symbols

#sam = {'AACG': ('0.8500', '1.4892'), 'AAL': ('11.3500', '29.2950'), 'AAME': ('1.9500', '2.0989'), 'AAOI': ('8.6520', '12.5300'), 'AAON': ('47.5000', '50.4200'), 'AKTX': ('1.6300', '1.8000'), 'ALAC': ('10.4700', '10.3500'), 'ALACR': ('0.1800', '0.2200'), 'ALACU': ('10.4900', '10.6500'), 'ALACW': ('0.0300', '0.0800'), 'ALBO': ('19.1000', '26.7100')}


'''def create_symbols():
    text_file = open("nasdaqlisted.txt", "r")
    lines = text_file.readlines()

    text_file.close()
    symbols = []
    for i in lines:
        i = i.split("|")[0]

        symbols.append(i)
    symbols.pop(-1)
    return symbols'''

#print(create_symbols())
    
#print(create_symbols())


#for i in range(10):

print(get_weekly_price_data(create_symbols(), "stock_data.json"))

#print(read_cache("stock_data.json"))

#print(create_request_url("CHKP"))
#print(create_request_url("CHK"))

#get_data_with_caching(create_symbols(), "stock_data")


