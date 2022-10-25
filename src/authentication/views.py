from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth
from django.shortcuts import HttpResponse, redirect, render
from authentication.models import CustomUser 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View

from . import forms

# Create your views here.

# def connection_to_website(request):
#     if request.user.is_authenticated:
#         return redirect(settings.LOGIN_REDIRECT_URL)
#     else:
#         return render(request, 'login.html')

def logout(request):
   auth.logout(request)
   return render(request=request, template_name="logout.html")

class SignUpView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

class LoginView(View):
    template_name = 'login.html'
    form_class = forms.LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)

        
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})

    
# def signup_page(request):
#     context = {}
#     if request.method == 'POST':
#         form = forms.SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Vous êtes inscrit")
#         else:
#             context["errors"] = form.errors

#     return render(request, 'signup.html', context={'form': form})
