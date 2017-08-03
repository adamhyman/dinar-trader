

"""
The Bittrex class is here:  https://github.com/ericsomdahl/python-bittrex/blob/master/bittrex/bittrex.py
"""


#import numpy as np
#a = np.array([1,2,3,4])


from liqui import Liqui

liqui_key = '../liqui.key'

with open(liqui_key, 'r') as f:
    key = f.readline().strip()
    secret = f.readline().strip()

my_liqui = Liqui(key, secret)

print (my_liqui.ticker('eth_btc'))
print (my_liqui.info())
print ('Balances:  ' + str(my_liqui.balances()) + '\n')



#print (my_liqui.depth('eth_btc')['eth_btc']['asks'])



from exchange_session import exchange_session

liqui = exchange_session(exchange='liqui', path_to_key=liqui_key)

liqui.update_balances()
liqui.print_balances()
liqui.update_books()
liqui.print_books()
#temp = liqui.get_balances()

#for b in temp:
#    print (b)
#    print (temp[b])


#liqui.print_balances()




### public api
##liqui.info()
##liqui.ticker('eth_btc')
##liqui.depth('eth_btc')
##liqui.trades('eth_btc')
##
### private api
##liqui.get_info()
##liqui.active_orders()
##liqui.order_info(314159265)
##liqui.cancel_order(271828182)
##liqui.trade('eth_btc', 'sell', 0.13, 10)
##liqui.trade_history()
##
### convenience methods
##liqui.balances()
##liqui.sell('eth_btc', 0.14, 10)
##liqui.buy('eth_btc', 0.12, 10)







