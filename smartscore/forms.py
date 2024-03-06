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
    expectations = forms.ChoiceField(choices=EXPECTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    # Define the fields for country and league
    country = forms.ModelChoiceField(queryset=League.objects.values_list('country_league', flat=True).distinct(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     empty_label='Select Country')
    league = forms.ModelChoiceField(queryset=League.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    empty_label='Select League')

    class Meta:
        model = UserProfile
        fields = ['country', 'league', 'budget', 'expectations']

    def __init__(self, *args, **kwargs):
        super(editFutureScopeForm, self).__init__(*args, **kwargs)

        # Pre-select the country and corresponding league if available
        if self.instance.pk:  # If form is for editing an existing instance
            try:
                user_profile_league = self.instance.league
                league_object = League.objects.get(name=user_profile_league)
                self.fields['country'].initial = league_object.country_league
                self.fields['league'].queryset = League.objects.filter(country_league=league_object.country_league).order_by('name')
                self.fields['league'].initial = user_profile_league
            except League.DoesNotExist:
                pass

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country:
            return country
        raise forms.ValidationError('Please select a country.')

    def clean_league(self):
        league = self.cleaned_data.get('league')
        if league:
            return league
        raise forms.ValidationError('Please select a league.')

    