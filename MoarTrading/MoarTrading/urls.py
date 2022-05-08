"""MoarTrading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required    
from less_talking_more_trading.views import home_view
from less_talking_more_trading.views import (form_example_view, basic_order_view, basic_sell_view, Quote_query_view, Quote_view,options_view,
options_query_view, options_data_view, Movers_Query_view, Movers_data_view, Watchlist_query_view, Market_Query_view, Market_hours_view,
sale_trigger_sale_view,order_trigger_order_view)                                 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('order_trigger_order/',  login_required(order_trigger_order_view.as_view()), name='order_trigger_order'),
    path('sale_trigger_sale/',  login_required(sale_trigger_sale_view.as_view()), name='sale_trigger_sale'),
    path('options_order/', login_required(options_view.as_view()), name='options_order'),
    path('options_query/', login_required(options_query_view.as_view()), name='options_query'),
    path('movers_query/',  login_required(Movers_Query_view.as_view()), name='movers_query'),
    path('movers_data/', login_required(Movers_data_view.as_view()), name='movers_data'),
    path('options_data/', login_required(options_data_view.as_view()), name='options_data'),
    path('basic_order/', login_required(basic_order_view.as_view()), name='basic_order'),
    path('market_hours_query/',  login_required(Market_Query_view.as_view()), name='market_hours_query'),
    path('market_hours/', login_required(Market_hours_view.as_view()), name='market_hours'),
    path('home/', home_view.as_view(), name='home'),
    path('', home_view.as_view(), name='home_empty'),
    path('sell_basic/', login_required(basic_sell_view.as_view()), name='sell_basic'),
    path('quote_query/', login_required(Quote_query_view.as_view()), name='quote_query'),
    path('stock_quote/',  login_required(Quote_view.as_view()), name='stock_quote'),
    path('watchlist_query/',  login_required(Watchlist_query_view.as_view()), name='watchlist_query'),
    path('', include('site_users.urls')),
]
