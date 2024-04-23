import pytest
from django.urls import reverse
from django.test import RequestFactory
from ..models import Player, Squad, UserProfile  # Import your models
from ..views import player_detail  # Import your view function
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseNotFound


@pytest.mark.django_db
def test_player_detail_view_authenticated_user_with_squads():
    # Create a player object
    player = Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10M"
    )
    
    # Create a user and user profile
    user = User.objects.create(username='test_user')
    user.set_password('password')
    user.save()
    profile = UserProfile.objects.create(user=user)
    
    # Create squads for the user
    squad1 = Squad.objects.create(name="Squad 1")
    squad2 = Squad.objects.create(name="Squad 2")

    profile.squads.add(squad1)
    profile.squads.add(squad2)
    
    # Authenticate the user
    client = Client()
    client.login(username='test_user', password='password')

    # Create a request
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': player.custom_id}))
    request.user = user

    # Call the view function
    response = player_detail(request, custom_id=player.custom_id)

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the player name is present in the response content
    assert player.Name in response.content.decode('utf-8')

    # Check if the squads are present in the response context
    assert squad1.name in response.content.decode('utf-8')
    assert squad2.name in response.content.decode('utf-8')



@pytest.mark.django_db
def test_player_detail_view_authenticated_user_without_squads():
    # Create a player object
    player = Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10M"
    )
    
    # Create a user and user profile
    user = User.objects.create(username='test_user')
    user.set_password('password')
    user.save()
    UserProfile.objects.create(user=user)

    # Authenticate the user
    client = Client()
    client.login(username='test_user', password='password')

    # Create a request
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': player.custom_id}))
    request.user = user

    # Call the view function
    response = player_detail(request, custom_id=player.custom_id)

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the player name is present in the response content
    assert player.Name in response.content.decode('utf-8')

    assert 'No squads available' in response.content.decode('utf-8')
    

@pytest.mark.django_db
def test_player_detail_view_unauthenticated_user():
    player = Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10M"
    )
    
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': player.custom_id}))
    request.user = AnonymousUser()

    response = player_detail(request, custom_id=player.custom_id)

    assert response.status_code == 200

    assert player.Name in response.content.decode('utf-8')

    assert '<p>Please <a href="/login/?next=/player/1/">login</a> to add this player to a squad.</p>' in response.content.decode('utf-8')

@pytest.mark.django_db
def test_player_detail_view_nationality_code_exists():

    player = Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="ITA",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10M"
    )
        
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': player.custom_id}))
    request.user = AnonymousUser()

    response = player_detail(request, custom_id=player.custom_id)

    assert response.status_code == 200

    assert '776' in response.content.decode('utf-8')

@pytest.mark.django_db
def test_player_detail_view_nationality_code_missing():

    player = Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="Unknown",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10M"
    )
        
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': player.custom_id}))
    request.user = AnonymousUser()

    response = player_detail(request, custom_id=player.custom_id)

    assert response.status_code == 200

    assert 'alt="Unknown"' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_player_detail_view_player_not_found():
    request = RequestFactory().get(reverse('player_detail', kwargs={'custom_id': 2}))
    request.user = AnonymousUser()

    response = player_detail(request, custom_id=1)

    assert response.status_code == 404
    assert isinstance(response, HttpResponseNotFound)

