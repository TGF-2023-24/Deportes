import pytest
from django.contrib.auth.models import User
from ..models import Player, Position, Squad, Shortlist, UserProfile, League

@pytest.fixture
def sample_user():
    return User.objects.create_user(username='test_user', password='test_password')


@pytest.fixture
def sample_squad():
    return Squad.objects.create(name='Test Squad')

@pytest.fixture
def sample_shortlist():
    return Shortlist.objects.create(name='Test Shortlist')

@pytest.fixture
def sample_user_profile(sample_user, sample_squad, sample_shortlist):
    return UserProfile.objects.create(user=sample_user, budget=100000, league='Test League', expectations=1)


def test_position_str():
    position = Position(name="Test Position")
    assert str(position) == "Test Position"

def test_squad_str():
    squad = Squad(name="Test Squad")
    assert str(squad) == "Test Squad"

def test_player_str():
    player = Player(Name="Test Player")
    assert str(player) == "Test Player"

def test_shortlist_str():
    shortlist = Shortlist(name="Test Shortlist")
    assert str(shortlist) == "Test Shortlist"

def test_league_str():
    league = League(name="Test League")
    assert str(league) == "Test League"

@pytest.mark.django_db
def test_user_profile_str(sample_user_profile):
    assert str(sample_user_profile) == "test_user"
    