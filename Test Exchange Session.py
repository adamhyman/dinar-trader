import Bittrex
import liqui
from time import sleep
import random

from exchange_session import exchange_session


kraken_key = '../kraken.key'
gemini_key = '../gemini.key'
liqui_key = '../liqui.key'
bittrex_key = '../bittrex.key'
gdax_key =  '../gdax.key'

kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)
gdax = exchange_session(exchange='gdax', path_to_key=gdax_key)
liqui = exchange_session(exchange='liqui', path_to_key=liqui_key)
bittrex = exchange_session(exchange='bittrex', path_to_key=bittrex_key)



kraken.update_balances()
kraken.print_balances()
kraken.update_books()

gemini.update_balances()
gemini.print_balances()
gemini.update_books()

##gdax.update_balances()
##gdax.print_balances()
##gdax.update_books()
##
##bittrex.update_balances()
##bittrex.print_balances()
##bittrex.update_books()
##
##liqui.update_balances()
##liqui.print_balances()
##liqui.update_books()

# Constants
sleep_time_sec = 15
eth_trade_base = .02     # Random variable will be added to this.  This makes tying a pair of buy-and-sell orders together easy, because we can now tie on quantiy.




while True:
    try:
        eth_trade_qty = str(round((eth_trade_base + random.randint(1, 1000)/100000), 5))
        print (eth_trade_qty)

        kraken.update_books()
        gemini.update_books()
##        gdax.update_books()

        print ('Can buy on Kraken for:  ' + str(kraken.book_from_pair('ETHUSD').ask() * 1.0027))
        print ('Can buy on Gemini for:  ' + str(gemini.book_from_pair('ETHUSD').ask() * 1.0027))
        print ('Can buy on Gdax for:  ' + str(gdax.book_from_pair('ETHUSD').ask() * 1.0027))
        
        print ('Can sell on Kraken for:  ' + str(kraken.book_from_pair('ETHUSD').bid() * .9972))
        print ('Can sell on Gemini for:  ' + str(gemini.book_from_pair('ETHUSD').bid() * 0.9972))
        print ('Can sell on Gdax for:  ' + str(gdax.book_from_pair('ETHUSD').bid() * 0.9972))


        #  If I can buy on Kraken for less than I can sell on Gemini
        if (kraken.book_from_pair('ETHUSD').ask() * 1.0027) < (gemini.book_from_pair('ETHUSD').bid() * .9972) and kraken.book_from_pair('ETHUSD').base.get_balance() > 500 and gemini.book_from_pair('ETHUSD').currency.get_balance() > 1:
            print ('Buy Kraken.  Sell Gemini.')
            kraken.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
            gemini.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
            break

        if (gemini.book_from_pair('ETHUSD').ask() * 1.0027) < (kraken.book_from_pair('ETHUSD').bid() * .9972) and gemini.book_from_pair('ETHUSD').base.get_balance() > 500 and kraken.book_from_pair('ETHUSD').currency.get_balance() > 1:
            print ('Buy Gemini.  Sell Kraken.')
            kraken.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
            gemini.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
            break
        
