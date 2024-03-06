from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Squad, Player, UserProfile, League

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SquadUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(SquadUpdateForm, self).__init__(*args, **kwargs)
        # Retrieve the instance of the squad being updated
        instance = kwargs.get('instance')
        # If the instance exists, update the queryset for players to only include those in the squad
        if instance:
            self.fields['players'] = forms.ModelMultipleChoiceField(queryset=Player.objects.filter(squad=instance), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Squad
        fields = ['name', 'players']


class SquadCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    players = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Squad
        fields = ['name', 'players']

class editFutureScopeForm(forms.ModelForm):

     # Define choices for expectations
    EXPECTATION_CHOICES = [
        (0, 'Short Term Success'),
        (1, 'Balanced Approach'),
        (2, 'Long Term Success')
    ]

    # Define the field for expectations
    expectations = forms.ChoiceField(choices=EXPECTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


     # Retrieve all leagues
    #Add countries first
    leagues = League.objects.all().order_by('country_league', 'name')

    league = forms.ModelChoiceField(queryset=leagues, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['league', 'budget', 'expectations']


    