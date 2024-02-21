from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Player, Position, Squad, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django import forms
from .forms import CreateUserForm, SquadCreationForm
from django.contrib.auth.decorators import login_required #utilizar este decorador para proteger las rutas que requieren autenticación
from .utils import get_dot_positions, get_player_stats, get_pos_stats, get_default_stats, get_squad_players, search_players_by_positions, get_squad_stats
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
    squads = None
    stats = get_default_stats(player)
    if request.user.is_authenticated:
        user = request.user
        squads = user.userprofile.squads.all()
    return render(request, 'player_detail.html', {'player': player, 'dot_positions': dot_positions, 'stats': stats, 'squads': squads})

def position_stats_api(request, position, custom_id):
    # Retrieve statistics for the given position
    avg_stats = get_pos_stats(position)
    player = Player.objects.get(custom_id=custom_id)
    player_stats = get_player_stats(player, position)

    # Merge both dictionaries
    stats = {**avg_stats, **player_stats}

    # Return statistics as JSON response
    return JsonResponse(stats)

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
                messages.success(request, 'Login successfully! ' + 'Welcome ' + username)
                next_url = request.POST.get('next')  # Default redirect to 'home'
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')
            else:
                messages.success(request, 'Login failed!')
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('home')

def signup_user(request):
    if request.user.is_authenticated: 
        return redirect('home') 
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                UserProfile.objects.create(user=user)

                username = form.cleaned_data.get('username')
                login(request, user)
                messages.success(request, 'User created successfully!')
                messages.info(request, 'Welcome ' + username)
                return redirect('home')
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
            Q(Nationality__icontains=searched) | 
            Q(Pref_foot__icontains=searched) 
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

            if selected_positions != [] and filters != None:
                filters_list = json.loads(filters)
                # Redirect to search_results view with query parameters
                url = f'/search_results/?positions={",".join(selected_positions)}&filters={json.dumps(filters_list)}'
                return redirect(url)
            else:
                return render(request, 'advanced_search.html', {})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def search_results(request):
    # Retrieve positions and filters from query parameters
    positions_str = request.GET.get('positions', '')
    filters_str = request.GET.get('filters', '')
    
    positions = positions_str.split(',') if positions_str else []
    try:
        # Deserialize the entire filters JSON array
        filters = json.loads(filters_str) if filters_str else []
    except json.JSONDecodeError:
        filters = []

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
    players = Player.objects.all()
    print(positions)
    print(players)
    # Filter players by positions
    if positions:
        position_filters = Q()
        for position in positions:
            print(position)
            position_filters |= Q(Pos__name=position)
        players = players.filter(position_filters)
         

    if filters:
        for filter_dict in filters:
            # Extract filter properties from the dictionary
            property_name = filter_dict.get('property')
            filter_type = filter_dict.get('type')
            filter_value = filter_dict.get('value')

            # Construct the filter query based on the filter type
            if filter_type == "less":
                players = players.filter(**{f"{property_name}__lt": filter_value})
            elif filter_type == "greater":
                players = players.filter(**{f"{property_name}__gt": filter_value})
            elif filter_type == "equal":
                players = players.filter(**{f"{property_name}": filter_value})
            elif filter_type == "contains":
                players = players.filter(**{f"{property_name}__icontains": filter_value})

    # Ensure distinct players
    players = players.distinct()
    
    return players

@login_required(login_url='login')
def my_squads(request):
    user = request.user
    my_squads = user.userprofile.squads.all() 
    return render(request, 'my_squads.html', {'my_squads': my_squads})

@login_required(login_url='login')
def squad_builder(request):
    user_profile = request.user.userprofile
    squads = user_profile.squads.all()
    return render(request, 'squad_builder.html', {'squads': squads})

def squad_players(request, squad_id):
    players = get_squad_players(squad_id)
    player_names = [player.Name for player in players]
    return JsonResponse(player_names, safe=False)

def players_by_position(request, squad_id, position):
    # Convert position to string if it's passed as a list
    if isinstance(position, list) and len(position) == 1:
        position = position[0]
    
    # Retrieve players by position for the specified squad
    players = get_squad_players(squad_id)
    print(players)
    player_names = search_players_by_positions(players, position)
    return JsonResponse(player_names, safe=False)


@login_required(login_url='login')
def create_squad(request):
    if request.method == 'POST':
        form = SquadCreationForm(request.POST)
        if form.is_valid():
            squad = form.save(commit=False)
            squad = form.save()
            # Add the current user to the squad
            request.user.userprofile.squads.add(squad)
            return redirect('my_squads')
    else:
        form = SquadCreationForm()
    return render(request, 'create_squad.html', {'form': form})


@login_required(login_url='login')
def edit_squad(request, squad_id):
    squad = get_object_or_404(Squad, pk=squad_id)
    if request.method == 'POST':
        form = SquadCreationForm(request.POST, instance=squad)
        if form.is_valid():
            form.save()
            return redirect('my_squads')
    else:
        form = SquadCreationForm(instance=squad)
    return render(request, 'edit_squad.html', {'form': form})

@login_required(login_url='login')
def delete_squad(request, squad_id):
    squad = get_object_or_404(Squad, pk=squad_id)
    if request.method == 'POST':
        squad.delete()
        return redirect('my_squads')
    return render(request, 'delete_squad.html', {'squad': squad})


@login_required(login_url='login')
def add_to_squad(request, custom_id):
    player = get_object_or_404(Player, pk=custom_id)
    if request.method == 'POST':
        squad_id = request.POST.get('squad')
        if squad_id:
            squad = get_object_or_404(Squad, pk=squad_id)
            if player not in squad.players.all():
                squad.players.add(player)
                messages.success(request, f"{player.Name} added to {squad.name} squad successfully.")
                return redirect('player_detail', custom_id=custom_id)
            else:
                messages.warning(request, f"{player.Name} is already in {squad.name} squad.")
        else:
            messages.error(request, "Please select a squad.")
            pass
    # Redirect to player detail page if there is an error or no squad is selected
    return redirect('player_detail', custom_id=custom_id)

def squad_stats_api(request, position, players):
    # Deserialize the players JSON array
    players_list = json.loads(players)

    # Retrieve statistics for the given position and players
    stats = get_squad_stats(position, players_list)

    # Return statistics as JSON response
    return JsonResponse(stats)