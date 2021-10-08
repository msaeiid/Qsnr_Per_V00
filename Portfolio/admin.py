from django.contrib import admin

from Portfolio.models import Profile, Job, Skill, Education, Language, Certificate

admin.site.site_header = 'Portfolio'
admin.site.site_title = 'Portfolio'
admin.site.index_title = 'Portfolio'


@admin.register(Profile)
class ProfileCustom(admin.ModelAdmin):
    fields = ('gender', 'marital_status', 'birthday', 'occupation', 'country', 'city', 'image', 'about_me', 'title',
              'phone', 'address')


@admin.register(Job)
class JobCustom(admin.ModelAdmin):
    fields = ('profile', 'title', 'company', 'start_dte', 'end_dte', 'already_work', 'description')


@admin.register(Skill)
class SkillCustom(admin.ModelAdmin):
    fields = ('profile', 'title', 'point', 'description')


@admin.register(Education)
class EducationCustom(admin.ModelAdmin):
    fields = ('profile', 'title', 'university', 'from_dte', 'to_dte', 'grade', 'degree')


@admin.register(Language)
class LanguageCustom(admin.ModelAdmin):
    fields = ('profile', 'title', 'point', 'description')


@admin.register(Certificate)
class CertificateCustom(admin.ModelAdmin):
    fields = ('profile', 'title', 'date', 'have_cert', 'image', 'authorized_by', 'url')

# Register your models here.
