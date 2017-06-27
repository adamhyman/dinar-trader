import krakenex

k = krakenex.API()

print("Hi")

print(k.query_public('Depth',{'pair': 'XXBTZUSD', 'count': '10'}))

print("Hi")
import json

k_data = k.query_public('Ticker',{'pair': 'XXBTZUSD'})
k_data = json.load(k_data)

print("123")

print(k_data["result"][0][0])

print("123")
print(k.query_public('Ticker',{'pair': 'XXBTZUSD'}))
