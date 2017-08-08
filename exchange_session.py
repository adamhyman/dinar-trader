

import importlib
import logging
import sys
import os
import csv
import socket
import krakenex
import gdax
import http.client
from time import sleep
import datetime
from geminiapi.gemini import GeminiSession

import Bittrex

from liqui import Liqui

# Constants
sleep_time_sec = 15



# Set up logger
# This will log all console outputs to a log file (run.log)
# Note: This is in addition to the CSV output file
#       as it is used for debugging purposes.
logging.basicConfig(filename='run.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def double_quote(word):
    double_q = '"' # double quote
    return double_q + str(word) + double_q
def single_quote(word):
    single_quote = "'" # single quote
    return single_quote + str(word) + single_quote


class currency(object):
    def __init__(self, session, currency, symbol, balance = 0):
        self.session = session
        self.currency = currency
        self.symbol = symbol         #  The symbol used on this exchange
        self.balance = balance
        self.active = True
        self.t1 = 0
        self.t2 = 0

        if (self.currency == 'USD'):
            self.min_increment = '0.01'
        

    def update_balance(self, balance, t1=0, t2=0):
        self.balance = balance
        self.t1 = t1
        self.t2 = t2

    def print_values(self):
        print('Currency: %s.  Symbol: %s.  Balance: %s.  T1: %s.  T2:%s.' % (self.currency, self.symbol, self.balance, self.t1, self.t2))

    def trade(self):
        self.balance = self.balance + 1

    def print_symbol(self):
        return str(self.symbol)

    def get_balance(self):
        return float(self.balance)


        


class book(object):
    def __init__(self, session, exchange, pair, currency, base, symbol):
        self.session = session
        self.exchange = exchange
        self.pair = pair
        self.currency = currency   #  A currency object
        self.base = base           #  A currency object
        self.symbol = symbol       #  The symbol used on this exchange
        self.active = True
        self.t1 = 0
        self.t2 = 0
        self.asks = [[0,0]]
        self.bids = [[0,0]]


    def update_book(self):
	
        if (self.exchange.lower() == "kraken"):

	    # https://api.kraken.com/0/public/Depth?pair=XETHZUSD
            while True:
                try:

                    self.t1 = datetime.datetime.now()
                    result = self.session.query_public('Depth',{'pair': self.symbol, 'count': '10'})['result']
                    self.t2 = datetime.datetime.now()

                except (http.client.HTTPException, socket.timeout) as ex:
                    logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                    logging.info ("Sleeping %s seconds and restarting Loop." % (sleep_time_sec))
                    sleep(sleep_time_sec)
                    continue

                self.asks = []
                self.bids = []

                # print (result[self.symbol]['asks'])
                
                for row in result[self.symbol]['asks']:
                    self.asks.append([row[0],row[1]])
                    
                for row in result[self.symbol]['bids']:
                    self.bids.append([row[0],row[1]])
                break

        elif (self.exchange.lower() == "gemini"):
		
            # https://api.gemini.com/v1/book/ETHBTC
			
            self.t1 = datetime.datetime.now()
            result = self.session.get_current_order_book(self.symbol)
            self.t2 = datetime.datetime.now()

            self.asks = []
            self.bids = []

            for row in result['asks']:
                self.asks.append([row['price'],row['amount']])

            for row in result['bids']:
                self.bids.append([row['price'],row['amount']])



        elif (self.exchange.lower() == "gdax"):
			
            # https://api.gdax.com/products/ETH-USD/book?level=2
            self.t1 = datetime.datetime.now()
            result = self.session.get_product_order_book(self.symbol, 2)
            self.t2 = datetime.datetime.now()
			
            self.bids = []
            self.asks = []
	
            for row in result['bids']:
                self.bids.append([row[0],row[1]])
            for row in result['asks']:
                self.asks.append([row[0],row[1]])

				
        elif (self.exchange.lower() == "bittrex"):
            #  https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-ETH&type=both&depth=4
			
            self.bids = []
            self.asks = []
			
            self.t1 = datetime.datetime.now()
            result = self.session.get_orderbook(self.symbol, "both", 10)['result']
            self.t2 = datetime.datetime.now()
			

            i = 0
            for row in result['buy']:
                self.bids.append([row['Rate'],row['Quantity']])
                i = i + 1
                if i > 20:
                    break
            i = 0
            for row in result['sell']:
                self.asks.append([row['Rate'],row['Quantity']])
                i = i + 1
                if i > 20:
                    break


        elif (self.exchange.lower() == "liqui"):
			
            self.t1 = datetime.datetime.now()
            result = self.session.depth(self.symbol)
            self.t2 = datetime.datetime.now()
			
            self.asks = result[self.symbol]['asks']
            self.bids = result[self.symbol]['bids']

        self.asks.sort(key=lambda x: x[0])
        self.bids.sort(key=lambda x: x[0], reverse=True)


    def trade(self, trans, qty):

        
        if (self.exchange.lower() == "kraken"):

            # TO DO: Handle the exception in exchange_session.py
            while True:
                try:
                    if (trans.lower() == 'buy'):
                        mydict = {'pair': self.symbol, 'type': 'buy', 'ordertype': 'market', 'price': '100000', 'volume': qty}


                        # Temporarily commented out the trading function
                        logging.info (self.session.query_private('AddOrder', mydict))
                    if (trans.lower() == 'sell'):
                        mydict = {'pair': self.symbol, 'type': 'sell', 'ordertype': 'market', 'price': self.base.min_increment, 'volume': qty}
                        
                        # Temporarily commented out the trading function
                        logging.info (self.session.query_private('AddOrder', mydict))
                    break
                except (http.client.HTTPException, socket.timeout) as ex:
                    logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                    logging.info ("Sleeping %s seconds and restarting Loop." % (sleep_time_sec))
                    sleep(sleep_time_sec)
                    break

        if (self.exchange.lower() == "gemini"):
            if (trans.lower() == 'buy'):
                logging.info (self.session.new_order(self.symbol, str(qty), "100000","buy", "immediate-or-cancel"))

            if (trans.lower() == 'sell'):
                logging.info (self.session.new_order(self.symbol, str(qty), self.base.min_increment,"sell", "immediate-or-cancel"))


        if (self.exchange.lower() == "gdax"):
            if (trans.lower() == 'buy'):
                logging.info (self.session.buy(type='market', size=str(qty), product_id=self.symbol))

            if (trans.lower() == 'sell'):
                logging.info (self.session.sell(type='market', size=str(qty), product_id=self.symbol))

        if (self.exchange.lower() == "bittrex"):
            if (trans.lower() == 'buy'):
                logging.info (self.session.buy_limit(self.symbol, qty, 100000))

            if (trans.lower() == 'sell'):
                logging.info (self.session.sell_limit(self.symbol, qty, 0.00001))

        if (self.exchange.lower() == "liqui"):
            if (trans.lower() == 'buy'):
                logging.info (self.session.buy('eth_btc', 10000, qty))

            if (trans.lower() == 'sell'):
                logging.info (self.session.sell('eth_btc', 0.00001, qty))


        if (trans.lower() == 'buy'):
            self.currency.update_balance(float(self.currency.balance) + float(qty))                         #  Buying increases currency by the qty puchased
            self.base.update_balance(float(self.base.balance) - float(self.bids[0][0]) * float(qty))        #  Buying decreases base by the amount paid


        if (trans.lower() == 'sell'):
            self.currency.update_balance(float(self.currency.balance) - float(qty))                         #  Selling decreases currency by the qty sold
            self.base.update_balance(float(self.base.balance) + float(self.bids[0][0]) * float(qty))        #  Selling increases base by the amount received


    def ask(self):
            return float(self.asks[0][0])

    def bid(self):
            return float(self.bids[0][0])

                
##        print (self.base.min_increment)

    def print_values(self):
        print ('%s - %s' %(self.exchange, self.pair))
        for row in self.asks:
            print ('Ask  %s.  Volume %s.' %(row[0], row[1]))
        print ('')
		
        for row in self.bids:
            print ('Bid  %s.  Volume %s.' %(row[0], row[1]))
        print ('')


class exchange_session(object):
    ## Defines an exchange API session    
    def __init__(self, exchange='', path_to_key='', debug=True):
        # Self types
        self.exchange = exchange
        self.debug = debug   # Allow debugging print messages

        self.currencies = []
        self.books = []
        # Create a Kraken exchange session object
        if (exchange.lower() == "kraken"):
            self.session = krakenex.API()
            self.session.load_key(path_to_key)
            logging.info ("Kraken session configured.")

            self.currencies.append(currency(self.session, 'USD', 'ZUSD'))
            self.currencies.append(currency(self.session, 'USDT', 'USDT'))
            self.currencies.append(currency(self.session, 'BTC', 'XXBT'))
            self.currencies.append(currency(self.session, 'ETH', 'XETH'))
            self.currencies.append(currency(self.session, 'XRP', 'XXRP'))
            self.currencies.append(currency(self.session, 'LTC', 'XLTC'))
            self.currencies.append(currency(self.session, 'DASH', 'DASH'))
            self.print_balances('Created %s Currencies:' %(self.exchange.title()))

            c1 = [x for x in self.currencies if x.currency == 'BTC'][0]
            c2 = [x for x in self.currencies if x.currency == 'USD'][0]


##            self.books.append(book(self.session, self.exchange, 'BTCUSD',  self.currency_from_symbol('BTC'),  self.currency_from_symbol('USD'), 'XXBTZUSD'))
            self.books.append(book(self.session, self.exchange, 'ETHUSD',  self.currency_from_symbol('ETH'),  self.currency_from_symbol('USD'), 'XETHZUSD'))
##            self.books.append(book(self.session, self.exchange, 'XRPUSD',  self.currency_from_symbol('XRP'),  self.currency_from_symbol('USD'), 'XXRPZUSD'))
##            self.books.append(book(self.session, self.exchange, 'LTCUSD',  self.currency_from_symbol('LTC'),  self.currency_from_symbol('USD'), 'XLTCZUSD'))
##            self.books.append(book(self.session, self.exchange, 'DASHUSD', self.currency_from_symbol('DASH'), self.currency_from_symbol('BTC'), 'DASHXBT'))

##"XETHZUSD":{"altname":"ETHUSD",
##            "aclass_base":"currency",
##            "base":"XETH",
##            "aclass_quote":"currency",
##            "quote":"ZUSD",
##            "lot":"unit","pair_decimals":5,"lot_decimals":8,
##            "lot_multiplier":1,
##            "leverage_buy":[2,3,4,5],
##            "leverage_sell":[2,3,4,5],
##            "fees":[[0,0.26],[50000,0.24],[100000,0.22],[250000,0.2],[500000,0.18],[1000000,0.16],[2500000,0.14],[5000000,0.12],[10000000,0.1]],
##            "fees_maker":[[0,0.16],[50000,0.14],[100000,0.12],[250000,0.1],[500000,0.08],[1000000,0.06],[2500000,0.04],[5000000,0.02],[10000000,0]],
##            "fee_volume_currency":"ZUSD",
##            "margin_call":80,
##            "margin_stop":40}



        # Create a Gemini exchange session object
        elif (exchange.lower() == "gemini"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                self.session = GeminiSession(key, secret, False)
            logging.info ("Gemini session configured.")

            self.currencies.append(currency(self.session, 'USD', 'USD'))
            self.currencies.append(currency(self.session, 'BTC', 'BTC'))
            self.currencies.append(currency(self.session, 'ETH', 'ETH'))

            self.print_balances('Created Gemini Currencies:')
            
##            self.books.append(book(self.session, self.exchange, 'BTCUSD', self.currency_from_symbol('BTC'), self.currency_from_symbol('USD'), 'BTCUSD'))
            self.books.append(book(self.session, self.exchange, 'ETHUSD', self.currency_from_symbol('ETH'), self.currency_from_symbol('USD'), 'ETHUSD'))			
            self.books.append(book(self.session, self.exchange, 'ETHBTC', self.currency_from_symbol('ETH'), self.currency_from_symbol('BTC'), 'ETHBTC'))
            
        # Create a GDAX exchange session object


        elif (exchange.lower() == "gdax"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                passphrase = f.readline().strip()
                self.session = gdax.AuthenticatedClient(key, secret, passphrase)
            logging.info ("GDAX session configured.")

            self.currencies.append(currency(self.session, 'USD', 'USD'))
            self.currencies.append(currency(self.session, 'BTC', 'BTC'))
            self.currencies.append(currency(self.session, 'ETH', 'ETH'))
            self.currencies.append(currency(self.session, 'LTC', 'LTC'))
            self.print_balances('Created %s Currencies:' %(self.exchange.title()))
			
            self.books.append(book(self.session, self.exchange, 'ETHUSD', self.currency_from_symbol('ETH'), self.currency_from_symbol('USD'), 'ETH-USD'))
##            self.books.append(book(self.session, self.exchange, 'BTCUSD', self.currency_from_symbol('BTC'), self.currency_from_symbol('USD'), 'BTC-USD'))
##            self.books.append(book(self.session, self.exchange, 'LTCUSD', self.currency_from_symbol('BTC'), self.currency_from_symbol('USD'), 'LTC-USD'))
##            self.books.append(book(self.session, self.exchange, 'LTCBTC', self.currency_from_symbol('LTC'), self.currency_from_symbol('BTC'), 'LTC-BTC'))

        elif (exchange.lower() == "bittrex"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                self.session = Bittrex.Bittrex(key, secret)
            logging.info ("Bittrex session configured.")

            self.currencies.append(currency(self.session, 'USDT', 'USDT'))
            self.currencies.append(currency(self.session, 'BTC', 'BTC'))
            self.currencies.append(currency(self.session, 'ETH', 'ETH'))
##            self.currencies.append(currency(self.session, 'XRP', 'XRP'))
##            self.currencies.append(currency(self.session, 'LTC', 'LTC'))
##            self.currencies.append(currency(self.session, 'DASH', 'DASH'))
            self.print_balances('Created %s Currencies:' %(self.exchange.title()))
			
            self.books.append(book(self.session, self.exchange, 'ETHBTC', self.currency_from_symbol('ETH'), self.currency_from_symbol('BTC'), 'BTC-ETH'))
##            self.books.append(book(self.session, self.exchange, 'LTCBTC', self.currency_from_symbol('LTC'), self.currency_from_symbol('BTC'), 'BTC-LTC'))
##            self.books.append(book(self.session, self.exchange, 'XRPBTC', self.currency_from_symbol('XRP'), self.currency_from_symbol('BTC'), 'BTC-XRP'))
##            self.books.append(book(self.session, self.exchange, 'DASHBTC', self.currency_from_symbol('DASH'), self.currency_from_symbol('BTC'), 'BTC-DASH'))
##            self.books.append(book(self.session, self.exchange, 'DASHETH', self.currency_from_symbol('DASH'), self.currency_from_symbol('ETH'), 'ETH-DASH'))
            
			
            
        elif (exchange.lower() == "liqui"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                self.session = Liqui(key, secret)
            logging.info ("Liqui session configured.")

            self.currencies.append(currency(self.session, 'USDT', 'USDT'))
            self.currencies.append(currency(self.session, 'BTC', 'BTC'))
            self.currencies.append(currency(self.session, 'ETH', 'ETH'))
##            self.currencies.append(currency(self.session, 'LTC', 'LTC'))
##            self.currencies.append(currency(self.session, 'DASH', 'DASH'))
			
            self.print_balances('Created %s Currencies:' %(self.exchange.title()))
			
            self.books.append(book(self.session, self.exchange, 'ETHBTC', self.currency_from_symbol('ETH'), self.currency_from_symbol('BTC'), 'eth_btc'))
##            self.books.append(book(self.session, self.exchange, 'DASHBTC', self.currency_from_symbol('DASH'), self.currency_from_symbol('BTC'), 'dash_btc'))
			
			
        elif (exchange == ""):
            raise ValueError("Missing exchange name.")

	
    def update_balances(self):
        ## Returns the balance of account in a dict format
        if (self.exchange.lower() == "kraken"):
            ## Note: Kraken has a known issue of timing out every so often
            ##       so this is addressed by catching a HTTP 504 error and
            ##       retrying the query
            while True:
                try:

                    t1 = datetime.datetime.now()
                    balances = self.session.query_private('Balance')['result']
                    t2 = datetime.datetime.now()

                except (http.client.HTTPException, socket.timeout) as ex:
                    logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                    logging.info ("Sleeping %s seconds and restarting Loop." % (sleep_time_sec))
                    sleep(sleep_time_sec)
                    continue

                for b in balances:
                    for c in self.currencies:
                        if b.lower() == c.symbol.lower():
                            c.update_balance(balances[b], t1, t2)
                
                #self.print_balances('Updated %s Currencies:' %(self.exchange.title()))
                break

        elif (self.exchange.lower() == "gemini"):
            
            t1 = datetime.datetime.now()
            balances = self.session.get_balances()
            t2 = datetime.datetime.now()

            for b in balances:
                for c in self.currencies:
                    if b['currency'].lower() == c.symbol.lower():
                        c.update_balance(b['available'], t1, t2)
			
        elif (self.exchange.lower() == "gdax"):
            t1 = datetime.datetime.now()
            balances = self.session.get_accounts()
            t2 = datetime.datetime.now()

            for b in balances:
                for c in self.currencies:
                    if b['currency'].lower() == c.symbol.lower():
                        c.update_balance(b['available'], t1, t2)
			
        elif (self.exchange.lower() == "bittrex"):
            t1 = datetime.datetime.now()
            balance = self.session.get_balances()['result']
            t2 = datetime.datetime.now()
			
            for b in balance:
                for c in self.currencies:
                    if b['Currency'].lower() == c.symbol.lower():
                        c.update_balance(b['Balance'], t1, t2)

        elif (self.exchange.lower() == "liqui"):
            t1 = datetime.datetime.now()
            balances = self.session.balances()
            t2 = datetime.datetime.now()

            for b in balances:
                for c in self.currencies:
                    if b.lower() == c.symbol.lower():
                        c.update_balance(balances[b], t1, t2)



    def currency_from_symbol(self, my_symbol):
        return [x for x in self.currencies if x.currency == my_symbol][0]
    
    def print_balances(self, message=None):
        if message == None:
            message = self.exchange.lower() + ' balances:'
        print (message)
        for c in self.currencies:
            c.print_values()
        print ('')

		
    def update_books(self):
        for b in self.books:
            b.update_book()
        print ('')
		
    def print_books(self, message=None):
        if message == None:
            message = self.exchange.lower() + ' books:'
        print (message)
        for b in self.books:
            b.print_values()
        print ('')

			
    def get_trade_info(self, ticker_pair="ETHUSD"):
        ## Returns recent trading activity for a symbol
        ## Valid ticker pairs: 
        ## 1. "ETHUSD"
        if (self.exchange.lower() == "kraken"):
            ## Note: Kraken has a known issue of timing out every so often
            ##       so this is addressed by catching a HTTP 504 error and
            ##       retrying the query
            while True:
                try:
                    if (ticker_pair == "ETHUSD"):
                        k_ticker = self.session.query_public('Ticker',{'pair': self.get_pair_name("ETHUSD")})['result']
                        return {'ask':float(k_ticker[self.get_pair_name("ETHUSD")]["a"][0]), 'bid':float(k_ticker[self.get_pair_name("ETHUSD")]["b"][0])}
                except (http.client.HTTPException, socket.timeout) as ex:
                    logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                    logging.info ("Sleeping %s seconds and restarting Loop." % (sleep_time_sec))
                    sleep(sleep_time_sec)
                    continue
        elif (self.exchange.lower() == "gemini"):
            if (ticker_pair == "ETHUSD"):
                gbalance = self.session.get_ticker(self.get_pair_name("ETHUSD"))
                return {'ask':float(gbalance["ask"]), 'bid':float(gbalance["bid"])}
        
        elif (self.exchange.lower() == "gdax"):
            if (ticker_pair == "ETHUSD"):
                gdax_balance = self.session.get_product_ticker(self.get_pair_name("ETHUSD"))
                return {'ask':float(gdax_balance['ask']), 'bid':float(gdax_balance['bid'])}

		
