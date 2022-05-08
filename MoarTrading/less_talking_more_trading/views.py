from django.shortcuts import render
import datetime
import re
import email
from pickle import NONE
from this import d
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .forms import (form_example, order_form_basic,sell_form_basic, Quote_Query_Form, options_form, options_query_form,
Movers_Query_Form, Watchlist_query_form, Market_Query_Form, sale_trigger_form)
from MoarTrading.order_generator import order_basic, one_order_triggers_another, options_order_single, generate_buy_equity_order
from MoarTrading.sell_generator import sell_basic, generate_sell_equity_order,sale_order_triggers_another
from MoarTrading.quote_generator import generate_quote
from MoarTrading.market_hours_generator import single_market_hours
from MoarTrading.option_chains_generator import generate_options_calls_date, generate_options_put_date
from MoarTrading.movers_generator import get_movers
from MoarTrading.watchlist_generator import create_watchlist_spec_equity, generate_watchlist
from MoarTrading.market_hours_generator import single_market_hours





# #example for how to access user profile in function based view
    # u = User.objects.get(username=request.user.username)
    # tda_id = u.profile.tdameritrade_id


   

    # print(acct_id)

    #for class based views use: self.request.user.username



#these lines essentiall fill the options_query object with junk data so function knows what type it is
trial_start_date=datetime.datetime.strptime('2022-2-22', '%Y-%m-%d').date()
trial_end_date=datetime.datetime.strptime('2022-2-22', '%Y-%m-%d').date()
price_history_str=""


options_query_object=list() #this will hold query data for option chains
hours_query_object=single_market_hours('EQUITY',trial_end_date)#this will hold query data for market hours chains
movers_query_obj=NONE
stock_quote_obj=NONE
#setup for options query object ends here

class sale_trigger_sale_view(FormView):

    template_name='one_sale_triggers_another.html'

    form_class=sale_trigger_form

    success_url='/home'


    def form_valid(self, form):

        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id

        


        company_1_symbol=form.cleaned_data['company_1_symbol']#GET compay 1 daTA
        stock_1_quantity=form.cleaned_data['stock_1_quantity']
        price_1_limit=form.cleaned_data['price_1_limit']

        company_2_symbol=form.cleaned_data['company_2_symbol']#GET compay 2 daTA
        stock_2_quantity=form.cleaned_data['stock_2_quantity']
        price_2_limit=form.cleaned_data['price_2_limit']
        timing=form.cleaned_data['timing'] #useless better to replace with choice between trigger cancel and trigger order
        session=form.cleaned_data['session']  #useless better to replace with choice between trigger cancel and trigger order

        order_1=generate_sell_equity_order(company_1_symbol, stock_1_quantity, price_1_limit)
        order_2=generate_sell_equity_order(company_2_symbol, stock_2_quantity, price_2_limit)

        sale_order_triggers_another(tda_id, order_1, order_2)

        #print(company_1_symbol,stock_1_quantity, price_1_limit, company_2_symbol,stock_2_quantity, price_2_limit)

    





        

        return super().form_valid(form)


class Market_Query_view(FormView):

    

    template_name='market_hours_query.html'

    form_class=Market_Query_Form

    success_url='/market_hours'


    def form_valid(self, form):

        global hours_query_object #without this python just creates a local var
        

        Market=form.cleaned_data['Market']
        Year=form.cleaned_data['Year']#GET compay 1 daTA
        Month=form.cleaned_data['Month']
        Day=form.cleaned_data['Day']#GET compay 1 daTA
        Hour=form.cleaned_data['Hour']
        Minutes=form.cleaned_data['Minutes']#GET compay 1 daTA
       
        
        date_maker = datetime.datetime(Year, Month, Day, Hour, Minutes)

        hours_query_object=single_market_hours(Market, date_maker)

        #print(hours_query_object)

        

    





        

        return super().form_valid(form)


