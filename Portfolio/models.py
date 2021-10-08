from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    Male = 1
    Female = 2
    gender_choice = ((Male, 'Male'),
                     (Female, 'Female'))
    gender = models.IntegerField(choices=gender_choice, verbose_name='Gender', blank=True, editable=True, null=True)
    single = 1
    married = 2
    marital_choice = (
        (single, 'Single'),
        (married, 'Married'))
    marital_status = models.IntegerField(choices=marital_choice, blank=True, editable=True, null=True)
    birthday = models.DateField(verbose_name='Birthday', blank=True, editable=True, null=True)
    occupation = models.CharField(verbose_name='Occupation', max_length=200, blank=True, editable=True, null=True)
    country = models.CharField(verbose_name='Country', max_length=100, blank=True, editable=True, null=True)
    city = models.CharField(verbose_name='City', max_length=100, blank=True, editable=True, null=True)
    image = models.ImageField(verbose_name='Image', blank=True, editable=True, null=True)
    about_me = models.TextField(verbose_name='About me', blank=True, editable=True, null=True)
    title = models.CharField(verbose_name='Title', max_length=150, blank=True, editable=True, null=True)
    phone = models.CharField(verbose_name='Phone number', max_length=11, blank=True, editable=True, null=True)
    address = models.TextField(verbose_name='Address', blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.user.username}'


class Job(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, editable=True, null=True)
    company = models.CharField(verbose_name='Company', max_length=100, blank=True, editable=True, null=True)
    start_dte = models.DateField(verbose_name='From', blank=True, editable=True, null=True)
    end_dte = models.DateField(verbose_name='To', blank=True, editable=True, null=True)
    already_work = models.BooleanField(verbose_name='I already work', default=False, blank=True, editable=True,
                                       null=True)
    description = models.TextField('Description', blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.portfolio.profile.user.username} {self.title}'


class Skill(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, editable=True, null=True)

    point = models.IntegerField(verbose_name='How much you know about it',
                                validators=[MaxValueValidator(100), MinValueValidator(1)])
    description = models.TextField(verbose_name='Description', blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.portfolio.profile.user.username} {self.title}'


class Education(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='educations')
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, editable=True, null=True)
    university = models.CharField(verbose_name='University', max_length=200, blank=True, editable=True, null=True)
    from_dte = models.DateField(verbose_name='From', blank=True, editable=True, null=True)
    to_dte = models.DateField(verbose_name='To', blank=True, editable=True, null=True)
    grade = models.FloatField(verbose_name='Average', blank=True, editable=True, null=True)
    Diploma = 1
    Associate = 2
    Bachelor = 3
    Master = 4
    Doctoral = 5
    PostDoc = 6
    degree_choice = (
        (Diploma, 'Diploma'),
        (Associate, 'Associate'),
        (Bachelor, 'Bachelor'),
        (Master, 'Master'),
        (Doctoral, 'Doctoral'),
        (PostDoc, 'Post-Doc')
    )
    degree = models.IntegerField(verbose_name='Degree', choices=degree_choice, blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.portfolio.profile.user.username} {self.title}'


class Language(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='languages')
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, editable=True, null=True)
    point = models.IntegerField(verbose_name='How much you know about it',
                                validators=[MaxValueValidator(100), MinValueValidator(1)])
    description = models.TextField(verbose_name='Description', blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.portfolio.profile.user.username} {self.title}'


class Certificate(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, editable=True, null=True)
    date = models.DateField(verbose_name='Date', blank=True, editable=True, null=True)
    have_cert = models.BooleanField(verbose_name='Do you have certificate?', default=False, blank=True, editable=True,
                                    null=True)
    image = models.ImageField(verbose_name='Image', blank=True, editable=True, null=True)
    authorized_by = models.CharField(verbose_name='Authorized by', max_length=200, blank=True, editable=True, null=True)
    url = models.URLField(verbose_name='Certificate Url', blank=True, editable=True, null=True)

    def __str__(self):
        return f'{self.portfolio.profile.user.username} {self.title}'

    # Create your models here.
