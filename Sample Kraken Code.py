
import krakenex

kraken_key = '../kraken.key'
mykraken = krakenex.API()
mykraken.load_key(kraken_key)



print (mykraken.query_private('Balance'))

print (mykraken.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'buy', 'ordertype': 'market', 'price': '1000', 'volume': str(.01)}))
print (mykraken.query_private('AddOrder', {'pair': 'XETHZUSD', 'type': 'sell', 'ordertype': 'market', 'price': '20', 'volume': str(.01)}))


##kraken_key = '../kraken.key'
##from exchange_session import exchange_session
##kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)


