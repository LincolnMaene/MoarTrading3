from  .sign_up import client_local
import json

import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

# Usage:
d = Decimal("42.5")
json.dumps(d, cls=DecimalEncoder)

def generate_watchlist(acc_id, watchlist_spec):#takes in stock symbol and returns quote json
  
  response = client_local.create_watchlist(acc_id,watchlist_spec) # get quotes for Boeing company
  try:
    return (json.dumps(response.json(),indent=4))
  
  except json.JSONDecodeError :  # includes simplejson.decoder.JSONDecodeError
    print('Decoding JSON has failed')  

def create_watchlist_spec_equity(name,quantity, price_avg, commission, symbol, date):

  real_price = str(price_avg)
  real_com=str(commission)

  # formatted_datetime = date.isoformat()
  # json_datetime = json.dumps(formatted_datetime)

  spec={
    "name": name ,
    "watchlistItems": [
        {
            "quantity": quantity,
            "averagePrice": real_price,
            "commission": real_com, 
            "purchasedDate": date,
            "instrument": {
                "symbol": symbol,
                "assetType": 'EQUITY'
            }
        }
    ]
  }

  return spec