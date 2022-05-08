from  .sign_up import client_local
import json


def single_market_hours(Market, Date):

    market_input=client_local.Markets(Market)

    response=client_local.get_hours_for_single_market(market_input,Date)



    return json.dumps(response.json())