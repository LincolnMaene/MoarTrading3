"""less_talking_more_trading URL Configuration

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
from unicodedata import name
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from site_users.views import LoginPageView, SignUpView 
from site_users.views import profile
from django.contrib.auth.decorators import login_required    
#from less_talking_more_trading.views import home_view
urlpatterns = [


   path('sign_up/', SignUpView.as_view(),name='sign_up'),
   path('login/', LoginView.as_view(),name='login'),  
   path('logout/', LogoutView.as_view(), name='logout'),
   path('profile_update/', profile, name='profile_update'),
   path('accounts/profile/', profile, name='profile_update2'),
   #path('home/', home_view.as_view(), name='home'),
   
]
