from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from Agah.forms import Question_from, Interviewer_form, Answersheet_from, Responser_form, Children_form, Main_form, \
    Main_form_M_series
from Agah.models import Question, Interviewer, Survey, Answer, AnswerSheet, Brand, BrandCategory


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
            try:
                answersheet = AnswerSheet.objects.get(pk=answersheet_pk)
            except:
                answersheet = False
        else:
            answersheet = False
        # generate forms
        Interviewer_frm = Interviewer_form(request.POST)
        Answersheet_frm = Answersheet_from(request.POST)
        Responser_frm = Responser_form(request.POST)

        # check for some validation...
        if Interviewer_frm.is_valid() and Answersheet_frm.is_valid() and Responser_frm.is_valid():
            S1 = int(request.POST.get('S1', None))
            try:
                S2 = int(request.POST.get('S2', None))
            except ValueError:
                S2 = request.POST.get('S2', None)
            S3 = get_age_category(int(request.POST.get('S3', None)))
            S4b = int(request.POST.get('S4b', None))
            S5 = int(request.POST.get('S5', 0))
            if S1 in [1, 2, 3] or S2 not in [1, 2, 3, 4, 5] or (S3 in [1, 5] and (S4b == 2 or (S4b == 1 and S5 == 0))):
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
            save_single_answer('S1', S1, answersheet)
            # S2 save
            save_single_answer('S2', S2, answersheet)
            # S3 save
            save_single_answer('S3', S3, answersheet)
            # S4a save
            S4a = int(request.POST.get('S4a'))
            save_single_answer('S4a', S4a, answersheet)
            # S4b save
            save_single_answer('S4b', S4b, answersheet)
            # S5 save
            if S5 is not None:
                save_single_answer('S5', S5, answersheet)
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
            answersheet.interviwer_category()
            request.session['answersheet'] = answersheet.pk
            request.session['number_of_children'] = int(S5)
            return redirect(reverse('children'))
        else:
            context = {'Interviewer_frm': Interviewer_frm, 'Answersheet_frm': Answersheet_frm,
                       'Responser_frm': Responser_frm}
            return render(request, 'Agah/Personal.html', )


def save_single_answer(question_code, user_answer, answersheet, override=True):
    if override:
        question = Question.objects.get(code__iexact=question_code)
        try:
            option = question.options.get(value=user_answer)
        except:
            if answersheet.answers.filter(question=question).exists():
                answer = answersheet.answers.get(question=question)
                answer.answer = user_answer
                answer.option = None
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
    question_S6 = Question.objects.get(code='S6')
    question_S7 = Question.objects.get(code='S7')
    question_S8 = Question.objects.get(code='S8')
    question_S9 = Question.objects.get(code='S9')
    question_S10 = Question.objects.get(code='S10')
    answersheet = request.session.get('answersheet')
    try:
        answersheet = AnswerSheet.objects.get(pk=answersheet)
    except:
        return redirect(reverse('personal'))
    # GET
    if request.method == 'GET':
        number_of_children = request.session.get('children', False)
        show = False
        q_questions = Question.objects.filter(code__startswith='Q')[:3]
        q_forms = []
        for q in q_questions:
            q_forms.append(Question_from(instance=q))
        context = {'q_forms': q_forms, 'Show': show}
        if number_of_children > 0 and number_of_children is not None:
            show = True
            # return redirect(reverse('main'))
            questions = Question.objects.filter(code__startswith='s')
            forms = []
            for i in range(1, number_of_children + 1):
                ins = {'S6': question_S6, 'S7': question_S7, 'S8': question_S8, 'S9': question_S9, 'S10': question_S10,
                       'row': i}
                form = Children_form(request.GET, instance=ins)
                forms.append(form)
            context['forms'] = forms
            context['Show'] = show
        return render(request, 'Agah/Childern.html', context)
    # POST
    else:
        answersheet = get_object_or_404(AnswerSheet, pk=request.session.get('answersheet'))
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
            save_single_answer(question_S9, request.POST.get(f'S9_{i}_1'), answersheet, False)
            save_single_answer(question_S9, request.POST.get(f'S9_{i}_2'), answersheet, False)
            save_single_answer(question_S10, request.POST.get(f'S10_{i}'), answersheet, False)
        q_questions = Question.objects.filter(code__startswith='Q')[:3]
        question_Q1 = q_questions[0]
        question_Q2 = q_questions[1]
        question_Q3 = q_questions[2]
        q1_answer = int(request.POST.get('Q1'))
        q2_answer = int(request.POST.get('Q2'))
        q3_answer = int(request.POST.get('Q3'))
        # save or update Q1 answer
        save_single_answer(question_Q1, q1_answer, answersheet, True)
        # save or update Q2 answer
        save_single_answer(question_Q2, q2_answer, answersheet, True)
        # save or update Q3 answer
        save_single_answer(question_Q3, q3_answer, answersheet, True)
        return redirect(reverse('main'))


@csrf_protect
def Main_view(request):
    # fetch question
    m_questions = Question.objects.filter(code__startswith='M')
    M1 = m_questions[0]
    M2 = m_questions[1]
    M3 = m_questions[2]
    context = {}
    # fetch Q question
    answersheet = request.session.get('answersheet')
    try:
        answersheet = AnswerSheet.objects.get(pk=answersheet)
    except:
        return redirect(reverse('personal'))
    Q1_status = int(answersheet.answers.get(question__code='Q1').answer) == 1
    Q2_status = int(answersheet.answers.get(question__code='Q2').answer) == 1
    Q3_status = int(answersheet.answers.get(question__code='Q3').answer) == 1
    if all([Q1_status, Q2_status, Q3_status]):
        questions = Question.objects.filter(code__startswith='Q')[3:]
        Q4 = questions[0]
        Q4a = Q4.next_question
        Q5 = Q4a.next_question
        Q6 = Q5.next_question
        Q7 = Q6.next_question
        Q8 = Q7.next_question
        Q9 = Q8.next_question
    # GET
    if request.method == 'GET':
        rest = False
        context = {}
        # show rest of q questions...
        if all([Q1_status, Q2_status, Q3_status]):
            Q_forms = []
            brands_cats = BrandCategory.objects.all()
            for i in range(1, 12):
                ins = {'Q4': Q4, 'Q4a': Q4a, 'Q5': Q5, 'Q6': Q6, 'Q7': Q7, 'Q8': Q8, 'Q9': Q9, 'row': i,
                       'brands_cat': brands_cats[i - 1]}
                Q_forms.append(Main_form(instance=ins))
                pass
            rest = True
            context['Q_forms'] = Q_forms
            context['Q_questions'] = [f'{Q4.code} {Q4.title}', f'{Q4a.code} {Q4a.title}', f'{Q5.code} {Q5.title}',
                                      f'{Q6.code} {Q6.title}', f'{Q7.code} {Q7.title}', f'{Q8.code} {Q8.title}',
                                      f'{Q9.code} {Q9.title}']

        # show m questions
        M2_form = Question_from(instance=M2)
        M3_form = Question_from(instance=M3)
        context['M_forms'] = [M2_form, M3_form]
        context['M1'] = M1
        context['M1_form'] = Main_form_M_series()
        context['Rest'] = rest
        return render(request, 'Agah/Main.html', context)


    # POST
    else:
        # show rest of q questions...
        if all([Q1_status, Q2_status, Q3_status]):
            pass

# Create your views here.
