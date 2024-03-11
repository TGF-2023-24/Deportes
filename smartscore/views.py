from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Player, Position, Squad, UserProfile, League
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django import forms
from .forms import CreateUserForm, SquadUpdateForm, SquadCreationForm
from django.contrib.auth.decorators import login_required #utilizar este decorador para proteger las rutas que requieren autenticación
from .utils import get_dot_positions, get_player_stats, get_pos_stats, get_default_stats, get_squad_players, search_players_by_positions, get_squad_stats, get_default_avg_stats, get_better_players
from django.http import JsonResponse, Http404
import json
from .dictionary import fifa_country_codes  
from .smartscore import smartScore
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
    # Check if the player's nationality code exists in the FIFA country codes
    flag_number = None
    if player.Nationality in fifa_country_codes:
        flag_number = fifa_country_codes[player.Nationality] 
    if request.user.is_authenticated:
        user = request.user
        squads = user.userprofile.squads.all()
    return render(request, 'player_detail.html', {'player': player, 'dot_positions': dot_positions, 'stats': stats, 'squads': squads, 'flag_number': flag_number})

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
    # Filter players by positions
    if positions:
        position_filters = Q()
        for position in positions:
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

    # Dictionary to hold players categorized by position for each squad
    players_by_position_per_squad = {}

    # Iterate through each squad
    for squad in my_squads:
        # Define positions to filter players
        goalkeepers = Position.objects.filter(name__startswith='GK')
        defenders = Position.objects.filter(name__in=('DC', 'DL', 'DR'))
        midfielders = Position.objects.filter(name__in=('DM', 'MC', 'ML', 'MR', 'AMC'))
        attackers = Position.objects.filter(name__in=('STC', 'AML', 'AMR'))

        # Filter players based on positions within the current squad
        players_by_position = {
            'goalkeepers': squad.players.filter(Pos__in=goalkeepers).distinct(),
            'defenders': squad.players.filter(Pos__in=defenders).distinct(),
            'midfielders': squad.players.filter(Pos__in=midfielders).distinct(),
            'attackers': squad.players.filter(Pos__in=attackers).distinct(),
        }

        # Add players categorized by position to the dictionary for the current squad
        players_by_position_per_squad[squad] = players_by_position

    return render(request, 'my_squads.html', {'my_squads': my_squads, 'players_by_position_per_squad': players_by_position_per_squad})


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
    filtered_players = search_players_by_positions(players, position)
    player_names = [player.Name for player in filtered_players]
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
        form = SquadUpdateForm(request.POST, instance=squad)
        if form.is_valid():
            form.save()
            return redirect('my_squads')
    else:
        form = SquadUpdateForm(instance=squad)
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

    players = Player.objects.filter(Name__in=players_list)

    avg_stats = get_pos_stats(position)
    avg_defaulf_stats = get_default_avg_stats(position)

    # Retrieve statistics for the given position and players
    stats = get_squad_stats(avg_stats, avg_defaulf_stats, position, players)

    # Return statistics as JSON response
    return JsonResponse(stats, safe=False)


def get_replacement_players(request, position, player, squad_id):
    # Retrieve replacement players based on position and exclude the current player

    squad = Squad.objects.get(pk=squad_id)

    current_players = squad.players.all()

    replacement_players = search_players_by_positions(Player.objects.all(), position)
    print("replacement_players", replacement_players)

    replacedPlayer = Player.objects.get(Name=player)
    replacement_players = get_better_players(replacedPlayer, replacement_players, position)
    player_names = [player.Name for player in replacement_players if player not in current_players]
    return JsonResponse(player_names, safe=False)

def compare_players(request, player1, player2, position):
    stats = {}
    stats[player1] = get_player_stats(Player.objects.get(Name=player1), position)
    stats[player2] = get_player_stats(Player.objects.get(Name=player2), position)
    stats['avg'] = get_pos_stats(position)
    # Return the player statistics as a JSON response
    return JsonResponse(stats, safe=False)

def replace_player(request, squad_id, old_player, new_player, pos):
    try:
        squad = Squad.objects.get(pk=squad_id)
        old_player = Player.objects.get(Name=old_player)
        new_player = Player.objects.get(Name=new_player)
        if old_player in squad.players.all():
            squad.players.remove(old_player)
            squad.players.add(new_player)
            return JsonResponse({'message': 'Player replaced successfully'}, status=200)  

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='login')
def futureScope(request):
    # Retrieve all leagues
    leagues = League.objects.all().order_by('country_league', 'name')
    
    # Extract unique country names from leagues
    countries = set(league.country_league for league in leagues)
    
    context = {
        'leagues': leagues,
        'countries': countries,
    }

    user_profile = request.user.userprofile
    
    if user_profile.league:
        context['budget'] = user_profile.budget
        context['selected_league'] = user_profile.league
        context['selected_expectations'] = user_profile.expectations
    
    return render(request, 'futureScope.html', context)

def save_futureScope(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transfer_budget = data.get('transfer_budget')
        selected_league = data.get('selected_league')
        selected_expectations = data.get('selected_expectations')

        # Get the current user's profile
        user_profile = request.user.userprofile

        print(transfer_budget, selected_league, selected_expectations)
        # Update the settings
        user_profile.budget = transfer_budget
        user_profile.league = selected_league
        user_profile.expectations = selected_expectations
        user_profile.save()

        return JsonResponse({'message': 'Settings saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='login')
def edit_futureScope(request):
    user_profile = request.user.userprofile
    
    # Retrieve all leagues
    leagues = League.objects.all().order_by('country_league', 'name')
    
    # Extract unique country names from leagues
    countries = set(league.country_league for league in leagues)
    
    initial_league = user_profile.league if user_profile.league else None
    initial_budget = user_profile.budget if user_profile.budget else None
    initial_expectations = user_profile.expectations if user_profile.expectations else None
    initial_country = League.objects.filter(name=initial_league).values_list('country_league', flat=True).first() if initial_league else None
    print("Initial league is", initial_league, "Initial country is", initial_country, "Initial budget is", initial_budget, "Initial expectations is", initial_expectations)


    context = {
        'leagues': leagues,
        'countries': countries,
        'initial_country': initial_country,
        'initial_league': initial_league,
        'initial_budget': initial_budget,
        'initial_expectations': initial_expectations,
    }

    return render(request, 'edit_futureScope.html', context)



def player_smartscore_api(request, position, custom_id):
    player = Player.objects.get(custom_id=custom_id)
    # If user is logged in, retrieve the future scope settings
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        league = user_profile.league
        expectations = user_profile.expectations
        budget = user_profile.budget
    else:
        league = ""
        expectations = 1
        budget = 9999
    print("League is", league, "Expectations is", expectations, "Budget is", budget)
    # Get the player's smartscore
    score = smartScore(player, position, budget, expectations, league)
    print("Score is", score)
    return JsonResponse({'smartscore': score})

def recommended_signings(request):
    # If user is logged in, retrieve the future scope settings
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        league = user_profile.league
        expectations = user_profile.expectations
        budget = user_profile.budget
    else:
        league = ""
        expectations = 1
        budget = 9999
    
    return render(request, 'recommended_signings.html')
