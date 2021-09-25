from django.contrib import admin
from django.db.models import Q
from import_export.admin import ImportExportModelAdmin

from Agah.models import Responder, Interviewer, Question, Survey, AnswerSheet, Option, Answer, BrandCategory, Brand

admin.site.site_header = 'نظرسنجی'
admin.site.site_title = 'نظرسنجی'
admin.site.index_title = ''


@admin.register(AnswerSheet)
class AnswerSheetCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'interviewer', 'responser', 'survey', 'number', 'date', 'total_point',
        'social_class',)

    class Meta:
        model = AnswerSheet
        fields = '__all__'


@admin.register(Interviewer)
class InterviewerCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'code',)

    class Meta:
        model = Interviewer
        fields = '__all__'


@admin.register(Responder)
class ResponderCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('firstname', 'mobile',)
    list_editable = ('mobile',)

    class Meta:
        model = Responder
        fields = '__all__'


@admin.register(Survey)
class SurveyCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title',)

    class Meta:
        model = Survey
        fields = '__all__'


@admin.register(Question)
class QuestionCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'survey', 'code', 'title', 'type', 'previous_question', 'next_question', 'has_other_in_options', 'is_required',
        'has_nothing_in_options',
        'min_input_value',
        'max_input_value')
    list_editable = ('type', 'previous_question', 'next_question', 'has_other_in_options', 'is_required',
                     'has_nothing_in_options',
                     'max_input_value',
                     'min_input_value')

    class Meta:
        model = Question
        fields = '__all__'


@admin.register(Option)
class OptionCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question', 'title', 'value', 'point',)

    class Meta:
        model = Option
        fields = '__all__'


@admin.register(Answer)
class AnswerCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('answersheet', 'question', 'option', 'answer', 'point',)
    search_fields = ['answersheet']

    class Meta:
        model = Answer
        fields = '__all__'

    def get_search_results(self, request, queryset, search_term):
        if search_term != '':
            return queryset.filter(Q(answersheet__responser__firstname__icontains=search_term) | Q(
                answersheet__responser__lastname__icontains=search_term)), True
        else:
            return queryset, False


@admin.register(BrandCategory)
class BrandCategoryCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title',)

    class Meta:
        model = BrandCategory
        fields = '__all__'


@admin.register(Brand)
class BrandCustom(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('category', 'title', 'value',)

    class Meta:
        model = Brand
        fields = '__all__'

# Register your models here.
