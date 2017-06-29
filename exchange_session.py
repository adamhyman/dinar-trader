## Ari Mahpour
## 06/28/2017
## Class for interfaces with different exchanges

#import krakenex
import importlib
krakenex = importlib.import_module("python3-krakenex.krakenex")



from geminiapi.gemini import GeminiSession 

class exchange_session(object):
    ## Defines an exchange API session
    
    def __init__(self, exchange='', path_to_key=''):
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
        
    def get_exchange_type():
        return self.exchange