##        if (kraken.book_from_pair('ETHUSD').ask() * 1.0027) < (gdax.book_from_pair('ETHUSD').bid() * .9972) and kraken.book_from_pair('ETHUSD').base.get_balance() > 100 and gdax.book_from_pair('ETHUSD').currency.get_balance() > 1:
##            print ('Buy Kraken.  Sell GDAX.')
##            kraken.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
##            gdax.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
##            break
##
##        if (gdax.book_from_pair('ETHUSD').ask() * 1.0027) < (kraken.book_from_pair('ETHUSD').bid() * .9972) and gdax.book_from_pair('ETHUSD').base.get_balance() > 100 and kraken.book_from_pair('ETHUSD').currency.get_balance() > 1:
##            print ('Buy GDAX.  Sell Kraken.')
##            kraken.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
##            gdax.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
##            break
##        
##        if (gdax.book_from_pair('ETHUSD').ask() * 1.0027) < (gemini.book_from_pair('ETHUSD').bid() * .9972) and gdax.book_from_pair('ETHUSD').base.get_balance() > 100 and gemini.book_from_pair('ETHUSD').currency.get_balance() > 1:
##            print ('Buy GDAX.  Sell Gemini.')
##            gdax.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
##            gemini.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
##            break
##
##        if (gemini.book_from_pair('ETHUSD').ask() * 1.0027) < (gdax.book_from_pair('ETHUSD').bid() * .9972) and gemini.book_from_pair('ETHUSD').base.get_balance() > 100 and gdax.book_from_pair('ETHUSD').currency.get_balance() > 1:
##            print ('Buy Gemini.  Sell GDAX.')
##            gdax.book_from_pair('ETHUSD').trade('sell', eth_trade_qty)
##            gemini.book_from_pair('ETHUSD').trade('buy', eth_trade_qty)
##            break
##
##
##        #  ETHBTC
##
##
##        
##        liqui.update_books()
##        bittrex.update_books()
##
##
##        print ('Can buy on Liqui for:  ' + str(liqui.book_from_pair('ETHBTC').ask() * 1.0027))
##        print ('Can buy on Bittrex for:  ' + str(bittrex.book_from_pair('ETHBTC').ask() * 1.0027))
##        print ('Can buy on Gemini for:  ' + str(gemini.book_from_pair('ETHBTC').ask() * 1.0027))
##
##        print ('Can sell on Bittrex for:  ' + str(bittrex.book_from_pair('ETHBTC').bid() * .9972))
##        print ('Can sell on Liqui for:  ' + str(liqui.book_from_pair('ETHBTC').bid() * 0.9972))
##        print ('Can sell on Gemini for:  ' + str(gemini.book_from_pair('ETHBTC').bid() * 0.9972))
##
##        #  Liqui / Bittrex
##        if (liqui.book_from_pair('ETHBTC').ask() * 1.0027) < (bittrex.book_from_pair('ETHBTC').bid() * .9972) and liqui.book_from_pair('ETHBTC').base.get_balance() > 100 and bittrex.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Liqui.  Sell Bittrex.')
##            bittrex.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            liqui.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break
##
##
##        if (bittrex.book_from_pair('ETHBTC').ask() * 1.0027) < (liqui.book_from_pair('ETHBTC').bid() * .9972) and bittrex.book_from_pair('ETHBTC').base.get_balance() > 100 and liqui.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Bittrex.  Sell Liqui.')
##            liqui.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            bittrex.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break
##
##        #  Liqui / Gemini
##        if (liqui.book_from_pair('ETHBTC').ask() * 1.0027) < (gemini.book_from_pair('ETHBTC').bid() * .9972) and liqui.book_from_pair('ETHBTC').base.get_balance() > 100 and gemini.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Liqui.  Sell Gemini.')
##            gemini.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            liqui.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break
##
##
##        if (gemini.book_from_pair('ETHBTC').ask() * 1.0027) < (liqui.book_from_pair('ETHBTC').bid() * .9972) and gemini.book_from_pair('ETHBTC').base.get_balance() > 100 and liqui.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Gemini.  Sell Liqui.')
##            liqui.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            gemini.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break
##
##        #  Bittrex / Gemini
##        if (bittrex.book_from_pair('ETHBTC').ask() * 1.0027) < (gemini.book_from_pair('ETHBTC').bid() * .9972) and bittrex.book_from_pair('ETHBTC').base.get_balance() > 100 and gemini.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Liqui.  Sell Gemini.')
##            gemini.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            bittrex.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break
##
##
##        if (gemini.book_from_pair('ETHBTC').ask() * 1.0027) < (bittrex.book_from_pair('ETHBTC').bid() * .9972) and gemini.book_from_pair('ETHBTC').base.get_balance() > 100 and bittrex.book_from_pair('ETHBTC').currency.get_balance() > 1:
##            print ('Buy Gemini.  Sell Liqui.')
##            bittrex.book_from_pair('ETHBTC').trade('sell', eth_trade_qty)
##            gemini.book_from_pair('ETHBTC').trade('buy', eth_trade_qty)
##            break

        
        sleep(31)

    except KeyboardInterrupt:
        print ("Exiting...")
        break
