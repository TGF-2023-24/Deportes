import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Squad, UserProfile, Player
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

@pytest.fixture
def user_client(client):

    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(user=user)
    client.force_login(user)
    return client

@pytest.fixture
def squad():
    squad = Squad.objects.create(name='Test Squad')
    UserProfile.objects.first().squads.add(squad)
    return squad

@pytest.mark.django_db
def test_my_squads_view(user_client, squad):

    response = user_client.get(reverse('my_squads'))
    assert response.status_code == 200
    assert squad.name in response.content.decode()


@pytest.fixture
def player():
    return  Player.objects.create(
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
def test_create_squad_view_get(user_client):

    response = user_client.get(reverse('create_squad'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_squad_view_post(user_client):

    data = {'name': 'New Squad'}
    response = user_client.post(reverse('create_squad'), data)
    assert response.status_code == 302  # Should redirect after successful POST

    # Ensure the squad is created and associated with the user
    user = get_user_model().objects.get(username='test_user')
    assert user.userprofile.squads.filter(name='New Squad').exists()

@pytest.mark.django_db
def test_edit_squad_view(user_client, squad):

    response = user_client.get(reverse('edit_squad', kwargs={'squad_id': squad.id}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_squad_view(user_client, squad):

    response = user_client.post(reverse('delete_squad', kwargs={'squad_id': squad.id}))
    assert response.status_code == 302  # Should redirect after successful deletion

    # Ensure the squad is deleted
    assert not Squad.objects.filter(id=squad.id).exists()

@pytest.mark.django_db
def test_add_to_squad_view(user_client, player, squad):

    data = {'squad': squad.id}
    response = user_client.post(reverse('add_to_squad', kwargs={'custom_id': player.custom_id}), data)
    assert response.status_code == 302  # Should redirect after successful addition

    # Ensure the player is added to the squad
    assert squad.players.filter(custom_id=player.custom_id).exists()

    # Test message functionality
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "success"