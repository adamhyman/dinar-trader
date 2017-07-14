## Ari Mahpour
## 06/28/2017
## Class for interfaces with different exchanges

import importlib
import logging
import socket
import http.client
import krakenex
from time import sleep
from geminiapi.gemini import GeminiSession

# Constants
sleep_time_sec = 15
root = logging.getLogger()

class exchange_session(object):
    ## Defines an exchange API session    
    def __init__(self, exchange='', path_to_key='', debug=True):
        # Self types
        self.exchange = exchange
        self.debug = debug   # Allow debugging print messages
        
        # Create a Kraken exchange session object
        if (exchange.lower() == "kraken"):
            self.session = krakenex.API()
            self.session.load_key(path_to_key)
            logging.info ("Kraken session configured.")
        # Create a Gemini exchange session object
        elif (exchange.lower() == "gemini"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                self.session = GeminiSession(key, secret, False)
            logging.info ("Gemini session configured.")
        # Create a GDAX exchange session object
        elif (exchange.lower() == "gdax"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                passphrase = f.readline().strip()
                print ('Key ' + key)
            self.session = gdax.AuthenticatedClient(key, secret, passphrase)
            logging.info ("GDAX session configured.")
        elif (exchange == ""):
            raise ValueError("Missing exchange name.")
            
    def get_pair_name(self, trade_name):
        ## Returns the proper trade name per exchange
        if (trade_name == "ETHUSD"):
            if (self.exchange.lower() == "kraken"):
                return "XETHZUSD"
            if (self.exchange.lower() == "gemini"):
                return "ethusd"
            if (self.exchange.lower() == "gdax"):
                return "ETH-USD"

    def get_balances(self):
        ## Returns the balance of account in a dict format
        if (self.exchange.lower() == "kraken"):
            ## Note: Kraken has a known issue of timing out every so often
            ##       so this is addressed by catching a HTTP 504 error and
            ##       retrying the query
            while True:
                try:
                    balance = self.session.query_private('Balance')['result']
                except (http.client.HTTPException, socket.timeout) as ex:
                    logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                    logging.info ("Sleeping %s seconds and restarting Loop." % (sleep_time_sec))
                    sleep(sleep_time_sec)
                    continue
                if self.debug:
                    logging.info ("Kraken USD: %s" % balance["ZUSD"])
                    logging.info ("Kraken ETH: %s" % balance["XETH"])
                    logging.info ("Kraken BTC: %s" % balance["XXBT"])
                return {'USD':float(balance["ZUSD"]), 'ETH':float(balance["XETH"]), 'BTC':float(balance["XXBT"])}
        elif (self.exchange.lower() == "gemini"):
            balance = self.session.get_balances()
            if self.debug:
                logging.info ("Gemini USD: %s" % balance[1]["available"])
                logging.info ("Gemini ETH: %s" % balance[2]["available"])
                logging.info ("Gemini BTC: %s" % balance[0]["available"])
            return {'USD':float(balance[1]["available"]), 'ETH':float(balance[2]["available"]), 'BTC':float(balance[0]["available"])}
        elif (self.exchange.lower() == "gdax"):
            balance = self.get_accounts()
            self.USD = balance[0]['balance']
            self.LTC = balance[1]['balance']
            self.ETH = balance[2]['balance']
            self.BTC = balance[3]['balance']
            if self.debug:
                logging.info ("GDAX USD:  %s" % balance[0]['balance'])
                logging.info ("GDAX ETH:  %s" % balance[2]['balance'])
                logging.info ("GDAX BTC:  %s" % balance[3]['balance'])
            return {'USD':float(balance[0]['balance']), 'ETH':float(balance[2]['balance']), 'BTC':float(balance[3]['balance'])}
            

            
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
        
            
    def get_balance_usd(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["ZUSD"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[1]["available"])
        elif (self.exchange.lower() == "gdax"):
            return float(self.session.get_accounts()[0]['balance'])
            
    def get_balance_eth(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["XETH"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[2]["available"])
        elif (self.exchange.lower() == "gdax"):
            return float(self.session.get_accounts()[2]['balance'])
            
    def get_balance_btc(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["XXBT"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[0]["available"])
        elif (self.exchange.lower() == "gdax"):
            return float(self.session.get_accounts()[3]['balance'])

    def get_exchange_type(self):
        return self.exchange
