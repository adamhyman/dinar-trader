import os
from time import sleep
from exchange_session import exchange_session

kraken_key = '../kraken.key'
gemini_key = '../gemini.key'
gdax_key = '../gdax.key'

kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)
gdax = exchange_session(exchange='gdax', path_to_key=gemini_key)

bool_pause = True

while True:
   print ("Fetching exchange data...")

   # Get the balances of the accounts
   kbalances = kraken.get_balances()
   gbalances = gemini.get_balances()
   print ("Kraken USD: %s" % kbalances["USD"])
   print ("Kraken ETH: %s" % kbalances["ETH"])
   print ("Kraken BTC: %s" % kbalances["BTC"])
   print ("Gemini USD: %s" % gbalances["USD"])
   print ("Gemini ETH: %s" % gbalances["ETH"])
   print ("Gemini BTC: %s" % gbalances["BTC"])
   
   # Get the bid and asking prices
   k_trade_info = kraken.get_trade_info("ETHUSD")
   k_ask_eth = k_trade_info["ask"] * 1.0026
   k_bid_eth = k_trade_info["bid"] * 0.9974
   g_trade_info = gemini.get_trade_info("ETHUSD")
   g_ask_eth = g_trade_info["ask"] * 1.0025
   g_bid_eth = g_trade_info["bid"] * 0.9975
   
   print ("Kraken Bid:  " + str(k_bid_eth))
   print ("Kraken Ask:  " + str(k_ask_eth))
   print ("Gemini Bid:  " + str(g_bid_eth))
   print ("Gemini Ask:  " + str(g_ask_eth))

##   #Buy Gemini, Sell Kraken
##   if float(k_bid_eth) > float(g_ask_eth) and gbalances["USD"] > float(100) and kbalances["ETH"] > float(1):
##      print("Buying on Gemini, Selling on Kraken")
##      print(gemini.session.new_order("ethusd", ".001", "1000","buy", "immediate-or-cancel"))
##      print(kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'sell', 'ordertype': 'market', 'price': '20', 'volume': '.001'}))
##      print("Transactions Complete")
##      # sys.exit("Exit")
##      bool_pause = False
##
##   #Buy Kraken, Sell Gemini
##   if float(g_bid_eth) > float(k_ask_eth) and kbalances["USD"] > float(100) and gbalances["ETH"] > float(1):
##      print("Buying on Kraken, Selling on Gemini")
##      print(gemini.session.new_order("ethusd", ".001", "20","sell", "immediate-or-cancel"))
##      print(kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'buy', 'ordertype': 'market', 'price': '1000', 'volume': '.001'}))
##      print("Transactions Complete")
##      # sys.exit("Exit")
##      bool_pause = False
   print("")

   if bool_pause:
       sleep(30)
