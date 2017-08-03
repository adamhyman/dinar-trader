#This only runs when it is inside of the gdax-python folder.
#You should be able to use the Authenticated Client for everything.

from time import sleep
import gdax

public_client = gdax.PublicClient()

#print ('Products ' + str(public_client.get_products()))
#print ('')
#print ('Order Book:  ' + str(public_client.get_product_order_book('ETH-USD', level=2)))
#print ('')
print ('Ticker:  ' + str(public_client.get_product_ticker(product_id='ETH-USD')))
print ('')


#  Get ETH Prices
gdax_ticker = public_client.get_product_ticker(product_id='ETH-USD')
gdax_ask_eth = gdax_ticker['ask']
gdax_bid_eth = gdax_ticker['bid']

print ('ETH Ask is ' + str(gdax_ask_eth) + ' and ETH Bid is ' + str(gdax_bid_eth))


#  Get BTC Prices
gdax_ticker = public_client.get_product_ticker(product_id='BTC-USD')
print ('GDAX TICKER:  ' +str(gdax_ticker))
gdax_ask_btc = gdax_ticker['ask']
gdax_bid_btc = gdax_ticker['bid']

print ('BTC Ask is ' + str(gdax_ask_btc) + ' and BTC Bid is ' + str(gdax_bid_btc))


gdax_key = '../../gdax.key'

with open(gdax_key, 'r') as f:
    key = f.readline().strip()
    secret = f.readline().strip()
    passphrase = f.readline().strip()


auth_client = gdax.AuthenticatedClient(key, secret, passphrase)

def update_account_balances ():
    gdax_accounts = auth_client.get_accounts()

    print ('auth_client.get_accounts() looks like this:')
    print (str(gdax_accounts))
    print ('I want to make sure they don\'t change the order of the currencies.')

    #  Initialize the variables
    gdax_usd = 0
    gdax_ltc = 0
    gdax_eth = 0
    gdax_usd = 0

    #  Check that the order of the currencies in the array hasn't changed
    if gdax_accounts[0]['currency'] == 'USD':
        gdax_usd = gdax_accounts[0]['balance']
        
    if gdax_accounts[1]['currency'] == 'LTC':
        gdax_ltc = gdax_accounts[1]['balance']
        
    if gdax_accounts[2]['currency'] == 'ETH':
        gdax_eth = gdax_accounts[2]['balance']
        
    if gdax_accounts[3]['currency'] == 'BTC':
        gdax_btc = gdax_accounts[3]['balance']

    print ('GDAX USD Balance:  ' + str(gdax_usd))
    print ('GDAX LTC Balance:  ' + str(gdax_ltc))
    print ('GDAX ETH Balance:  ' + str(gdax_eth))
    print ('GDAX BTC Balance:  ' + str(gdax_btc))

update_account_balances ()
print ('')

#  This is the code that buys or sells.  Only uncomment 1 of the 4 rows at a time, while running it.

#  Buying:
#print (auth_client.buy(type='market', size='0.01', product_id='BTC-USD'))       #  This buys BTC
#print (auth_client.buy(type='market', size='0.01', product_id='ETH-USD'))       #  This buys ETH

#  Selling
#print (auth_client.sell(type='market', size='0.01', product_id='BTC-USD'))       #  This sells BTC
#print (auth_client.sell(type='market', size='0.01', product_id='ETH-USD'))       #  This sells ETH


print ('')
print ('')
sleep(5)  # Wait for the trade to be executed.

update_account_balances ()


