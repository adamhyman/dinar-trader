
import krakenex

kraken_key = '../kraken.key'

mykraken = krakenex.API()
mykraken.load_key(kraken_key)


print (mykraken.query_private('Balance'))



kraken_key = '../kraken.key'
from exchange_session import exchange_session
kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)


