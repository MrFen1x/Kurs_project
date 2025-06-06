from django import forms
from django.contrib.auth.forms import UserCreationForm
from images.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')