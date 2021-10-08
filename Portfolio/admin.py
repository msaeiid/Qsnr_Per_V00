from django.contrib import admin

from Portfolio.models import Profile, Job, Skill, Education, Language, Certificate, Portfolio

admin.site.site_header = 'Portfolio'
admin.site.site_title = 'Portfolio'
admin.site.index_title = 'Portfolio'


@admin.register(Profile)
class Profile_Custom(admin.ModelAdmin):
    fields = ('gender', 'marital_status', 'birthday', 'occupation', 'country', 'city', 'image', 'about_me', 'title',
              'phone', 'address')


@admin.register(Job)
class Job_Custom(admin.ModelAdmin):
    fields = ('profile', 'title', 'company', 'start_dte', 'end_dte', 'already_work', 'description')


@admin.register(Skill)
class Skill_Custom(admin.ModelAdmin):
    fields = ('profile', 'title', 'point', 'description')


@admin.register(Education)
class Education_Custom(admin.ModelAdmin):
    fields = ('profile', 'title', 'university', 'from_dte', 'to_dte', 'grade', 'degree')


@admin.register(Language)
class Language_Custom(admin.ModelAdmin):
    fields = ('profile', 'title', 'point', 'description')


@admin.register(Certificate)
class Certificate_Custom(admin.ModelAdmin):
    fields = ('profile', 'title', 'date', 'have_cert', 'image', 'authorized_by', 'url')


@admin.register(Portfolio)
class Portfolio_Custom(admin.ModelAdmin):
    fields = ('language',)

# Register your models here.
