from django import forms
from django.forms import ModelForm
from Agah.models import Responder, Interviewer, AnswerSheet


def choice_maker(question):
    options = [('', '')]
    for item in question.options.all():
        options.append((item.value, item.title))
    if question.has_other_in_options:
        options.append((0, 'سایر'))
    if question.has_nothing_in_options:
        options.append((4, 'هیچکدام'))
    return options


class Question_from(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Question_from, self).__init__()
        question = kwargs.get('instance')
        self.fields[question.code] = option_maker(question, question.code)


class Responser_form(ModelForm):
    class Meta:
        model = Responder
        fields = '__all__'


class Interviewer_form(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ('code',)

    def clean(self):
        cleaned_data = {'code': self.data.get('code')}
        code = cleaned_data.get('code')
        try:
            code = int(code)
        except:
            raise ValueError('برای فیلد کدپرسشگر از عدد استفاده نمایید')
        search = Interviewer.objects.filter(code=int(code))
        if len(search) != 1:
            raise ValueError('کدپرسشگر وارد شده نامعتبر است')
        return cleaned_data


class Answersheet_from(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ('number',)

    day = forms.IntegerField(label='تاریخ شمسی', min_value=0, max_value=31)


class Children_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Children_form, self).__init__()
        row = kwargs.get('instance').get('row')
        S6 = kwargs.get('instance').get('S6')
        S7 = kwargs.get('instance').get('S7')
        S8 = kwargs.get('instance').get('S8')
        S9 = kwargs.get('instance').get('S9')
        S10 = kwargs.get('instance').get('S10')
        self.fields[f'{row}'] = forms.CharField(widget=forms.TextInput(attrs={'disabled': True, 'value': f'{row}'}))
        self.fields[f'S6_{row}'] = option_maker(S6, f'{row}')
        self.fields[f'S7_{row}'] = option_maker(S7, f'{row} birthday')
        self.fields[f'S8_{row}'] = option_maker(S8, f'{row} option')
        state = 1
        self.fields[f'S9_{row}_{state}'] = option_maker(S9, f'{row} option')
        self.fields[f'S9_{row}_{state + 1}'] = option_maker(S9, f'{row} option')
        self.fields[f'S10_{row}'] = option_maker(S10, f'{row} option')


def option_maker(question, class_html):
    # Int
    if question.type == 'IntegerField':
        return forms.CharField(label=f'{question.code} {question.title}', widget=forms.TextInput(
            attrs={'type': 'number', 'required': question.is_required, 'min': question.min_input_value,
                   'max': question.max_input_value, 'class': class_html}))
    # Text
    if question.type == 'CharField':
        return forms.CharField(required=question.is_required,
                               max_length=question.max_input_value,
                               label=f'{question.code} {question.title}')
    # Drop down
    if question.type == 'ChoiceField':
        return forms.ChoiceField(required=question.is_required,
                                 choices=choice_maker(question),
                                 label=f'{question.code} {question.title}',
                                 widget=forms.Select(attrs={'class': class_html}))
    # Radio button
    if question.type == 'RadioSelect':
        return forms.ChoiceField(required=question.is_required,
                                 choices=choice_maker(question),
                                 label=f'{question.code} {question.title}',
                                 widget=forms.RadioSelect(attrs={'class': class_html}))
    # Check box
    if question.type == 'MultipleChoiceField':
        return forms.ChoiceField(required=question.is_required,
                                 choices=choice_maker(question),
                                 label=question.title, widget=forms.CheckboxSelectMultiple(attrs={'class': class_html}))
