from django.core.validators import RegexValidator
from django.db import models


class Interviewer(models.Model):
    '''
    پرسشگر
    '''

    class Meta:
        verbose_name = 'پرسشگر'
        verbose_name_plural = 'پرسشگر'

    code = models.CharField(verbose_name='کد پرسشگر', primary_key=True, unique=True, blank=False, null=False,
                            editable=True, max_length=5, validators=[
            RegexValidator(regex='^[0-9]{5}$', message='تعداد ارقام میبایست حداقل و حداکثر 5 رقم باشند')])
    name = models.CharField(verbose_name='نام پرسشگر', max_length=100, blank=False, editable=True, null=False,
                            validators=[RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                       message='لطفا از زبان فارسی استفاده نمایید')])

    def __str__(self):
        return self.name


class Responder(models.Model):
    '''
    پاسخگو
    '''

    class Meta:
        verbose_name = 'پاسخگو'
        verbose_name_plural = 'پاسخگو'

    firstname = models.CharField(verbose_name='نام پاسخگو', max_length=100, editable=True, blank=False, null=False,
                                 validators=[RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                            message='لطفا از زبان فارسی استفاده نمایید')])
    mobile = models.CharField(verbose_name='تلفن تماس پاسخگو', max_length=11, blank=False, null=False, editable=True,
                              validators=[
                                  RegexValidator(regex='^09[0-9]{9}$',
                                                 message='لطفا شماره موبایل را به صورت کامل وارد نمایید')])
    address = models.TextField(verbose_name='آدرس')

    def __str__(self):
        return f'{self.firstname}'


class Child(models.Model):
    class Meta:
        verbose_name = 'فرزند'
        verbose_name_plural = 'فرزند'
        ordering = ['pk']

    responder = models.ForeignKey(to=Responder, on_delete=models.CASCADE, verbose_name='پاسخگو',
                                  related_name='children')
    gender = models.ForeignKey(verbose_name='جنسیت', blank=False, null=False, editable=True, to='Option',
                               on_delete=models.PROTECT)
    birthday_year = models.IntegerField(verbose_name='سال تولد', blank=False, null=False, editable=True, validators=[
        RegexValidator(regex='^1[0-9]{3}$', message='لطفا سال تولد را صحیح و کامل وارد نمایید')])
    age = models.IntegerField(verbose_name='محسابه سن اتومات', blank=False, null=False, editable=True, )

    def __str__(self):
        return f' فرزندان ' \
               f'{self.responder.firstname}'


class Survey(models.Model):
    '''
    پرسشنامه
    '''

    class Meta:
        verbose_name = 'پرسشنامه'
        verbose_name_plural = 'پرسشنامه'

    title = models.CharField(verbose_name='عنوان', max_length=20)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    '''
    سوالات
    '''

    class Meta:
        verbose_name = 'پرسش'
        verbose_name_plural = 'پرسش'
        ordering = ['pk']

    survey = models.ForeignKey(verbose_name='پرسشنامه', to=Survey, on_delete=models.PROTECT, related_name='questions')
    code = models.CharField(verbose_name='شماره سوال', max_length=20)
    next_question = models.OneToOneField(verbose_name='سوال بعدی', to='Question', on_delete=models.PROTECT, null=True,
                                         blank=True, related_name='next', default=None)
    previous_question = models.OneToOneField(verbose_name='سوال قبلی', to='Question', on_delete=models.PROTECT,
                                             null=True,
                                             blank=True, related_name='previous')
    title = models.TextField(verbose_name='عنوان')
    question_choices = (('IntegerField', 'عدد'),
                        ('CharField', 'متن'),
                        ('ChoiceField', 'کرکره ی'),
                        ('RadioSelect', 'تک انتخاب'),
                        ('MultipleChoiceField', 'چند انتخاب'),)
    type = models.CharField(max_length=50, choices=question_choices, blank=True)
    has_other_in_options = models.BooleanField(verbose_name='سایر دارد؟', default=False)
    has_nothing_in_options = models.BooleanField(verbose_name='هیچکدام دارد؟', default=False)
    min_input_value = models.PositiveIntegerField(verbose_name='حداقل(فیلدهای عددی)')
    max_input_value = models.PositiveIntegerField(verbose_name='حداکثر(فیلدهای عددی)')
    is_required = models.BooleanField(verbose_name='اجباری است؟', default=False)

    def __str__(self):
        return f'{self.code}'


class Option(models.Model):
    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه'
        ordering = ['question','pk']

    question = models.ForeignKey(verbose_name='پرسش', to=Question, on_delete=models.CASCADE, related_name='options')
    title = models.TextField(verbose_name='عنوان')
    value = models.PositiveSmallIntegerField(verbose_name='کد', default=0)
    point = models.PositiveSmallIntegerField(verbose_name='امتیاز', default=0)

    def __str__(self):
        return f'{self.title}'


