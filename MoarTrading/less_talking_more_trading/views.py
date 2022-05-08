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
from .forms import (form_example, order_form_basic,sell_form_basic, Quote_Query_Form)
from MoarTrading.order_generator import order_basic, one_order_triggers_another, options_order_single, generate_buy_equity_order
from MoarTrading.sell_generator import sell_basic, generate_sell_equity_order,sale_order_triggers_another
from MoarTrading.quote_generator import generate_quote


price_history_str=""

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
