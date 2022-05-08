from  .sign_up import client_local
import json


def get_daily_price_history(symbol, price_list):


    parameter=(symbol, price_list)

    response=client_local.get_price_history_every_week(symbol)

    return json.dumps(response.json(), indent=4)