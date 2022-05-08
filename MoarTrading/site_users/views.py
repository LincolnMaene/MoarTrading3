from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from site_users.forms import LoginForm
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .forms import UpdateProfileForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from .config import acct_id

@login_required
def profile(request):
    

    if request.method == 'POST':
        #user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        #if user_form.is_valid() and profile_form.is_valid():
        if  profile_form.is_valid():
            #user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='basic_order')
    else:
        #user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    #return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
    return render(request, 'registration/update_profile.html', {'form': profile_form})


class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'registration/register.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


class LoginPageView(LoginView):
    
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile_update')
    success_message = "Login Successful"
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})



class logout_user(LogoutView):
    
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('login')
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})



