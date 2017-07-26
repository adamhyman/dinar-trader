
from geminiapi.gemini import GeminiSession

gemini_key = '../gemini.key'

with open(gemini_key, 'r') as f:
    key = f.readline().strip()
    secret = f.readline().strip()

gemini = GeminiSession(key, secret, False)

print (gemini.get_balances())
