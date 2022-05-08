#this file should contain all funcitons necessary to place orders

from datetime import datetime
from .sign_up import client_local
import json
from tda.orders.generic import OrderBuilder
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session
#from .config import acct_id
from tda.orders.options import OptionSymbol, option_buy_to_open_market
from tda.orders.common import first_triggers_second



def generate_buy_equity_order(company_symbol,stock_quantity, price_limit):# if it works, should generate equity buy builder object

    

    return equity_buy_limit(company_symbol, stock_quantity,price_limit)
       

def order_basic(company_symbol, stock_quantity, price_limit, timing, session_in, acct_id): # we need an equity builder order object to place trades
    
    
    #this is the simples possible order build
        
        # All orders execute during the current normal trading session. If placed outside of trading hours, the execute during the next normal trading session.

        # Time-in-force is set to DAY.

        # All other fields (such as requested destination, etc.) are left unset, meaning they receive default treatment from TD Ameritrade. Note this treatment depends on TDA’s implementation, and may change without warning.
    
    duration=Duration.GOOD_TILL_CANCEL
    if(timing=='Day'):
        duration=Duration.DAY
    elif (timing=='Fill or Kill'):
        duration=Duration.FILL_OR_KILL


    


    session=Session.SEAMLESS
    if(session_in=='AM'):
        session=Session.AM
    elif(session_in=='PM'):
        session=Session.PM
    elif(session_in=='Normal'):
        session=Session.NORMAL
    
    #client_local=sign_up.client_local # we need a reference to the local client
    client_local.place_order(
    acct_id,  # account_id
    equity_buy_limit(company_symbol, stock_quantity,price_limit)
        .set_duration(duration)
        .set_session(session)
        .build())


def one_order_triggers_another(acct_id, order_1, order_2): #order_1 and order_2 must be generated using method in this
    # It appears that using these methods requires disabling Advanced Features on your account. 
    # It is not entirely clear why this is the case, but we’ve seen numerous reports of issues with OCO
    #  and trigger orders being resolved by this method. 
    # You can disable advanced features by calling TDAmeritrade support and requesting that they be turned off
    client_local.place_order(

        acct_id,
        first_triggers_second(order_1,order_2)

    )









def obtain_options_symbol(company_symbol, exp_year, exp_month, exp_day, put_call, strike_price):#this does not work, maybe someday!!!

    options_symbol=OptionSymbol(
    company_symbol, datetime.date(year=exp_year, month=exp_month, day=exp_day), put_call, strike_price).build()

    return options_symbol


def options_order_single(company_symbol, stock_quantity , acct_id): # we need an equity builder order object to place trades
    
    
    #this is the simples possible options order
    #had to hunt down some chinese website to figure out the documentation
        
        
        

    print('trying to order options for ',company_symbol)
    
    #client_local=sign_up.client_local # we need a reference to the local client
    client_local.place_order(
    acct_id,  # account_id
    option_buy_to_open_market(company_symbol, stock_quantity)
        )

