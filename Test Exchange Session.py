import Bittrex
import liqui

from exchange_session import exchange_session


kraken_key = '../kraken.key'
gemini_key = '../gemini.key'
liqui_key = '../liqui.key'
bittrex_key = '../bittrex.key'
gdax_key =  '../gdax.key'

kraken = exchange_session(exchange='kraken', path_to_key=kraken_key)
gemini = exchange_session(exchange='gemini', path_to_key=gemini_key)
##liqui = exchange_session(exchange='liqui', path_to_key=liqui_key)
##bittrex = exchange_session(exchange='bittrex', path_to_key=bittrex_key)
##gdax = exchange_session(exchange='gdax', path_to_key=gdax_key)





kraken.update_balances()
kraken.update_books()
## kraken.print_books()
kraken.books[0].trade('sell', .002)
## kraken.books[0].trade()
kraken.print_balances()



##gemini.update_balances()
##gemini.update_books()
##gemini.print_books()
##gemini.books[0].trade('buy', .002)
##gemini.print_balances()

##gemini.update_books()
##gemini.print_books()
##
##liqui.update_balances()
##liqui.print_balances()
##liqui.update_books()
##liqui.print_books()
##
##bittrex.update_balances()
##bittrex.print_balances()
##bittrex.print_books()
##bittrex.update_books()
##bittrex.print_books()
##
##gdax.update_balances()
##gdax.print_balances()
##gdax.print_books()
##gdax.update_books()
##gdax.print_books()



