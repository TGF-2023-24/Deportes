import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from ..models import Shortlist, Player, UserProfile
from ..views import  remove_from_shortlist, save_recommendations 
import json

@pytest.fixture
def user(client):
    # Create a user for testing
    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(user=user)  # Create a related UserProfile
    client.force_login(user)
    return user

@pytest.fixture
def shortlist():
    shortlist_obj = Shortlist.objects.create(name='Test Shortlist')
    UserProfile.objects.first().shortlist.add(shortlist_obj)
    return shortlist_obj


@pytest.fixture
def player():
    return    Player.objects.create(
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
        market_value="10"
    )

@pytest.mark.django_db
def test_save_recommendations_view(user):
    url = reverse('save_recommendations')
    data = {
        'position': 'Position',
        'archetype': 'Archetype',
        'foot': 'Foot',
        'recommendation': {'name': 'Test Player'}
    }
    request = RequestFactory().post(url, data=json.dumps(data), content_type='application/json')
    request.user = user
    response = save_recommendations(request)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_shortlist_view(user, shortlist, client):  # Add 'client' to the function arguments
    response = client.get(reverse('shortlist'))  # Use the client to make the request
    assert response.status_code == 200
    assert shortlist.name in response.content.decode()

@pytest.mark.django_db
def test_remove_from_shortlist_view(user, shortlist, player):
    shortlist.players.add(player)
    url = reverse('remove_from_shortlist', kwargs={'shortlist_id': shortlist.id, 'player_id': player.custom_id})
    request = RequestFactory().get(url)
    request.user = user
    response = remove_from_shortlist(request, shortlist_id=shortlist.id, player_id=player.custom_id)
    assert response.status_code == 302
    assert player not in shortlist.players.all()
