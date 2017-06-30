import os
from time import sleep
from exchange_session import exchange_session

kraken_key = '../kraken.key'
gemini_key = '../gemini.key'

kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)

while True:
   print ("Fetching exchange data...")

   kbalances = kraken.get_balances()
   gbalances = gemini.get_balances()
   print ("Kraken USD: %s" % kbalances["USD"])
   print ("Kraken ETH: %s" % kbalances["ETH"])
   print ("Kraken BTC: %s" % kbalances["BTC"])
   print ("Gemini USD: %s" % gbalances["USD"])
   print ("Gemini ETH: %s" % gbalances["ETH"])
   print ("Gemini BTC: %s" % gbalances["BTC"])

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

   bool_pause = True
##   #Buy Gemini, Sell Kraken
##   if float(k_bid_eth) > float(g_ask_eth) and float(g_usd) > float(100) and float(k_eth) > float(1):
##      print("Buying on Gemini, Selling on Kraken")
##      print(gemini.session.new_order("ethusd", ".001", "500","buy", "immediate-or-cancel"))
##      print(kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'sell', 'ordertype': 'market', 'price': '1', 'volume': '.001'}))
##      print("Transactions Complete")
##      # sys.exit("Exit")
##      bool_pause = False
##
##   #Buy Kraken, Sell Gemini
##   if float(g_bid_eth) > float(k_ask_eth) and float(k_usd) > float(100) and float(g_eth) > float(1):
##      print("Buying on Kraken, Selling on Gemini")
##      print(gemini.session.new_order("ethusd", ".001", "5","sell", "immediate-or-cancel"))
##      print(kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'buy', 'ordertype': 'market', 'price': '300', 'volume': '.001'}))
##      print("Transactions Complete")
##      # sys.exit("Exit")
##      bool_pause = False
   print("")

   if bool_pause:
       sleep(30)
