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
from .forms import (form_example, order_form_basic)
from MoarTrading.order_generator import order_basic

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
