import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..forms import CreateUserForm, SquadUpdateForm, CustomUserChangeForm, SquadCreationForm
from ..models import Squad, Player

@pytest.mark.django_db
def test_create_user_form_valid():
    # Test valid form data
    form = CreateUserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword123', 'password2': 'testpassword123'})
    assert form.is_valid()

@pytest.mark.django_db
def test_create_user_form_invalid():
    # Test invalid form data
    form = CreateUserForm(data={})  # Empty data should be invalid
    assert not form.is_valid()

@pytest.mark.django_db
def test_squad_update_form():
    # Test squad update form with instance
    squad = Squad.objects.create(name='Test Squad')
    player = Player.objects.create(
        Name="Cristiano Ronaldo",
        Club="Manchester United",
        League="Premier League",
        Nationality="Portugal",
        Pref_foot="Right",
        Age=37,
        Height=187,
        Weight=83,
        custom_id=2,
        Salary=60000,
        International_match=10,
        CAbil=85,
        Pot_abil=95,
        Strater_match=25,
        Res_match=15,
        Min=1800,
        Goal=7,
        Asis=5,
        xG=6.5,
        Gol_90=0.35,
        Asis_90=0.25,
        Goal_allowed=15,
        Clean_sheet=5,  
        Sv_rat=85,
        xSv_rat=80,
        Pen_saved_rat=75,
        Faga=25,
        Fcomm=20,
        Yel=3,
        Red=0,
        Dist_90=10.5,
        Key_tck_90=1.5,
        Key_hdr_90=1.0,
        Blocks_90=3.5,
        Clr_90=4.0,
        Int_90=2.0,
        Hdr_rat=90,
        Tackles_rat=80,
        Gl_mistake=2,
        Pass_rat=95,
        Pr_pass_90=90,
        Key_pass_90=2.5,
        Cr_c_90=4.0,
        Cr_c_acc=85,
        Ch_c_90=2.5,
        Drb_90=2.0,
        Poss_lost_90=9.5,
        Shot_rat=85,
        Conv_rat=20,
        Dorsal=7,
        Country_league="Test Country",
        market_value="15M"
    )
    form = SquadUpdateForm(instance=squad)
    assert 'players' in form.fields

@pytest.mark.django_db
def test_custom_user_change_form():
    # Test custom user change form
    user = User.objects.create(username='testuser', email='test@example.com')
    form = CustomUserChangeForm(instance=user)
    assert 'password' not in form.fields

@pytest.mark.django_db
def test_squad_creation_form():
    # Test squad creation form
    form = SquadCreationForm(data={'name': 'Test Squad'})
    assert form.is_valid()

    # Test invalid squad creation form with missing name
    form = SquadCreationForm(data={})
    assert not form.is_valid()
    assert 'name' in form.errors
