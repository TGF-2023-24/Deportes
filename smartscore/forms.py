from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Squad, Player

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


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['username', 'email']
        labels = {
            'username': 'Username',
            'email': 'Email address',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password fields
        self.fields.pop('password')

class SquadCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    #players = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Squad
        fields = ['name']  
