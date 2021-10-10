import django.forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Agah import forms
from Portfolio.models import Profile, Job, Skill, Education, Language, Certificate


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class DateInput(django.forms.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'marital_status', 'birthday', 'occupation', 'country', 'city', 'image', 'about_me', 'title',
                  'phone', 'address']
        widgets = {
            'birthday': DateInput()
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['profile']
        widgets = {
            'already_work': django.forms.CheckboxInput,
            'start_dte': DateInput(),
            'end_dte': DateInput(),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['profile']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['title', 'university', 'from_dte', 'to_dte', 'grade', 'degree']
        widgets = {
            'from_dte': DateInput(),
            'to_dte': DateInput(),
        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ['profile']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ['profile']
        widgets = {
            'date': DateInput(),
            'have_cert': django.forms.CheckboxInput
        }
