from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Agah import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
