from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Player, Position
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django import forms
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required #utilizar este decorador para proteger las rutas que requieren autenticación
from .utils import get_dot_positions, get_player_stats, get_pos_stats  # Import the get_dot_positions function
from django.http import JsonResponse, Http404
import json
#se usa @login_required(login_url='login') en la vista que se quiere proteger

# Create your views here.

def home(request):
    all_players = Player.objects.all()
    return render(request, 'home.html', {'all': all_players})

def about(request):
    return render(request, 'about.html', {})

def player_detail(request, custom_id):
    player = Player.objects.get(custom_id=custom_id)
    # Call the get_dot_positions function to calculate dot positions
    dot_positions = get_dot_positions(player.Pos)
    stats = get_player_stats(player)
    avg_stats = get_pos_stats()
    return render(request, 'player_detail.html', {'player': player, 'dot_positions': dot_positions, 'stats': stats, 'avg_stats': avg_stats})

def login_user(request):
    if request.user.is_authenticated: #habrá que cambiar el redirect, esto debe ser cutre, pero por el momento nos vale
        return redirect('home') 
    else:
        if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if(user is not None):
                login(request, user)
                messages.success(request, 'Login successfully!')
                messages.info(request, 'Welcome ' + username)
                return redirect('home')
            else:
                messages.success(request, 'Login failed!')
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('home')

def signup_user(request):
    if request.user.is_authenticated: #habrá q cambiarlo tmb
        return redirect('home') 
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'User created successfully!')
                messages.info(request, 'Welcome ' + user)
                return redirect('login') # Redirigir al usuario a la página de inicio de sesión, hay que cambiarlo
            else:
                messages.error(request, 'An error occurred during the registration process')
        
        context = {'form': form}
        return render(request, 'signup.html', context)
   

def search_player(request):
    if request.method == 'POST':
        searched = request.POST['q']
        
        players = Player.objects.filter(
            Q(Name__icontains=searched) | 
            Q(Club__icontains=searched) | 
            Q(League__icontains=searched) | 
            Q(Nacionality__icontains=searched) | 
            Q(Pref_foot__icontains=searched) 
            #| Q(Pos__icontains=searched) 
        )


        return render(request, 'search_player.html', {'searched': searched, 'players': players})
    else:
        return render(request, 'search_player.html', {})

   
def advanced_search(request):
    if request.method == 'GET':
        try:
            # Retrieve parameters from the request
            selected_positions = request.GET.getlist('selectedPositions')
            filters = request.GET.get('filters')
            print("We are in the advanced search view")
            print(selected_positions)  # Print selected positions to console
            print(filters)  # Print filters to console  

            if selected_positions != [] and filters != None:
                filters_list = json.loads(filters)
                # Redirect to search_results view with query parameters
                url = f'/search_results/?positions={",".join(selected_positions)}&filters={json.dumps(filters_list)}'
                return redirect(url)
            else:
                print("We do this once")
                return render(request, 'advanced_search.html', {})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def search_results(request):
    # Retrieve positions and filters from query parameters
    positions_str = request.GET.get('positions', '')
    filters_str = request.GET.get('filters', '')
    
    positions = positions_str.split(',') if positions_str else []
    filters = filters_str.split(',') if filters_str else []
    print("We are in the search results view")
    print(positions)  # Print positions to console
    print(filters)  # Print filters to console

    try:
        # Perform search based on positions and filters
        results = perform_search(positions, filters)

        if not results:
            raise Http404("No results found.")

        # Render the search results template with the results
        return render(request, 'search_results.html', {'results': results})
    
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
    

def perform_search(positions, filters):
    print("We are in the perform search function")
    print(positions)  # Print positions to console
    players = Player.objects.all()

    # Filter players by positions
    if positions:
        position_filters = Q()
        for position in positions:
            position_filters |= Q(Pos__name=position)
        players = players.filter(position_filters)

    print("We will return the players now")
    print(players)  # Print players to console
    return players