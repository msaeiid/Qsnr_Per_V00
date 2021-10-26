from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from Portfolio.forms import RegisterForm, ProfileUpdateForm, JobForm, SkillForm, EducationForm, LanguageForm, \
    CertificateForm
from Portfolio.models import Profile, Job, Skill, Education, Language, Certificate


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
    template_name = 'Portfolio/Job/CreateAndUpdate.html'

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
    template_name = 'Portfolio/Job/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        job = Job.objects.get(pk=kwargs.get('pk'))
        if request.user != job.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))


def JobDelete(request, pk):
    if request.method == 'GET':
        job = get_object_or_404(Job, pk=pk)
        if request.user != job.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        job.delete()
        return redirect(reverse('Portfolio:portfolio'))


class SkillCreate(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'Portfolio/Skill/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            return redirect(reverse('Portfolio:portfolio'))


class SkillUpdate(UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'Portfolio/Skill/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        skill = Skill.objects.get(pk=kwargs.get('pk'))
        if request.user != skill.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))


def SkillDelete(request, pk):
    if request.method == 'GET':
        skill = get_object_or_404(Skill, pk=pk)
        if request.user != skill.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        skill.delete()
        return redirect(reverse('Portfolio:portfolio'))


class EducationCreate(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'Portfolio/Education/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = request.user.profile
            education.save()
            return redirect(reverse('Portfolio:portfolio'))


class EducationUpdate(UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'Portfolio/Education/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        education = Education.objects.get(pk=kwargs.get('pk'))
        if request.user != education.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))


def EducationDelete(request, pk):
    if request.method == 'GET':
        education = get_object_or_404(Education, pk=pk)
        if request.user != education.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        education.delete()
        return redirect(reverse('Portfolio:portfolio'))


class LanguageCreate(CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'Portfolio/Language/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.profile = request.user.profile
            language.save()
            return redirect(reverse('Portfolio:portfolio'))


class LanguageUpdate(UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'Portfolio/Language/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        language = Language.objects.get(pk=kwargs.get('pk'))
        if request.user != language.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))


def LanguageDelete(request, pk):
    if request.method == 'GET':
        language = get_object_or_404(Language, pk=pk)
        if request.user != language.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        language.delete()
        return redirect(reverse('Portfolio:portfolio'))


class CertificateCreate(CreateView):
    model = Certificate
    form_class = CertificateForm
    template_name = 'Portfolio/Certificate/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        form = CertificateForm(request.POST, files=request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.profile = request.user.profile
            certificate.save()
            return redirect(reverse('Portfolio:portfolio'))


class CertificateUpdate(UpdateView):
    model = Certificate
    form_class = CertificateForm
    template_name = 'Portfolio/Certificate/CreateAndUpdate.html'

    def post(self, request, *args, **kwargs):
        certificate = Certificate.objects.get(pk=kwargs.get('pk'))
        if request.user != certificate.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        form = CertificateForm(request.POST, instance=certificate, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('Portfolio:portfolio'))


def CertificateDelete(request, pk):
    if request.method == 'GET':
        certificate = get_object_or_404(Certificate, pk=pk)
        if request.user != certificate.profile.user:
            return render(request, 'Portfolio/error.html', context={'error_title': 'Access denied!',
                                                                    'error': ' only profile owner can update this profile'})
        certificate.delete()
        return redirect(reverse('Portfolio:portfolio'))


def PortfolioView(request):
    if request.method == 'GET':
        pass


def Protfolio(request, username=None):
    if request.method == 'GET':
        show_control_box = False
        try:
            user = get_object_or_404(User, username=username)
        except:
            user = request.user
        if request.user.is_authenticated and request.user == user.profile.user:
            show_control_box = True
        context = {'profile': user.profile,
                   'jobs': user.profile.jobs.all(),
                   'skills': user.profile.skills.all(),
                   'educations': user.profile.educations.all(),
                   'languages': user.profile.languages.all(),
                   'certificates': user.profile.certificates.all(),
                   'show_control_box': show_control_box}
        return render(request, 'Portfolio/Portfolio/detail.html', context)

# Create your views here.
