## Ari Mahpour
## 06/28/2017
## Class for interfaces with different exchanges

import importlib
krakenex = importlib.import_module("python3-krakenex.krakenex")
from geminiapi.gemini import GeminiSession 

class exchange_session(object):
    ## Defines an exchange API session
    
    def __init__(self, exchange='', path_to_key=''):
        # Self types
        self.exchange = exchange
        
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
            return float(self.session.query_private('Balance')['result']["GBTC"])
        elif (self.exchange.lower() == "gemini"):
            return float(self.session.get_balances()[0]["available"])

    def get_exchange_type(self):
        return self.exchange