class Market_hours_view (APIView):#!!!! CHECK FORMAT FOR FOREX, BONDS ETC...!!!!

    authentication_classes=[]
    permission_classes=[]

    def get(self,request, format=None):

        global hours_query_object
        is_open=False#tells us if the market is open
        


        #print(options_query_object)

        # data={

        #     "sales":177,
        #     "customers":120,
        # }

      

        hours_query_object=hours_query_object.split(",")
        

       
       
        index=0
        hrs_str=""
        for x in hours_query_object:
            if "start" in x or "end" in x:
                is_open=True
                hrs_str=hrs_str+x+","

        hrs_str=hrs_str.split("{")

        hrs_str_two=""

        for x in hrs_str:

            if "start" in x or "end" in x:
                
                hrs_str_two=hrs_str_two+x+","
                #print(hrs_str_two)
        
        hrs_str_two=hrs_str_two.split(",")

        hrs_str_3=""
        for x in hrs_str_two:
           if "start" in x or "end" in x:
                
                hrs_str_3=hrs_str_3+x+","
                #print(hrs_str_two)
        forbid_string1="\""
        forbid_string2="{"
        forbid_string3="}"
        forbid_string4="["
        forbid_string5="]"

        hrs_str_3=hrs_str_3.replace(forbid_string1,'')
        hrs_str_3=hrs_str_3.replace(forbid_string2,'')
        hrs_str_3=hrs_str_3.replace(forbid_string3,'')
        hrs_str_3=hrs_str_3.replace(forbid_string4,'')
        hrs_str_3=hrs_str_3.replace(forbid_string5,'')

        hrs_str_3=hrs_str_3.split(',')
           


        print(hrs_str_3)
           
       

        if is_open==True: #if market is open
            
            data=hrs_str_3
            
            return render(request, 'market_hrs.html', {'data': data})
        
        return render(request, 'maket_closed_err.html')



class Watchlist_query_view(FormView):

    template_name='watchlist_query.html'

    form_class=Watchlist_query_form

    success_url='/home'


    def form_valid(self, form):

        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id
        
        symbol=form.cleaned_data['symbol']
        name=form.cleaned_data['name']
        date=form.cleaned_data['date']
        quantity=form.cleaned_data['quantity']
        price_avg=form.cleaned_data['price_avg']
        commission=form.cleaned_data['commission']

        real_date=datetime.datetime.strptime(date, '%Y-%m-%d').date()

      
      
      
        spec=create_watchlist_spec_equity(name,quantity,price_avg,commission,symbol,date)

        # print(spec)

        # print(tda_id)

        print(generate_watchlist(tda_id,spec))





        

        return super().form_valid(form)


class Movers_data_view (APIView): #this should give the user the top ten movers for that day and so on and so forth

    authentication_classes=[]
    permission_classes=[]

    list_of_lists=[[]] * 10

    list_of_descriptions=[[]] * 10

    list_of_symbols=[[]] * 10

    

    

   

    def get(self,request, format=None):
        nothing_found=1

        print("!!!!!type of movers query object is:", type(movers_query_obj))

        print("!!!!!size of movers query object is:", len(movers_query_obj))

        size=10

        if(len(movers_query_obj)>0):

            nothing_found=0

            print("size greater than zero")

            for x in range(0, size):

                Movers_data_view.list_of_lists[x]=list(movers_query_obj[x].items())

            for x in range(0, size):

                Movers_data_view.list_of_descriptions[x]=list(Movers_data_view.list_of_lists[x][1])

            for x in range(0, size):

                Movers_data_view.list_of_symbols[x]=list(Movers_data_view.list_of_lists[x][4])

            for x in range(0, size):

                Movers_data_view.list_of_symbols[x]=str(Movers_data_view.list_of_symbols[x])
                Movers_data_view.list_of_descriptions[x]=str(Movers_data_view.list_of_descriptions[x])
        
        
            #by the time we reach here, i have converted the symbols and company names into usable strings for html

            #print(Movers_data_view.list_of_symbols)
            # for x in jsonObject:#     print(x)

            disallowed_substr="['description', '"
            disallowed_substr2="']"
            disallowed_substr3="['symbol', '"
            
            for x in range(0, size):

                Movers_data_view.list_of_symbols[x]=Movers_data_view.list_of_symbols[x].replace(disallowed_substr3, "")
                Movers_data_view.list_of_symbols[x]=Movers_data_view.list_of_symbols[x].replace(disallowed_substr2, "")
                Movers_data_view.list_of_descriptions[x]=Movers_data_view.list_of_descriptions[x].replace(disallowed_substr, "")
                Movers_data_view.list_of_descriptions[x]=Movers_data_view.list_of_descriptions[x].replace(disallowed_substr2, "")

            range_html=[0,1,2,3,4,5]

            compact_list=zip(Movers_data_view.list_of_descriptions, Movers_data_view.list_of_symbols)




            return render(request, 'movers_display.html', 
                {'description': compact_list })

        else:

            return render(request, 'movers_display.html', 
                {'nothing': nothing_found})


          

