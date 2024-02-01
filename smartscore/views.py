from django.shortcuts import render, redirect
from .models import Player
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import CreateUserForm

# Create your views here.

def home(request):
    all_players = Player.objects.all()
    return render(request, 'home.html', {'all': all_players})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('home')
        else:
            messages.success(request, 'Login failed!')
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('home')

def signup_user(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('login') # Redirigir al usuario a la página de inicio de sesión, hay que cambiarlo
        else:
            messages.error(request, 'An error occurred during the registration process')
    
    context = {'form': form}
    return render(request, 'signup.html', context)
   

   

