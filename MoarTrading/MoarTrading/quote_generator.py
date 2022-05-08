from  .sign_up import client_local
import json

def generate_quote(stock_symbol):#takes in stock symbol and returns quote json
  response = client_local.get_quotes(stock_symbol) # get quotes for Boeing company
  return (json.dumps(response.json(),indent=4))








