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

gdax.update_balances()
gdax.print_balances()
gdax.update_books()

bittrex.update_balances()
bittrex.print_balances()
bittrex.update_books()

liqui.update_balances()
liqui.print_balances()
liqui.update_books()

# Constants
sleep_time_sec = 15
eth_trade_base = .0     # Random variable will be added to this.  This makes tying a pair of buy-and-sell orders together easy, because we can now tie on quantiy.



while True:
    try:
        eth_trade_qty = str(round((eth_trade_base + random.randint(1, 10000)/100000), 5))
        print (eth_trade_qty)

        kraken.update_books()
        gemini.update_books()
        gdax.update_books()

        print ('Can buy on Kraken for:  ' + str(kraken.books[0].ask() * 1.0027))
        print ('Can buy on Gemini for:  ' + str(gemini.books[0].ask() * 1.0027))
        print ('Can buy on Gdax for:  ' + str(gdax.books[0].ask() * 1.0027))
        
        print ('Can sell on Kraken for:  ' + str(kraken.books[0].bid() * .9972))
        print ('Can sell on Gemini for:  ' + str(gemini.books[0].bid() * 0.9972))
        print ('Can sell on Gdax for:  ' + str(gdax.books[0].bid() * 0.9972))


        #  If I can buy on Kraken for less than I can sell on Gemini
        if (kraken.books[0].ask() * 1.0027) < (gemini.books[0].bid() * .9972) and kraken.books[0].base.get_balance() > 100 and gemini.books[0].currency.get_balance() > 1:
            print ('Buy Kraken.  Sell Gemini.')
            kraken.books[0].trade('buy', eth_trade_qty)
            gemini.books[0].trade('sell', eth_trade_qty)
            break

        if (gemini.books[0].ask() * 1.0027) < (kraken.books[0].bid() * .9972) and gemini.books[0].base.get_balance() > 100 and kraken.books[0].currency.get_balance() > 1:
            print ('Buy Gemini.  Sell Kraken.')
            kraken.books[0].trade('sell', eth_trade_qty)
            gemini.books[0].trade('buy', eth_trade_qty)
            break
        
        if (kraken.books[0].ask() * 1.0027) < (gdax.books[0].bid() * .9972) and kraken.books[0].base.get_balance() > 100 and gdax.books[0].currency.get_balance() > 1:
            print ('Buy Kraken.  Sell GDAX.')
            kraken.books[0].trade('buy', eth_trade_qty)
            gdax.books[0].trade('sell', eth_trade_qty)
            break

        if (gdax.books[0].ask() * 1.0027) < (kraken.books[0].bid() * .9972) and gdax.books[0].base.get_balance() > 100 and kraken.books[0].currency.get_balance() > 1:
            print ('Buy GDAX.  Sell Kraken.')
            kraken.books[0].trade('sell', eth_trade_qty)
            gdax.books[0].trade('buy', eth_trade_qty)
            break
        
        if (gdax.books[0].ask() * 1.0027) < (gemini.books[0].bid() * .9972) and gdax.books[0].base.get_balance() > 100 and gemini.books[0].currency.get_balance() > 1:
            print ('Buy GDAX.  Sell Gemini.')
            gdax.books[0].trade('buy', eth_trade_qty)
            gemini.books[0].trade('sell', eth_trade_qty)
            break

        if (gemini.books[0].ask() * 1.0027) < (gdax.books[0].bid() * .9972) and gemini.books[0].base.get_balance() > 100 and gdax.books[0].currency.get_balance() > 1:
            print ('Buy Gemini.  Sell GDAX.')
            gdax.books[0].trade('sell', eth_trade_qty)
            gemini.books[0].trade('buy', eth_trade_qty)
            break


        #  BTC ETH


        
        liqui.update_books()
        bittrex.update_books()


        print ('Can buy on Liqui for:  ' + str(liqui.books[0].ask() * 1.0027))
        print ('Can buy on Bittrex for:  ' + str(bittrex.books[0].ask() * 1.0027))
        print ('Can buy on Gemini for:  ' + str(gemini.books[1].ask() * 1.0027))

        print ('Can sell on Bittrex for:  ' + str(bittrex.books[0].bid() * .9972))
        print ('Can sell on Liqui for:  ' + str(liqui.books[0].bid() * 0.9972))
        print ('Can sell on Gemini for:  ' + str(gemini.books[1].bid() * 0.9972))

        #  Liqui / Bittrex
        if (liqui.books[0].ask() * 1.0027) < (bittrex.books[0].bid() * .9972) and liqui.books[0].base.get_balance() > 100 and bittrex.books[0].currency.get_balance() > 1:
            print ('Buy Liqui.  Sell Bittrex.')
            bittrex.books[0].trade('sell', eth_trade_qty)
            liqui.books[0].trade('buy', eth_trade_qty)
            break


        if (bittrex.books[0].ask() * 1.0027) < (liqui.books[0].bid() * .9972) and bittrex.books[0].base.get_balance() > 100 and liqui.books[0].currency.get_balance() > 1:
            print ('Buy Bittrex.  Sell Liqui.')
            liqui.books[0].trade('sell', eth_trade_qty)
            bittrex.books[0].trade('buy', eth_trade_qty)
            break

        #  Liqui / Gemini
        if (liqui.books[0].ask() * 1.0027) < (gemini.books[1].bid() * .9972) and liqui.books[0].base.get_balance() > 100 and gemini.books[1].currency.get_balance() > 1:
            print ('Buy Liqui.  Sell Gemini.')
            gemini.books[1].trade('sell', eth_trade_qty)
            liqui.books[0].trade('buy', eth_trade_qty)
            break


        if (gemini.books[1].ask() * 1.0027) < (liqui.books[0].bid() * .9972) and gemini.books[1].base.get_balance() > 100 and liqui.books[0].currency.get_balance() > 1:
            print ('Buy Gemini.  Sell Liqui.')
            liqui.books[0].trade('sell', eth_trade_qty)
            gemini.books[1].trade('buy', eth_trade_qty)
            break

        #  Bittrex / Gemini
        if (bittrex.books[0].ask() * 1.0027) < (gemini.books[1].bid() * .9972) and bittrex.books[0].base.get_balance() > 100 and gemini.books[1].currency.get_balance() > 1:
            print ('Buy Liqui.  Sell Gemini.')
            gemini.books[1].trade('sell', eth_trade_qty)
            bittrex.books[0].trade('buy', eth_trade_qty)
            break


        if (gemini.books[1].ask() * 1.0027) < (bittrex.books[0].bid() * .9972) and gemini.books[1].base.get_balance() > 100 and bittrex.books[0].currency.get_balance() > 1:
            print ('Buy Gemini.  Sell Liqui.')
            bittrex.books[0].trade('sell', eth_trade_qty)
            gemini.books[1].trade('buy', eth_trade_qty)
            break

        
        sleep(31)

    except KeyboardInterrupt:
        print ("Exiting...")
        break
