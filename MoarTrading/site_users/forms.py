from cProfile import label
from tkinter.ttk import Style
from unicodedata import category
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist



class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['username', 'email', 'first_name']


class LoginForm(forms.Form):
    put_or_call=[('PUT', 'p'), ('Call','c')]
    username= forms.CharField()
    password = forms.CharField()
    
# Basically we are hooking the create_user_profile, this is not a form, it's a model i'm too affraid to move
#  and save_user_profile methods to the User model, 
#  whenever a save event occurs. This kind of signal is called post_save. 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tdameritrade_id = models.IntegerField("Please Enter TDAmeritrade ID:", default=00000000000)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tdameritrade_id',)
        #labels = {
        #"tdameritrade_id": "Please Enter TDAmeritrade ID"
        #}
        