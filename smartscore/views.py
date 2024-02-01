from django.shortcuts import render
from .models import Player

# Create your views here.

def home(request):
    all_players = Player.objects.all()
    return render(request, 'home.html', {'all': all_players})

def about(request):
    return render(request, 'about.html', {})

   

