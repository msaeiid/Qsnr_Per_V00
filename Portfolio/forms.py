from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Agah import forms
from Portfolio.models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'marital_status', 'birthday', 'occupation', 'country', 'city', 'image', 'about_me', 'title',
                  'phone', 'address']
