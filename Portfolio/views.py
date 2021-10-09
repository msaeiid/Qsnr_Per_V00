from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from Portfolio.forms import RegisterForm, ProfileUpdateForm, JobForm
from Portfolio.models import Profile, Job


class RegisterView(CreateView):
    template_name = 'Portfolio/Account/Register.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('Portfolio:Profile', kwargs={'pk': self.request.user.profile.pk})


class LoginView(LoginView):
    template_name = 'Portfolio/Account/Login.html'


class LogoutView(LogoutView):
    pass


class ProfileUpdateView(UpdateView):
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
        return redirect(reverse('Portfolio:portfolio'))


class JobCreate(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'Portfolio/Job/Create.html'

    def post(self, request, *args, **kwargs):
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.profile = request.user.profile
            job.save()
            return redirect(reverse('Portfolio:portfolio'))


class JobUpdate(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'Portfolio/Job/Create.html'

    def post(self, request, *args, **kwargs):
        job = Job.objects.get(pk=kwargs.get('pk'))
        if request.user != job.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))

    def get_success_url(self):
        return reverse_lazy('Portfolio:portfolio')


def PortfolioView(request):
    if request.method == 'GET':
        pass

# Create your views here.
