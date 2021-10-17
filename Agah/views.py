from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from Agah.forms import Question_from, Interviewer_form, Answersheet_from, Responser_form, Children_form, Main_form, \
    Main_form_M_series
from Agah.models import Question, Interviewer, Survey, Answer, AnswerSheet, Brand, BrandCategory, Option
from django.contrib import messages


@csrf_protect
def Personal(request):
    # GET
    if request.method == 'GET':
        questions = Question.objects.filter(code__startswith='S')
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
            S1 = save_single_answer('S1', S1, answersheet)
            # S2 save
            S2 = save_single_answer('S2', S2, answersheet)
            # S3 save
            S3 = save_single_answer('S3', S3, answersheet)
            # S4a save
            S4a = int(request.POST.get('S4a'))
            S4a = save_single_answer('S4a', S4a, answersheet)
            # S4b save
            S4b = save_single_answer('S4b', S4b, answersheet)
            # S5 save
            if S5 is not None:
                S5 = save_single_answer('S5', S5, answersheet)
            else:
                S5 = Question.objects.get(code='S5')
                if answersheet.answers.filter(question=S5).exists():
                    answersheet.answers.get(question=S5).delete()
            request.session['answersheet'] = answersheet.pk
            if int(request.POST.get('S4b')) == 1 and int(request.POST.get('S4a')) == 1:
                request.session['children'] = int(request.POST.get('S5', 0))
            else:
                try:
                    del request.session['number_of_children']
                except:
                    pass
            # Constrain check
            if S2.option is None:
                S2.option = Option.objects.get(pk=10)
                S2.save()
            if S1.option.value in [1, 2, 3] or S2.option.value not in [1, 2, 3, 4, 5] or (S3.answer in [1, 5] and (
                    S4b.option.value == 2 or (S4b.option.value == 1 and S5.answer == 0))):
                if answersheet:
                    del request.session['answersheet']
                messages.warning(request, 'خاتمه نظرسنجی')
                return redirect(reverse('personal'))

            answersheet.interviwer_category()
            request.session['answersheet'] = answersheet.pk
            if S5.answer:
                request.session['number_of_children'] = int(S5.answer)
                return redirect(reverse('children'))
            else:
                return redirect(reverse('main'))
        else:
            questions = Question.objects.filter(code__startswith='S')
            S1_frm = Question_from(instance=questions.get(code__iexact='S1'))
            S2_frm = Question_from(instance=questions.get(code__iexact='S2'))
            S3_frm = Question_from(instance=questions.get(code__iexact='S3'))
            S4a_frm = Question_from(instance=questions.get(code__iexact='S4a'))
            S4b_frm = Question_from(instance=questions.get(code__iexact='S4b'))
            S5_frm = Question_from(instance=questions.get(code__iexact='S5'))
            Interviewer_frm = Interviewer_form(request.POST)
            Answersheet_frm = Answersheet_from(request.POST)
            Responser_frm = Responser_form(request.POST)
            context = {'S1_frm': S1_frm, 'S2_frm': S2_frm, 'S3_frm': S3_frm, 'S4a_frm': S4a_frm, 'S4b_frm': S4b_frm,
                       'S5_frm': S5_frm, 'Interviewer_frm': Interviewer_frm,
                       'Answersheet_frm': Answersheet_frm, 'Responser_frm': Responser_frm, 'POST': True}
            return render(request, template_name='Agah/Personal.html', context=context)


