import os
import csv
import logging
import sys
import http.client
import socket
from time import sleep
from datetime import datetime
from exchange_session import exchange_session

# Constants
sleep_time_sec = 15

# Key locations
kraken_key = '../kraken.key'
gemini_key = '../gemini.key'
gdax_key = '../gdax.key'

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

# Session initialization
kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)
gdax = exchange_session(exchange='gdax', path_to_key=gemini_key)

# Set up CSV log file and write headers
logfile = open("log.csv", 'w', newline='')
log_writer = csv.writer(logfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
log_writer.writerow(['Date', 'Time', 'Kraken Balance (USD)', 'Kraken Balance (ETH)', 'Kraken Balance (BTC)', 'Gemini Balance (USD)', 'Gemini Balance (ETH)', 'Gemini Balance (BTC)', 'Kraken ETHUSD Ask', 'Kraken ETHUSD Bid', 'Gemini ETHUSD Ask', 'Gemini ETHUSD Bid',])

# Get the initial balances of the accounts
logging.info ("Getting balances.")
kbalances = kraken.get_balances()
gbalances = gemini.get_balances()
logging.info ("")

logging.info ("Running exchange queries and looking for opportunities.")

while True:
   try:
       # Get the bid and asking prices
       logging.info ("Getting prices.")
       k_trade_info = kraken.get_trade_info("ETHUSD")
       k_ask_eth = k_trade_info["ask"] * 1.0026
       k_bid_eth = k_trade_info["bid"] * 0.9974
       g_trade_info = gemini.get_trade_info("ETHUSD")
       g_ask_eth = g_trade_info["ask"] * 1.0025
       g_bid_eth = g_trade_info["bid"] * 0.9975

       logging.info ("Kraken Bid:  %s" % k_bid_eth)
       logging.info ("Kraken Ask:  %s" % k_ask_eth)
       logging.info ("Gemini Bid:  %s" % g_bid_eth)
       logging.info ("Gemini Ask:  %s" % g_ask_eth)
       logging.info ("")
       
       log_writer.writerow([datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S.%f'), str(kbalances["USD"]), str(kbalances["ETH"]), str(kbalances["BTC"]), str(gbalances["USD"]), str(gbalances["ETH"]), str(gbalances["BTC"]), str(k_ask_eth), str(k_bid_eth), str(g_ask_eth), str(g_bid_eth)])

       # Buy Gemini, Sell Kraken
       if float(k_bid_eth) > float(g_ask_eth) and gbalances["USD"] > float(100) and kbalances["ETH"] > float(1):
            logging.info ("Buying on Gemini, Selling on Kraken")
            # TO DO: Handle the exception in exchange_session.py
            try:
                logging.info (kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'sell', 'ordertype': 'market', 'price': '20', 'volume': '.001'}))
            except (http.client.HTTPException, socket.timeout) as ex:
                logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                logging.info ("Sleeping %s seconds and restarting Loop." % (ex, sleep_time_sec))
                sleep(sleep_time_sec)
                continue
            logging.info (gemini.session.new_order("ethusd", ".001", "1000","buy", "immediate-or-cancel"))
            logging.info ("Transactions Complete")
            kbalances = kraken.get_balances()
            gbalances = gemini.get_balances()

       # Buy Kraken, Sell Gemini
       if float(g_bid_eth) > float(k_ask_eth) and kbalances["USD"] > float(100) and gbalances["ETH"] > float(1):
            logging.info ("Buying on Kraken, Selling on Gemini")
            # TO DO: Handle the exception in exchange_session.py
            try:
                logging.info (kraken.session.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'buy', 'ordertype': 'market', 'price': '1000', 'volume': '.001'}))
            except (http.client.HTTPException, socket.timeout) as ex:
                logging.warning ("\"{0}\" exception occurred. Arguments: {1!r}".format(type(ex).__name__, ex.args))
                logging.info ("Sleeping %s seconds and restarting Loop." % (ex, sleep_time_sec))
                sleep(sleep_time_sec)
                continue
            logging.info (gemini.session.new_order("ethusd", ".001", "20","sell", "immediate-or-cancel"))
            logging.info ("Transactions Complete")
            kbalances = kraken.get_balances()
            gbalances = gemini.get_balances()
        
       logging.info ("No opportunities found. Sleeping for %s seconds." % sleep_time_sec)
       logging.info ("")
       sleep(sleep_time_sec)
   except KeyboardInterrupt:
       print ("Exiting...")
       break

logfile.close()
