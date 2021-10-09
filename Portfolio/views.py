from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from Portfolio.forms import RegisterForm, ProfileUpdateForm
from Portfolio.models import Profile


class RegisterView(CreateView):
    template_name = 'Portfolio/Account/Register.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('Portfolio:Profile', kwargs={'pk': self.request.user.profile.pk})


class LoginView(LoginView):
    template_name = 'Portfolio/Account/Login.html'


class LogoutView(LogoutView):
    pass


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'Portfolio/Profile/Update.html'
    form_class = ProfileUpdateForm

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
        if profile.user != request.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = ProfileUpdateForm(request.POST, instance=profile, files=request.FILES)
        if form.is_valid():
            form.save()
# Create your views here.
