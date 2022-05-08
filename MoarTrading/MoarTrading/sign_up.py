#what this file does, essentially, is allow the app to authenticate with tda api
#this file creates the client
import os
from tda import auth, client
import json
from .config import api_key
from .config import redirect_uri
from .config import token_path
from .definitions import ROOT_DIR
# api_key=config.api_key 
# redirect_uri=config.redirect_uri
# token_path=config.token_path

# ROOT_DIR=definitions.ROOT_DIR
try:
    client_local = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    with driver:#the chromdriver file needs to be found
        client_local = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)


#r = c.get_price_history('AAPL',
#        period_type=client.Client.PriceHistory.PeriodType.YEAR,
#        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#        frequency=client.Client.PriceHistory.Frequency.DAILY)
#assert r.status_code == 200, r.raise_for_status()
#print(json.dumps(r.json(), indent=4))