class Movers_Query_view(FormView):

    

    template_name='movers_query.html'

    form_class=Movers_Query_Form

    success_url='/movers_data'


    def form_valid(self, form):

        global movers_query_obj

        global hours_query_object #without this python just creates a local var
        

        index=form.cleaned_data['index']
        direction=form.cleaned_data['direction']#GET compay 1 daTA
        change=form.cleaned_data['change']
       
       
       

        movers_query_obj=get_movers(index,direction,change)

        #print("type of query obj: ",type(movers_query_obj))

    





        

        return super().form_valid(form)



class options_data_view (APIView): #this allows us to see  option data

    authentication_classes=[]
    permission_classes=[]

    

    def get(self,request, format=None):

        data_view=1

        global options_query_object #the plan is to take string returned by function them extract symbols

        data1=""
        data2=""
        data3=""
        data4=""

        options_query_object=options_query_object.split(",")

        for item in options_query_object:

            if item.find("symbol")!=-1:
               data1=data1+item

        data1=data1.split(":")
        disallowed_substr1="{\""
        disallowed_substr2="\""
        disallowed_substr3="symbol"

        for item in data1:
            item=item.replace(disallowed_substr1, "")
            item=item.replace(disallowed_substr2, ",")
            item=item.replace(disallowed_substr3, "")
            
            data2=data2+item
        
        data2=data2.split(",")
        index=0
        for item in data2:

            if(item!="" and item!=''):
                data3=data3+item
                

            index=index+1

        data3=data3.split(" ")

        
        for item in data3:
            if not item:
               item="x"
            else:
                data4=data4+item+","
        
        data4=data4.split(",")
            


                
            
            
            
           
        
        #print(data4)
        return render(request, 'options_symbols.html', {'data': data4, 'data_view': data_view})


class options_view(FormView):

    template_name='options_order.html'

    form_class=options_form

    success_url='/home'


    def form_valid(self, form):

        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id
        
        underlying_symbol=form.cleaned_data['underlying_symbol']
        quantity=form.cleaned_data['quantity']
        
        #print(underlying_symbol, expiration_date, contract_type, strike_price_as_string)

        options_order_single(underlying_symbol,quantity, tda_id)



        # same for all other fields, can also do form.save() if model form





        

        return super().form_valid(form)

class options_query_view(FormView): #this view is repsonsible for giving us a query of options data

    template_name='options_query.html'

    form_class=options_query_form

    success_url='/options_data'


    def form_valid(self, form):
        
        global options_query_object#without global, python will just create a local variable

        underlying_symbol=form.cleaned_data['underlying_symbol']
        end_date=form.cleaned_data['end_date']
        start_date=form.cleaned_data['start_date']
        strike_number=form.cleaned_data['strike_number']
        contract_type=form.cleaned_data['contract_type']

        #print(underlying_symbol, expiration_date, contract_type, strike_price_as_string)

        # start_date=datetime.datetime.strptime('2022-2-22', '%Y-%m-%d').date()
        # end_date=datetime.datetime.strptime('2023-12-31', '%Y-%m-%d').date()



        # same for all other fields, can also do form.save() if model form

        if(contract_type=='Call'):
            options_query_object=generate_options_calls_date(underlying_symbol, strike_number , start_date, end_date)
        else:
            options_query_object=generate_options_put_date(underlying_symbol, strike_number , start_date, end_date)

        #print(options_query_object)




        

        return super().form_valid(form)




