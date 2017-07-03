## Ari Mahpour
## 06/28/2017
## Class for interfaces with different exchanges

import importlib
krakenex = importlib.import_module("python3-krakenex.krakenex")
gdax = importlib.import_module("gdax-python")
from geminiapi.gemini import GeminiSession

class exchange_session(object):
    ## Defines an exchange API session
    
    
    def __init__(self, exchange='', path_to_key=''):
        # Self types
        self.exchange = exchange
        self.debug = True   # Allow debugging print messages
        
        # Create a Kraken exchange session object
        if (exchange.lower() == "kraken"):
            self.session = krakenex.API()
            self.session.load_key(path_to_key)
            print ("Kraken session configured.")
        elif (exchange.lower() == "gemini"):
            with open(path_to_key, 'r') as f:
                key = f.readline().strip()
                secret = f.readline().strip()
                self.session = GeminiSession(key, secret, False)
            print ("Gemini session configured.")
        elif (exchange == ""):
            raise ValueError("Missing exchange name.")
            
    def get_pair_name(self, trade_name):
        if (trade_name == "ETHUSD"):
            if (self.exchange.lower() == "kraken"):
                return "XETHZUSD"
            if (self.exchange.lower() == "gemini"):
                return "ethusd"

    # Returns the balance of account in a dict format
    def get_balances(self):
        if (self.exchange.lower() == "kraken"):
            balance = self.session.query_private('Balance')['result']
            if self.debug:
                print ("Kraken USD: %s" % balance["ZUSD"])
                print ("Kraken ETH: %s" % balance["XETH"])
                print ("Kraken BTC: %s" % balance["XXBT"])
            return {'USD':float(balance["ZUSD"]), 'ETH':float(balance["XETH"]), 'BTC':float(balance["XXBT"])}
        elif (self.exchange.lower() == "gemini"):
            balance = self.session.get_balances()
            if self.debug:
                print ("Gemini USD: %s" % balance[1]["available"])
                print ("Gemini ETH: %s" % balance[2]["available"])
                print ("Gemini BTC: %s" % balance[0]["available"])
            return {'USD':float(balance[1]["available"]), 'ETH':float(balance[2]["available"]), 'BTC':float(balance[0]["available"])}
            
    def get_trade_info(self, ticker_pair="ETHUSD"):
        ## Returns recent trading activity for a symbol
        ## Valid ticker pairs: 
        ## 1. "ETHUSD"
        if (self.exchange.lower() == "kraken"):
            if (ticker_pair == "ETHUSD"):
                k_ticker = self.session.query_public('Ticker',{'pair': self.get_pair_name("ETHUSD")})['result']
                return {'ask':float(k_ticker[self.get_pair_name("ETHUSD")]["a"][0]), 'bid':float(k_ticker[self.get_pair_name("ETHUSD")]["b"][0])}
        elif (self.exchange.lower() == "gemini"):
            if (ticker_pair == "ETHUSD"):
                gbalance = self.session.get_ticker(self.get_pair_name("ETHUSD"))
                return {'ask':float(gbalance["ask"]), 'bid':float(gbalance["bid"])}
            
    def get_balance_usd(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["ZUSD"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[1]["available"])
            
    def get_balance_eth(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["XETH"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[2]["available"])
            
    def get_balance_btc(self):
        if (self.exchange.lower() == "kraken"):
            return float(self.session.query_private('Balance')['result']["XXBT"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[0]["available"])

    def get_exchange_type(self):
        return self.exchange
