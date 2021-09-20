from django.contrib import admin
from django.db.models import Q

from Agah.models import Responder, Interviewer, Question, Survey, AnswerSheet, Option, Answer, \
    Child, Limit, BrandCategory, Brand

admin.site.site_header = 'نظرسنجی'
admin.site.site_title = 'نظرسنجی'
admin.site.index_title = ''


class AnswerSheetCustom(admin.ModelAdmin):
    list_display = (
        'interviewer', 'responser', 'survey','number', 'date', 'total_point',
        'social_class',)


class InterviewerCustom(admin.ModelAdmin):
    list_display = ('name', 'code',)


class ResponderCustom(admin.ModelAdmin):
    list_display = ('firstname', 'mobile',)
    list_editable = ('mobile',)


class SurveyCustom(admin.ModelAdmin):
    list_display = ('title',)


class QuestionCustom(admin.ModelAdmin):
    list_display = (
        'survey', 'code', 'title', 'type', 'previous_question', 'next_question', 'has_other_in_options', 'is_required',
        'has_nothing_in_options',
        'max_input_value',
        'min_input_value')
    list_editable = ('type', 'previous_question', 'next_question', 'has_other_in_options', 'is_required',
                     'has_nothing_in_options',
                     'max_input_value',
                     'min_input_value')


class OptionCustom(admin.ModelAdmin):
    list_display = ('question', 'title', 'value', 'point',)


class AnswerCustom(admin.ModelAdmin):
    list_display = ('answersheet', 'question', 'option', 'answer', 'point',)
    search_fields = ['answersheet']

    def get_search_results(self, request, queryset, search_term):
        if search_term != '':
            return queryset.filter(Q(answersheet__responser__firstname__icontains=search_term) | Q(
                answersheet__responser__lastname__icontains=search_term)), True
        else:
            return queryset, False


class ChildCustom(admin.ModelAdmin):
    list_display = ('responder', 'gender', 'birthday_year',)


class LimitCustom(admin.ModelAdmin):
    list_display = ('marital_status', 'age', 'maximum', 'capacity',)


class BrandCategoryCustom(admin.ModelAdmin):
    list_display = ('title',)


class BrandCustom(admin.ModelAdmin):
    list_display = ('category', 'title', 'value',)


admin.site.register(Interviewer, InterviewerCustom)
admin.site.register(Responder, ResponderCustom)
admin.site.register(Survey, SurveyCustom)
admin.site.register(Question, QuestionCustom)
admin.site.register(AnswerSheet, AnswerSheetCustom)
admin.site.register(Option, OptionCustom)
admin.site.register(Answer, AnswerCustom)
admin.site.register(Child, ChildCustom)
admin.site.register(Limit, LimitCustom)
admin.site.register(BrandCategory, BrandCategoryCustom)
admin.site.register(Brand, BrandCustom)

# Register your models here.