class Quote_view(TemplateView):##this displayds the price history

    template_name="stock_quote.html"

    

    

    def get_context_data(self, **kwargs):
        global stock_quote_obj
        price_len=len(price_history_str)#this tells us the lenght of the price history list
        
       
        context=super().get_context_data(**kwargs)
        context["quote_data"]=stock_quote_obj#we need to serialize to json otherwise it's all strings, impossible to work with
        context["len"]=price_len
       

        #print(context["labels"])
        return context


class Quote_query_view(FormView):

    template_name='quote_query.html'

    form_class=Quote_Query_Form

    success_url='/stock_quote'


    def form_valid(self, form):

        global stock_quote_obj

        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id
        
        symbol=form.cleaned_data['symbol']
      
        #price_list = []
        #print(underlying_symbol, expiration_date, contract_type, strike_price_as_string)
        response = generate_quote(symbol)

        disallowed_substr="{[, '"

        #print(response)

        #response=generate_quote(symbol)

        # the goal is to split the price hisotry string so as to have nothign but the raw numerical data (high point each week)
        
        
        split_str=response.split()

        empty_string = ""

        index_str=0
        #print(split_str)
        for item in split_str: #this allowes me to pick for data i want  from string above

            

            bidprice='"bidPrice":'
            askprice='"askPrice":'
            openprice='"openPrice":'
            highprice='"highPrice":'
            lowprice='"lowPrice":'
            closeprice='"closePrice":'
          

            #print(item)

            if item==bidprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])
            elif item==askprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])
            elif item==openprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])

            elif item==highprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])

            elif item==lowprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])
            elif item==closeprice:
                #print(item)
                empty_string=empty_string+split_str[index_str+1]
                #print(split_str[index_str])
                #print(split_str[index_str+1])

            index_str=index_str+1


     


        empty_string=empty_string.split(',')

        # print(empty_string[0])

        
        stock_quote_obj=empty_string
        

        # same for all other fields, can also do form.save() if model form





        

        return super().form_valid(form)

class basic_sell_view(FormView):

    template_name='basic_sell.html'

    form_class=sell_form_basic

    success_url='/home'


    def form_valid(self, form):
        
        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id
       
        company_symbol=form.cleaned_data['sell_company_symbol']
        stock_quantity=form.cleaned_data['sell_quantity']
        price_limit=form.cleaned_data['sell_price_limit']
        timing=form.cleaned_data['timing']
        session=form.cleaned_data['session']

        sell_basic(company_symbol, stock_quantity, price_limit, timing, session, tda_id)

        # same for all other fields, can also do form.save() if model form


       

        return super().form_valid(form)




class home_view(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'home.html', {})


# Create your views here.
class basic_order_view(FormView):

    template_name='basic_order.html'

    form_class=order_form_basic

    success_url='/basic_order'

    


    def form_valid(self, form):
        
        username_query=self.request.user.username #get id of logged in user 

        logged_in_user =  User.objects.get(username=username_query) #get user object

        tda_id = logged_in_user.profile.tdameritrade_id #get user ameritrade id

        # print('acct id: ')
        # print(tda_id)




        company_symbol=form.cleaned_data['company_symbol']
        stock_quantity=form.cleaned_data['stock_quantity']
        price_limit=form.cleaned_data['price_limit']
        timing=form.cleaned_data['timing']
        session=form.cleaned_data['session']

        order_basic(company_symbol, stock_quantity, price_limit, timing, session, tda_id)

        # same for all other fields, can also do form.save() if model form


        

        return super().form_valid(form)


class form_example_view(FormView):

    # we grab the model form
    
   
    template_name='form_example.html'

    form_class=form_example

    success_url='/home'


    def form_valid(self, form):
        
        name=form.cleaned_data['name']
        email=form.cleaned_data['email']

        

        # same for all other fields, can also do form.save() if model form


        print(name, email)

        return super().form_valid(form)
