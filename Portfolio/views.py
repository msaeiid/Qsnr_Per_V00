from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from Portfolio.forms import RegisterForm


class Register(CreateView):
    success_url = '/here/'
    template_name = 'Portfolio/Register.html'
    form_class = RegisterForm


class Login(LoginView):
    template_name = 'Portfolio/Login.html'


class Logout(LogoutView):
    pass

# Create your views here.
