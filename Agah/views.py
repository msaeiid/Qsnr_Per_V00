from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from Agah.forms import Question_from, Interviewer_form, Answersheet_from, Responser_form, Children_form
from Agah.models import Question, Interviewer, Survey, Answer, AnswerSheet


@csrf_protect
def Personal(request):
    # GET
    if request.method == 'GET':
        questions = Question.objects.filter(code__startswith='s')
        S1_frm = Question_from(instance=questions.get(code__iexact='S1'))
        S2_frm = Question_from(instance=questions.get(code__iexact='S2'))
        S3_frm = Question_from(instance=questions.get(code__iexact='S3'))
        S4a_frm = Question_from(instance=questions.get(code__iexact='S4a'))
        S4b_frm = Question_from(instance=questions.get(code__iexact='S4b'))
        S5_frm = Question_from(instance=questions.get(code__iexact='S5'))
        Interviewer_frm = Interviewer_form(request.GET)
        Answersheet_frm = Answersheet_from(request.GET)
        Responser_frm = Responser_form(request.GET)
        context = {'S1_frm': S1_frm, 'S2_frm': S2_frm, 'S3_frm': S3_frm, 'S4a_frm': S4a_frm, 'S4b_frm': S4b_frm,
                   'S5_frm': S5_frm, 'Interviewer_frm': Interviewer_frm,
                   'Answersheet_frm': Answersheet_frm, 'Responser_frm': Responser_frm}
        return render(request, template_name='Agah/Personal.html', context=context)
    # POST
    else:
        # answersheet exist
        answersheet_pk = request.session.get('answersheet', False)
        if answersheet_pk:
            answersheet = AnswerSheet.objects.get(pk=answersheet_pk)
        else:
            answersheet = False
        # generate forms
        Interviewer_frm = Interviewer_form(request.POST)
        Answersheet_frm = Answersheet_from(request.POST)
        Responser_frm = Responser_form(request.POST)

        # check for some validation...
        if Interviewer_frm.is_valid() and Answersheet_frm.is_valid() and Responser_frm.is_valid():
            S1 = int(request.POST.get('S1', None))
            S2 = int(request.POST.get('S2', None))
            S3 = get_age_category(int(request.POST.get('S3', None)))
            S4b = int(request.POST.get('S4b', None))
            S5 = int(request.POST.get('S5', 0))
            if S1 in [1, 2, 3] or S2 == 0 or (S3 in [1, 5] and (S4b == 2 or (S4b == 1 and S5 == 0))):
                if answersheet:
                    answersheet.delete()
                    answersheet.responser.delete()
                    request.session.flush()
                raise ValueError('خاتمه نظرسنجی GENERAL')

            # save or update responser data
            if answersheet:
                # update firstname
                if answersheet.responser.firstname != Responser_frm.cleaned_data.get('firstname'):
                    answersheet.responser.firstname = Responser_frm.cleaned_data.get('firstname')
                    answersheet.responser.save()
                # update mobile
                if answersheet.responser.mobile != Responser_frm.cleaned_data.get('mobile'):
                    answersheet.responser.mobile = Responser_frm.cleaned_data.get('mobile')
                    answersheet.responser.save()
                # update address
                if answersheet.responser.address != Responser_frm.cleaned_data.get('address'):
                    answersheet.responser.address = Responser_frm.cleaned_data.get('address')
                    answersheet.responser.save()
            else:
                responder = Responser_frm.save()

            # save or update interviewer code
            if answersheet:
                if answersheet.interviewer.code != Interviewer_frm.cleaned_data.get('code'):
                    answersheet.interviewer = Interviewer.objects.get(code=Interviewer_frm.cleaned_data.get('code'))
                    answersheet.save()
            else:
                interviewer = Interviewer.objects.get(code=Interviewer_frm.cleaned_data.get('code'))

            # save or update answersheet data
            if answersheet:
                # update date
                import jdatetime
                new_date = jdatetime.date(1400, 6, Answersheet_frm.cleaned_data.get('day')).togregorian()
                if answersheet.date != new_date:
                    answersheet.date = new_date
                    answersheet.save()
                if answersheet.number != Answersheet_frm.cleaned_data.get('number'):
                    answersheet.number = Answersheet_frm.cleaned_data.get('number')
                    answersheet.save()
            else:
                answersheet = Answersheet_frm.save(commit=False)
                answersheet.responser = responder
                answersheet.interviewer = interviewer
                answersheet.survey = Survey.objects.get(title__iexact='Qsnr_Per_V00')
                import jdatetime
                answersheet.date = jdatetime.date(1400, 6, Answersheet_frm.cleaned_data.get('day')).togregorian()
                answersheet.save()

            # S1 save
            save_single_answer('S1', int(request.POST.get('S1')), answersheet)
            # S2 save
            save_single_answer('S2', int(request.POST.get('S2')), answersheet)
            # S3 save
            save_single_answer('S3', get_age_category(int(request.POST.get('S3'))), answersheet)
            # S4a save
            save_single_answer('S4a', int(request.POST.get('S4a')), answersheet)
            # S4b save
            save_single_answer('S4b', int(request.POST.get('S4b')), answersheet)
            # S5 save
            if request.POST.get('S5') is not None:
                save_single_answer('S5', int(request.POST.get('S5')), answersheet)
            else:
                S5 = Question.objects.get(code='S5')
                if answersheet.answers.filter(question=S5).exists():
                    answersheet.answers.get(question=S5).delete()
            request.session['answersheet'] = answersheet.pk
            if int(request.POST.get('S4b')) == 1 and int(request.POST.get('S4a')) == 1:
                request.session['children'] = int(request.POST.get('S5'))
            else:
                try:
                    del request.session['children']
                except:
                    pass
            return redirect(reverse('children'))
        else:
            context = {'Interviewer_frm': Interviewer_frm, 'Answersheet_frm': Answersheet_frm,
                       'Responser_frm': Responser_frm}
            return render(request, 'Agah/Personal.html', )
        pass


