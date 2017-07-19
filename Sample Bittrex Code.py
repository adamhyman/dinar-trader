

"""
The Bittrex wrapper is here:  https://github.com/ericsomdahl/python-bittrex/blob/master/bittrex/bittrex.py
"""


import Bittrex


bittrex_key = '../bittrex.key'

with open(bittrex_key, 'r') as f:
    key = f.readline().strip()
    secret = f.readline().strip()

bittrex = Bittrex.Bittrex(key, secret)


#print (bittrex.get_markets())
print (bittrex.get_ticker('BTC-LTC'))
print (bittrex.get_ticker('BTC-XRP'))
print (bittrex.get_ticker('BTC-ARK'))
print (bittrex.get_ticker('BTC-GNT'))
print (bittrex.get_ticker('BTC-BAT'))
print (bittrex.get_ticker('BTC-ETH'))
print (bittrex.get_ticker('ETH-GNT'))
print (bittrex.get_ticker('ETH-REP'))
print (bittrex.get_ticker('ETH-BAT'))




bittrex_BTC_LTC = bittrex.get_ticker('BTC-LTC')


bittrex_BTC_LTC_bid = bittrex_BTC_LTC['result']['Bid']
bittrex_BTC_LTC_ask = bittrex_BTC_LTC['result']['Ask']

print ('Bittrex BTC-LTC Bid:  ' + str(bittrex_BTC_LTC_bid))
print ('Bittrex BTC-LTC Ask:  ' + str(bittrex_BTC_LTC_ask))


import json



#  Get Balances



def getbalances () :

    bittrex_BAT = ''
    bittrex_BTC = ''
    bittrex_ETH = ''
    bittrex_GNT = ''
    bittrex_LTC = ''

    bittrex_balances = bittrex.get_balances()

    for i in bittrex_balances['result']:
        if i['Currency'] == 'BAT':
            bittrex_BAT = i['Balance']
        if i['Currency'] == 'BTC':
            bittrex_BTC = i['Balance']
        if i['Currency'] == 'ETH':
            bittrex_ETH = i['Balance']
        if i['Currency'] == 'GNT':
            bittrex_GNT = i['Balance']
        if i['Currency'] == 'LTC':
            bittrex_LTC = i['Balance']
        
    print ('BAT Bal:  ' + str(bittrex_BAT))
    print ('BTC Bal:  ' + str(bittrex_BTC))
    print ('ETH Bal:  ' + str(bittrex_ETH))
    print ('GNT Bal:  ' + str(bittrex_GNT))
    print ('LTC Bal:  ' + str(bittrex_LTC))
    print ('')

getbalances ()

#  Trading functions
#  I am currently getting an error when I run these:
#       {'success': False, 'message': 'MARKET_ORDERS_DISABLED', 'result': None}
#  I have contacted Bittrex support, to try resolve the error.
#  Ari, you're welcome to run them and see if it works.
#print (bittrex.buy_market('BTC-LTC', .5))
#print (bittrex.sell_market('BTC-LTC', .5))
