from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserFollows

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

class FollowsUserForm(forms.ModelForm):
    def clean_input_username_of_user_to_follow(self):
        input_username_of_user_to_follow = self['followed_user']
        if not CustomUser.objects.filter(username=input_username_of_user_to_follow).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas")
        return input_username_of_user_to_follow

    class Meta:
        model = UserFollows
        fields = ['followed_user']
        widgets = {
            'followed_user': forms.TextInput()
        }
        labels = {'followed_user': "Suivre d'autres utilisateurs"}
    

            
        