def save_single_answer(question_code, user_answer, answersheet, override=True):
    if user_answer is not None:
        if override:
            question = Question.objects.get(code__iexact=question_code)
            try:
                option = question.options.get(pk=user_answer)
            except:
                if answersheet.answers.filter(question=question).exists():
                    answer = answersheet.answers.get(question=question)
                    answer.answer = user_answer
                    answer.option = None
                    answer.save()
                    return answer
                else:
                    answer = Answer(question=question, option=None, answersheet=answersheet, point=0,
                                    answer=user_answer)
                    answer.save()
                    return answer
            else:
                if answersheet.answers.filter(question=question).exists():
                    if answersheet.answers.get(question=question).option != option:
                        answer = answersheet.answers.get(question=question)
                        answer.option = option
                        # answer.answer = option.value
                        answer.point = 0
                        answer.save()
                        return answer
                    else:
                        return answersheet.answers.get(question=question)
                else:
                    answer = Answer(question=question, option=option, answersheet=answersheet, point=option.point)
                    answer.save()
                    return answer
        else:
            question = Question.objects.get(code__iexact=question_code)
            try:
                option = question.options.get(pk=user_answer)
            except:
                answer = Answer(question=question, option=None, answersheet=answersheet, point=0, answer=user_answer)
                answer.save()
                return answer
            else:
                answer = Answer(question=question, option=option, answersheet=answersheet, point=option.point)
                answer.save()
                return answer


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
        messages.warning(request, 'پرسشنامه فعال ندارید')
        return redirect(reverse('personal'))
    # GET
    if request.method == 'GET':
        number_of_children = request.session.get('number_of_children', False)
        show = False
        q_questions = Question.objects.filter(code__startswith='Q')[:3]
        context = {'Show': show}
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
            context['S6'] = question_S6
            context['S7'] = question_S7
            context['S8'] = question_S8
            context['S9'] = question_S9
            context['S10'] = question_S10
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

        for i in range(1, request.session['number_of_children'] + 1):
            save_single_answer(question_S6, request.POST.get(f'S6_{i}'), answersheet, False)
            save_single_answer(question_S7, request.POST.get(f'S7_{i}'), answersheet, False)
            save_single_answer(question_S8, request.POST.get(f'S8_{i}'), answersheet, False)
            save_single_answer(question_S9, request.POST.get(f'S9_{i}_1'), answersheet, False)
            save_single_answer(question_S9, request.POST.get(f'S9_{i}_2'), answersheet, False)
            save_single_answer(question_S10, request.POST.get(f'S10_{i}'), answersheet, False)
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
        messages.warning(request, 'پرسشنامه فعال ندارید')
        return redirect(reverse('personal'))
    questions = Question.objects.filter(code__startswith='Q')
    Q1 = questions[0]
    Q2 = Q1.next_question
    Q3 = Q2.next_question
    Q4 = Q3.next_question
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
        # show q questions...
        Q_forms = []
        brands_cats = BrandCategory.objects.all()
        for i in range(1, 12):
            ins = {'Q1': Q1, 'Q2': Q2, 'Q3': Q3, 'Q4': Q4, 'Q4a': Q4a, 'Q5': Q5, 'Q6': Q6, 'Q7': Q7, 'Q8': Q8, 'Q9': Q9,
                   'row': i,
                   'brands_cat': brands_cats[i - 1]}
            Q_forms.append(Main_form(instance=ins))
        context['Q_forms'] = Q_forms
        context['Q_questions'] = {'Q1': Q1, 'Q2': Q2, 'Q3': Q3, 'Q4': Q4, 'Q4a': Q4a, 'Q5': Q5, 'Q6': Q6, 'Q7': Q7,
                                  'Q8': Q8, 'Q9': Q9}

        # show m questions
        M2_form = Question_from(instance=M2)
        M3_form = Question_from(instance=M3)
        context['M_forms'] = [M2_form, M3_form]
        context['M1'] = M1
        context['M1_form'] = Main_form_M_series()
        return render(request, 'Agah/Main.html', context)


    # POST
    else:
        # get answers...
        Q1_answer = request.POST.getlist('Q1')
        Q2_answer = request.POST.getlist('Q2')
        Q3_answer = request.POST.getlist('Q3')
        Q4_answer = request.POST.getlist('Q4')
        Q4a_answer = request.POST.getlist('Q4a')
        Q5_answer = request.POST.getlist('Q5')
        Q6_answer = request.POST.getlist('Q6')
        Q7_answer = request.POST.getlist('Q7')
        Q8_answer = request.POST.getlist('Q8')
        Q9_answer = request.POST.getlist('Q9')


        # save Q1
        save_list_answer(Q1, Q1_answer, answersheet)
        # save Q2
        save_list_answer(Q2, Q2_answer, answersheet)
        # save Q3
        save_list_answer(Q3, Q3_answer, answersheet)


        # save Q4
        save_list_answer(Q4, Q4_answer, answersheet)
        # save Q4a
        save_list_answer(Q4a, Q4a_answer, answersheet)
        # save Q5
        save_list_answer(Q5, Q5_answer, answersheet)
        # save Q6
        save_list_answer(Q6, Q6_answer, answersheet)
        # save Q7
        save_list_answer(Q7, Q7_answer, answersheet)
        # save Q8
        save_list_answer(Q8, Q8_answer, answersheet, False)
        # save Q9
        save_list_answer(Q9, Q9_answer, answersheet, False)
        # save M1
        M1_form_1_answer = request.POST.get('M1_form_1')
        answer = Answer(question=M1, answersheet=answersheet, answer=M1_form_1_answer, point=0,
                        option=M1.options.get(value=int(1)))
        answer.save()
        M1_form_2_answer = request.POST.get('M1_form_2')
        answer = Answer(question=M1, answersheet=answersheet, answer=M1_form_2_answer, point=0,
                        option=M1.options.get(value
                                              =int(2)))
        answer.save()
        # save_single_answer(M1, M1_form_1_answer, answersheet,False)
        # save_single_answer(M1, M1_form_2_answer, answersheet,False)
        # save M2
        M2_answer = request.POST.get('M2')
        save_single_answer(M2, M2_answer, answersheet)
        # save M3
        M3_answer = request.POST.get('M3')
        save_single_answer(M3, M3_answer, answersheet)
        messages.success(request, message='پرسشنامه با موفقیت ثبت شد')
        # request.session.flush()
        return redirect(reverse('personal'))


def save_list_answer(question, user_answer, answersheet, brand=True):
    # category = BrandCategory.objects.all()[:10]
    batch_size = len(user_answer)
    list_answer = []
    for i in range(len(user_answer)):
        if brand:
            list_answer.append(Answer(question=question, answersheet=answersheet, point=0,
                                      brand=Brand.objects.get(pk=int(user_answer[i]))))
        else:
            option = question.options.get(pk=user_answer[i])
            list_answer.append(Answer(question=question, answersheet=answersheet, option=option, point=0))

    bulk = Answer.objects.bulk_create(list_answer, batch_size)

# Create your views here.
