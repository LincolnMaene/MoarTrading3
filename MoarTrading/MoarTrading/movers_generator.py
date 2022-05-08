from  .sign_up import client_local
import json


def get_movers(index, direction, change):#Top 10 (up or down) movers by value or percent for a particular Market
        

    real_direction= client_local.Movers.Direction.UP# we need to convert user input to what the code expects
    real_change=client_local.Movers.Change.VALUE

  

    if(direction=='DOWN'):
        real_direction=client_local.Movers.Direction.DOWN

    if(change=='PERCENT'):
       real_change=client_local.Movers.Change.PERCENT

    response=client_local.Movers()

    response=client_local.get_movers(index,real_direction, real_change)

    print("http respons: ",response)

    print(response.json())

    return (response.json())