def save_single_answer(question_code, user_answer, answersheet, override=True):
    if override:
        question = Question.objects.get(code__iexact=question_code)
        try:
            option = question.options.get(value=user_answer)
        except:
            if answersheet.answers.filter(question=question).exists():
                answer = answersheet.answers.get(question=question)
                answer.answer = user_answer
                answer.save()
            else:
                answer = Answer(question=question, option=None, answersheet=answersheet, point=0, answer=user_answer)
                answer.save()
        else:
            if answersheet.answers.filter(question=question).exists():
                if answersheet.answers.get(question=question).option != option:
                    answer = answersheet.answers.get(question=question)
                    answer.option = option
                    answer.answer = option.value
                    answer.point = option.point
                    answer.save()
            else:
                answer = Answer(question=question, option=option, answersheet=answersheet, point=option.point,
                                answer=option.value)
                answer.save()
    else:
        question = Question.objects.get(code__iexact=question_code)
        try:
            option = question.options.get(value=user_answer)
        except:
            answer = Answer(question=question, option=None, answersheet=answersheet, point=0, answer=user_answer)
            answer.save()
        else:
            answer = Answer(question=question, option=option, answersheet=answersheet, point=option.point,
                            answer=option.value)
            answer.save()


def get_age_category(age):
    import jdatetime
    age = jdatetime.datetime.now().year - (age + 1300)
    if age <= 15:
        return 1
    elif 16 <= age <= 25:
        return 2
    elif 26 <= age <= 35:
        return 3
    elif 36 <= age <= 45:
        return 4
    elif 46 <= age:
        return 5


@csrf_protect
def Children(request):
    # GET
    if request.method == 'GET':
        number_of_children = request.session.get('children', False)
        if not number_of_children:
            return redirect(reverse('question'))
        questions = Question.objects.filter(code__startswith='s')
        S6 = questions.get(code='S6')
        S7 = questions.get(code='S7')
        S8 = questions.get(code='S8')
        S9 = questions.get(code='S9')
        S10 = questions.get(code='S10')
        forms = []
        for i in range(1, number_of_children + 1):
            ins = {'S6': S6, 'S7': S7, 'S8': S8, 'S9': S9, 'S10': S10, 'row': i}
            form = Children_form(request.GET, instance=ins)
            forms.append(form)
        context = {'forms': forms}
        return render(request, 'Agah/Childern.html', context)
    # POST
    else:
        answersheet = get_object_or_404(AnswerSheet, pk=request.session.get('answersheet'))
        question_S6 = Question.objects.get(code='S6')
        question_S7 = Question.objects.get(code='S7')
        question_S8 = Question.objects.get(code='S8')
        question_S9 = Question.objects.get(code='S9')
        question_S10 = Question.objects.get(code='S10')
        if answersheet.answers.filter(question=question_S6).exists():
            answersheet.answers.filter(question=question_S6).delete()

        if answersheet.answers.filter(question=question_S7).exists():
            answersheet.answers.filter(question=question_S7).delete()

        if answersheet.answers.filter(question=question_S8).exists():
            answersheet.answers.filter(question=question_S8).delete()

        if answersheet.answers.filter(question=question_S9).exists():
            answersheet.answers.filter(question=question_S9).delete()

        if answersheet.answers.filter(question=question_S10).exists():
            answersheet.answers.filter(question=question_S10).delete()

        for i in range(1, request.session['children'] + 1):
            save_single_answer(question_S6, request.POST.get(f'S6_{i}'), answersheet, False)
            save_single_answer(question_S7, request.POST.get(f'S7_{i}'), answersheet, False)
            save_single_answer(question_S8, request.POST.get(f'S8_{i}'), answersheet, False)
            save_single_answer(question_S9, request.POST.get(f'S9_{i}'), answersheet, False)
            save_single_answer(question_S10, request.POST.get(f'S10_{i}'), answersheet, False)
        return redirect(reverse('question'))


def Question_view(request):
    print('')
    pass

# Create your views here.