class AnswerSheet(models.Model):
    '''
    پاسخ های مصاحبه شونده
    '''

    class Meta:
        verbose_name = 'پاسخنامه'
        verbose_name_plural = 'پاسخنامه'

    interviewer = models.ForeignKey(verbose_name='پرسشگر', on_delete=models.PROTECT, to=Interviewer, blank=False,
                                    null=False, editable=True)
    responser = models.ForeignKey(verbose_name='پاسخگو', on_delete=models.PROTECT, to=Responder, blank=False,
                                  null=False, editable=True)
    survey = models.ForeignKey(verbose_name='پرسشنامه', to='Survey', on_delete=models.PROTECT, blank=False, null=False,
                               editable=True)
    date = models.DateField(verbose_name='تاریخ شمسی', blank=False, null=False, editable=True)
    number = models.PositiveIntegerField(verbose_name='شماره پرسشنامه',null=False)
    total_point = models.PositiveSmallIntegerField(verbose_name='مجموع امتیاز', default=0, blank=False, null=False,
                                                   editable=True)
    social_class = models.CharField(verbose_name='کلاس اجتماعی', max_length=1, editable=False)

    def __str__(self):
        return f'{self.responser.firstname}'

    def calculate_total_point(self):
        temp = [p.point for p in self.answers.all()]
        self.total_point = sum(temp)
        if self.responser.city.is_important:
            if 15 <= self.total_point:
                self.social_class = 'A'
            elif 8 <= self.total_point <= 14:
                self.social_class = 'B'
            else:
                self.social_class = 'C1'
        else:
            if 8 < self.total_point:
                self.social_class = 'A'
            elif 5 <= self.total_point <= 8:
                self.social_class = 'B'
            else:
                self.social_class = 'C1'

        self.save()


class Answer(models.Model):
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ'
        ordering = ['answersheet', 'question']

    question = models.ForeignKey(verbose_name='پرسش', to=Question, on_delete=models.PROTECT)
    answersheet = models.ForeignKey(verbose_name='پاسخنامه', to=AnswerSheet, related_name='answers',
                                    on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='مقدار', max_length=10, default=None, null=True, blank=True, editable=True)
    point = models.PositiveSmallIntegerField(verbose_name='امتیاز', editable=True, null=False, blank=False, default=0)
    option = models.ForeignKey(to=Option, verbose_name='گزینه ی انتخاب شده', editable=True, null=True, blank=True,
                               default=None, on_delete=models.PROTECT)

    def __str__(self):
        return f'پاسخ سوال' \
               f' {self.question.title}'


class Limit(models.Model):
    class Meta:
        verbose_name = 'محدودیت'
        verbose_name_plural = 'محدودیت'
        ordering = ['marital_status', 'age']

    marital_status_choices = ((1, 'مجرد'),
                              (2, 'متاهل'),
                              (3, 'مطلقه'),
                              (4, 'بیوه'))

    marital_status = models.IntegerField(verbose_name='وضعیت تاهل', choices=marital_status_choices,
                                         editable=True, null=False, blank=False)
    age_choices = ((1, '24-18'),
                   (2, '29-25'),
                   (3, '34-30'),
                   (4, '39-35'),)
    age = models.IntegerField(verbose_name='بازه سنی', choices=age_choices, editable=True, blank=False, null=False)
    maximum = models.PositiveSmallIntegerField(verbose_name='تعداد سهمیه', editable=True, blank=False, null=False)
    capacity = models.PositiveSmallIntegerField(verbose_name='تعداد ثبت نام شده', editable=True, default=0)

    def __str__(self):
        return f'{self.marital_status}          {self.age}'

    def check_for_capacity(self):
        if self.maximum > self.capacity:
            self.capacity += 1
            self.save()
            return True
        else:
            return False


class BrandCategory(models.Model):
    class Meta:
        verbose_name = 'محصولات-دسته بندی'
        verbose_name_plural = 'محصولات-دسته بندی'
        ordering = ['pk']

    title = models.CharField(verbose_name='عنوان دسته بندی', max_length=50, blank=False, null=False)

    def __str__(self):
        return f'{self.title}'


class Brand(models.Model):
    class Meta:
        verbose_name = 'محصولات'
        verbose_name_plural = 'محصولات'
        ordering = ['category', 'value']

    title = models.CharField(verbose_name='عنوان', max_length=50, blank=False, null=False)
    value = models.PositiveSmallIntegerField(verbose_name='کد')
    category = models.ForeignKey(to=BrandCategory, on_delete=models.PROTECT, verbose_name='دسته بندی',
                                 related_name='brands')

    def __str__(self):
        return f'{self.title}'
