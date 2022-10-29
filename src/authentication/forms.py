from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import UserFollows

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

class FollowsUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        labels = {'ticket': 'Ticket', 'rating': 'Note', 'headline': 'Titre', 'body': 'Commentaire'}
        