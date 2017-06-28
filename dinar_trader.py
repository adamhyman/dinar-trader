import sys
import os.path

print (os.path.dirname(__file__) + '\..\kraken.key')



"""Python module for the Gemini API.
https://docs.gemini.com
@author Maneet Khaira
@email msk2226@columbia.edu
"""

import requests
import time
import base64
import hashlib
import json
import hmac

#print("Sleeping")
#time.sleep(1200)
#print("Waking Up")

class GeminiSession:
    """Defines a Gemini API session.
    A session uses one Gemini API key. An account can have multiple sessions.
    """

    def __init__(self, api_key, api_secret, sandbox=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox

        if sandbox is False:
            self.api_url = 'https://api.gemini.com/v1/'
        else:
            self.api_url = 'https://api.sandbox.gemini.com/v1/'


    def load_key(self, path):
        """ Load key and secret from file.

        Expected file format is key and secret on separate lines.
        
        :param path: path to keyfile
        :type path: str
        :returns: None
        
        """
        with open(path, 'r') as f:
            self.api_key = f.readline().strip()
            self.api_secret = f.readline().strip()
        return

    def get_symbols(self):
        """Returns all available symbols for trading."""      
        try: 
            return requests.get(self.api_url + 'symbols').json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_ticker(self, symbol):
        """Returns recent trading activity for a symbol"""
        try: 

            return requests.get(self.api_url + 'pubticker/' + symbol).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_current_order_book(self, symbol, limit_bids=None, limit_asks=None):
        """Get the current order book
        Args:
            symbol (str): Symbol such as btcusd.
            limit_bids (int): Optional. Max number of bids (offers to buy) to 
                return. Default is 50.                
            limit_asks (int): Optional. Max number of asks (offers to sell) to
                return. Default is 50.
        
        Returns:
            A JSON object with two arrays, one for bids and one for asks.
        """

        limits = {}
        if limit_bids is not None:
            limits["limit_bids"] = limit_bids
        if limit_asks is not None:
            limits["limit_asks"] = limit_asks
        
        try:
            return requests.get(self.api_url + symbol, params=limits).json()
        except requests.exceptions.RequestException as e:
            raise e

    def new_order(self, symbol, amount, price, side, client_order_id=None, 
        order_execution=None):
        """Place a new order
        Args:
            symbol (str): Symbol such as btcusd.
            amount (str): Decimal amount of BTC to purchase. Note that this 
                should be a string.
            price (str): Decimal amount of USD to spend per BTC. Note that this
                should be a string.
            side (str): Must be "buy" or "sell"
            order_execution (str): Optional. Order execution option.
                "maker-or-cancel" and "immediate-or-cancel" are the currently
                supported options.
        Returns: 
            A JSON object with information about the order.
        """
        
        fields = {
                'request': '/v1/order/new',
                'nonce': self._nonce(),

                # Request-specific items
                'symbol': symbol,  # Any symbol from the /symbols API
                'amount': amount,  # Once again, a quoted number
                'price': price,
                'side': side,  # Must be "buy" or "sell"

                # The order type; only "exchange limit" supported
                'type': 'exchange limit'
        }

        if client_order_id is not None:
            fields['client_order_id'] = client_order_id
        
        if order_execution is not None:
            fields['order_execution'] = [order_execution]
        
        try:
            return requests.post(self.api_url + 'order/new', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e
    
    def cancel_order(self, order_id):
        """Cancels an existing order with the given order_id"""
        fields = {
            'request': '/v1/order/cancel',
            'nonce': self._nonce(),
            'order_id': order_id
        }

        try:
            return requests.post(self.api_url + 'order/cancel', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def cancel_all_session_orders(self):
        """Cancels all orders for the current session"""
        fields = {
            'request': '/v1/order/cancel/session',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'order/cancel/session', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e
    
    def cancel_all_active_orders(self):
        """Cancels all orders across all sessions"""
        fields = {
            'request': '/v1/order/cancel/all',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'order/cancel/all', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_order_status(self, order_id):
        """Get the status of an order with given order_id"""
        fields = {
            'request': '/v1/order/status',
            'nonce': self._nonce(),
            'order_id': order_id
        }

        try:
            return requests.post(self.api_url + 'order/status', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_all_order_status(self):
        """Get the status of all active orders"""
        fields = {
            'request': '/v1/order',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'order', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_past_trades(self, symbol, limit_trades=None, timestamp=None):
        """Returns information about past trades.
        
        Args:
            limit_trades (int): Optional. The max number of trades to return. 
                Default is 50, max is 100.
            timestamp (int): Optional. Can be provided to only return trades 
                after timestamp. Can be in milliseconds or seconds.
        Returns: 
            Array of trade information items.
        """

        fields = {
            'request': '/v1/mytrades',
            'nonce': self._nonce(),
            'symbol': symbol,
        }

        if limit_trades is not None:
            fields["limit_trades"] = limit_trades

        if timestamp is not None:
            fields["timestamp"] = timestamp

        try:
            return requests.post(self.api_url + 'mytrades', 
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_trade_volume(self):
        """Get trade volume information for the account
        Returns: 
            Array where each element contains information about one day of 
            trading activity.
        """
        fields = {
            'request': '/v1/tradevolume',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'tradevolume',
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_balances(self):
        """Get available balances in the supported currencies
        
        Returns:
            Array where each element is for a different currency.
        """
        fields = {
            'request': '/v1/balances',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'balances',
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def heartbeat(self):
        """Prevents a session from timing out if the require heartbeat flag is 
        set when the API key was provisioned.
        """
        fields = {
            'request': '/v1/heartbeat',
            'nonce': self._nonce(),
        }

        try:
            return requests.post(self.api_url + 'heartbeat',
                headers=self._create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def _nonce(self):
        # Creates a 'nonce' by getting system time
        return int(round(time.time() * 1000))

    def _create_payload(self, fields):
        # Formats the headers as specified by the Gemini API
        encodedFields = base64.b64encode(json.dumps(fields).encode())

        headers = {
            'X-GEMINI-APIKEY': self.api_key,
            'X-GEMINI-PAYLOAD': encodedFields,
            'X-GEMINI-SIGNATURE': hmac.new(self.api_secret.encode(), 
                encodedFields, digestmod=hashlib.sha384).hexdigest()
        }

        return headers






# Set third argument to True if you are experimenting on api.sandbox.gemini.com
session = GeminiSession("key", "secret", False)
session.load_key(os.path.dirname(__file__) + '\..\gemini.key')


import krakenex



#configure api
k = krakenex.API()
k.load_key(os.path.dirname(__file__) + '\..\kraken.key')


for x in range(1, 1000):
    print ("")
        
    kbalance = k.query_private('Balance')
    # print(k.query_private('Balance'))
    kbalance = kbalance['result']

    k_usd = float(kbalance["ZUSD"])
    k_eth = float(kbalance["XETH"])

    print ("Kraken USD:  " + str(k_usd))
    print ("Kraken ETH:  " + str(k_eth))



    gbalance = session.get_balances()

    g_btc=gbalance[0]["available"]
    g_usd=gbalance[1]["available"]
    g_eth=gbalance[2]["available"]

    print ("Gemini USD:  " + str(g_usd))
    print ("Gemini ETH:  " + str(g_eth))
    # print ("Gemini BTC:  " + str(g_btc))


    k_ticker = k.query_public('Ticker',{'pair': 'XETHZUSD'})
    k_ticker = k_ticker['result']
    k_ask_eth = float(k_ticker["XETHZUSD"]["a"][0])
    k_bid_eth = float(k_ticker["XETHZUSD"]["b"][0])


    k_ask_eth = float(k_ask_eth * 1.0026)
    k_bid_eth = float(k_bid_eth * .9974)

    print ("Kraken Bid:  " + str(k_bid_eth))
    print ("Kraken Ask:  " + str(k_ask_eth))


    gbalance = session.get_ticker("ethusd")
    #print(session.get_ticker("ethusd"))

    g_bid_eth = float(gbalance["bid"])
    g_ask_eth = float(gbalance["ask"])


    g_ask_eth = float(g_ask_eth * 1.0025)
    g_bid_eth = float(g_bid_eth * .9975)

    print ("Gemini Bid:  " + str(g_bid_eth))
    print ("Gemini Ask:  " + str(g_ask_eth))



    #  Buy Gemini, Sell Kraken
    if float(k_bid_eth) > float(g_ask_eth) and float(g_usd) > float(100) and float(k_eth) > float(1):
        print("Buying on Gemini, Selling on Kraken")
        print(session.new_order("ethusd", ".001", "500","buy", "immediate-or-cancel"))
        print(k.query_private('AddOrder', {'pair': 'XETHZUSD',
                                 'type': 'sell',
                                 'ordertype': 'market',
                                 'price': '1',
                                 'volume': '.001'}))
        print("Transactions Complete")
        # sys.exit("Exit")

    #  Buy Kraken, Sell Gemini
    if float(g_bid_eth) > float(k_ask_eth) and float(k_usd) > float(100) and float(g_eth) > float(1):
        print("Buying on Kraken, Selling on Gemini")
        print(session.new_order("ethusd", ".001", "5","sell", "immediate-or-cancel"))
        print(k.query_private('AddOrder', {'pair': 'XETHZUSD',
                                 'type': 'buy',
                                 'ordertype': 'market',
                                 'price': '300',
                                 'volume': '.001'}))
        print("Transactions Complete")
        # sys.exit("Exit")


    time.sleep(30)
