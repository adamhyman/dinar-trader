import os
from time import sleep
from exchange_session import exchange_session

# Read in key files
# TO DO: Put this as a separate function
kraken_key = '../kraken.key'
gemini_key = '../gemini.key'

kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)

while True:
   print ("Fetching exchange data...")
       
   kbalance = kraken.session.query_private('Balance')
   # print(kraken.session.query_private('Balance'))
   kbalance = kbalance['result']

   k_usd = float(kbalance["ZUSD"])
   k_eth = float(kbalance["XETH"])

   print ("Kraken USD:  " + str(k_usd))
   print ("Kraken ETH:  " + str(k_eth))

   gbalance = gemini.session.get_balances()

   g_btc=gbalance[0]["available"]
   g_usd=gbalance[1]["available"]
   g_eth=gbalance[2]["available"]

   print ("Gemini USD:  " + str(g_usd))
   print ("Gemini ETH:  " + str(g_eth))
   # print ("Gemini BTC:  " + str(g_btc))

   k_ticker = kraken.session.query_public('Ticker',{'pair': 'XETHZUSD'})
   k_ticker = k_ticker['result']
   k_ask_eth = float(k_ticker["XETHZUSD"]["a"][0])
   k_bid_eth = float(k_ticker["XETHZUSD"]["b"][0])

   k_ask_eth = float(k_ask_eth * 1.0026)
   k_bid_eth = float(k_bid_eth * .9974)

   print ("Kraken Bid:  " + str(k_bid_eth))
   print ("Kraken Ask:  " + str(k_ask_eth))

   gbalance = gemini.session.get_ticker("ethusd")
   #print(gemini.session.get_ticker("ethusd"))

   g_bid_eth = float(gbalance["bid"])
   g_ask_eth = float(gbalance["ask"])

   g_ask_eth = float(g_ask_eth * 1.0025)
   g_bid_eth = float(g_bid_eth * .9975)

   print ("Gemini Bid:  " + str(g_bid_eth))
   print ("Gemini Ask:  " + str(g_ask_eth))

   ##  Buy Gemini, Sell Kraken
   #if float(k_bid_eth) > float(g_ask_eth) and float(g_usd) > float(100) and float(k_eth) > float(1):
   #    print("Buying on Gemini, Selling on Kraken")
   #    print(gemini.session.new_order("ethusd", ".001", "500","buy", "immediate-or-cancel"))
   #    print(kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD',
   #                             'type': 'sell',
   #                             'ordertype': 'market',
   #                             'price': '1',
   #                             'volume': '.001'}))
   #    print("Transactions Complete")
   #    # sys.exit("Exit")
   #
   ##  Buy Kraken, Sell Gemini
   #if float(g_bid_eth) > float(k_ask_eth) and float(k_usd) > float(100) and float(g_eth) > float(1):
   #    print("Buying on Kraken, Selling on Gemini")
   #    print(gemini.session.new_order("ethusd", ".001", "5","sell", "immediate-or-cancel"))
   #    print(kraken..query_private('AddOrder', {'pair': 'XETHZUSD',
   #                             'type': 'buy',
   #                             'ordertype': 'market',
   #                             'price': '300',
   #                             'volume': '.001'}))
   #    print("Transactions Complete")
   #    # sys.exit("Exit")
   print("")
   sleep(30)
