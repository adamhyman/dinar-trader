
from geminiapi.gemini import GeminiSession

gemini_key = '../gemini.key'

with open(gemini_key, 'r') as f:
    key = f.readline().strip()
    secret = f.readline().strip()

gemini = GeminiSession(key, secret, False)

print (gemini.get_balances())



#  Sell ETHUSD
#  This works.
#print (gemini.new_order("ETHUSD", str(.001), ".01","sell", "immediate-or-cancel"))


#  This works.
#print (gemini.new_order("ETHUSD", str(.001), str(.01),"sell", "immediate-or-cancel"))

