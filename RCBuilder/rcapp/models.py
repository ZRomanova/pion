from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core import validators

def parse_filename(instance, filename):
    return smart_text(filename)
# App models

# Расширение

class UserAdditionalData(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True)
    organization = models.CharField(max_length=100, verbose_name="Организация", blank=True)
    occupation = models.CharField(max_length=100, verbose_name="Должность", blank=True)

class UserRequest(models.Model):
    username = models.CharField(max_length=100, verbose_name="Логин", blank=False)
    email = models.CharField(max_length=100, verbose_name="Адрес электронной почты", blank=False)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", blank=False)
    first_name = models.CharField(max_length=100, verbose_name="Имя", blank=False)
    middle_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True)
    site = models.CharField(max_length=100, verbose_name="Веб сайт или адрес в социальных сетях", blank=False, validators=[validators.MinLengthValidator(2, message="Недопустимое значение")])
    region = models.CharField(max_length=100, verbose_name="Регион", blank=False, validators=[validators.MinLengthValidator(2, message="Недопустимое значение региона")])
    organization = models.CharField(max_length=100, verbose_name="Организация", blank=False, validators=[validators.MinLengthValidator(2, message="Недопустимое значение организации")])
    occupation = models.CharField(max_length=100, verbose_name="Должность", blank=True)
    password = models.CharField(max_length=100, verbose_name="Пароль", blank=False)
    password_repeat = models.CharField(max_length=100, verbose_name="Повторите пароль", blank=False)
    created = models.BooleanField(verbose_name="Создан", default=False)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, blank=True)
    submission_date = models.DateTimeField(verbose_name="Дата подтверждения", default=None, null=True, blank=True)
    wanna_be_shown = models.BooleanField(verbose_name="После регистрации отобразить на странице пользователей", default=True)
    last_seen = models.DateTimeField(verbose_name="Дата последнего входа", default=None, null=True, blank=True)
    class Meta:
        verbose_name = "Запрос на регистрацию нового пользователя"
        verbose_name_plural = "Запросы на регистрацию нового пользователя"
    def __str__(self):
        return self.username + ": " + self.email + " => " + self.last_name + " " + self.first_name + " " + self.middle_name + " => " + self.site + " => " + self.region + ": " + self.organization + " – " + self.occupation
    def get_absolute_url(self):
        return "/portal/request/" + str(self.pk)
    def get_rcs(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            return []
        user = users[0]
        rcs = ResultsChain.objects.filter(user=user)
        return rcs
    def created_status(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            if self.created:
                return "Отклонён/удалён"
            else:
                return "Ожидает подтверждения"
        else:
            return "Пользователь существует (подтвержден)"
    def created_status_class(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            if self.created:
                return "danger"
            else:
                return "warning"
        else:
            return "success"
    def display_status(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            if self.created:
                return False
            else:
                return True
        else:
            return True
            
    def has_company_data(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            return -1
        user = users[0]
        companies = CompanyData.objects.filter(company_owner=user)
        if len(companies) == 0:
            return 0
        return 1
    def create_company(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            return
        user = users[0]
        companies = CompanyData.objects.filter(company_owner=user)
        if len(companies) != 0:
            return
        created = CompanyData.objects.create(company_name=self.organization, 
                                    company_site=self.site, 
                                    company_owner=user, 
                                    contact_fio=self.last_name + " " + self.first_name + (' ' + self.middle_name if self.middle_name else ''), 
                                    contact_job=self.occupation,
                                    contact_email=self.email,
                                    reg_region=self.region,
                                    realization_region=self.region)
        CompanyDataUserConnector.objects.create(user_ref=user, company_data_ref=created)
    def remove_company(self):
        users = User.objects.filter(username=self.username)
        if len(users) == 0:
            return
        user = users[0]
        companies = CompanyData.objects.filter(company_owner=user)
        if len(companies) == 0:
            return
        companies.delete()


#Цепочка результатов
class ResultsChain(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название программы")
    organization = models.CharField(max_length=150, blank=True, verbose_name="Организация")
    website = models.CharField(max_length=80, blank=True, verbose_name="Сайт организации")
    formation_date = models.DateField(verbose_name="Дата формирования", auto_now_add=True)
    realization_days = models.IntegerField(verbose_name="Дней на реализацию", blank=True, null=True)
    realization_date = models.DateField(verbose_name="Реализовать до", default=datetime.date.today, blank=True)
    terms = models.CharField(max_length=300, default="", blank=True, verbose_name="Сроки")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    durability = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Длительность проектного цикла")
    loop_beginning_date = models.DateField(verbose_name="Дата начала проектного цикла", blank=True, null=True, default=None)
    loop_ending_date = models.DateField(verbose_name="Дата окончания проектного цикла", blank=True, null=True, default=None)
    case_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить файл с кейсом по данной программе")
    head_comment = models.CharField(max_length=100, blank=True, default="", verbose_name="Ссылка на отзыв куратора")
    company_data_ref = models.ForeignKey('CompanyData', on_delete=models.SET_NULL, verbose_name="Название организации", null=True, default=None, blank=True)
    display_organization = models.BooleanField(verbose_name="Отображать организацию", default=False)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/portal/" + str(self.pk)
    def get_edit_url(self):
        return "/portal/edit/" + str(self.pk)
    def get_company_name(self):
        if self.company_data_ref:
            companies = CompanyData.objects.filter(pk=self.company_data_ref.pk)
            if len(companies) == 1:
                return companies[0].company_name
        else:
            if self.user:
                companies = CompanyData.objects.filter(company_owner=self.user)
                if len(companies) == 1:
                    return companies[0].company_name
                company_references = CompanyDataUserConnector.objects.filter(user_ref = self.user)
                if len(company_references) == 1:
                    company_reference = company_references[0]
                    companies = CompanyData.objects.filter(pk=company_reference.pk)
                    if len(companies) > 0:
                        return companies[0].company_name
        return self.organization
    class Meta:
        verbose_name = 'Цепочка результатов'
        verbose_name_plural = 'Цепочки результатов'

#Целевая группа
class Target(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    class Meta:
        verbose_name = "Целевая группа"
        verbose_name_plural = "Целевые группы"

#Ресурс
class Resource(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    subtitle = models.CharField(max_length=100, null=True, blank=True, default="Другое", verbose_name='Группа')
    custom_subtitle = models.CharField(max_length=100, blank=True, verbose_name='Либо введите свой вариант группы', null=True, default=None)
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.value
    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурсы"

#Деятельность
class Activity(models.Model):
    value = models.CharField(max_length=700, verbose_name="Деятельность")
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевые группы")
    # target_ref = models.ForeignKey('Target', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Целевая группа")
    def __str__(self):
        return self.value
    class Meta:
        verbose_name = "Деятельность"
        verbose_name_plural = "Деятельности"

#Непосредственный результат
class Output(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    order = models.IntegerField(verbose_name = "Порядковый номер", blank=True, default=0)
    # activity_ref = models.ForeignKey('Activity', on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="Деятельность")
    activity_refs = models.ManyToManyField(Activity, blank=True, verbose_name="Деятельности")
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    target_ref = models.ForeignKey('Target', on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Целевая группа")
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def activities(self):
        result = ""
        for elem in self.activity_refs.all():
            result += ("" if result == "" else ", ") + str(elem)
        return result
    class Meta:
        verbose_name = "Непосредственный результат"
        verbose_name_plural = "Непосредственные результаты"
        ordering = ['order']

class OutputIndicator(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    description = models.CharField(max_length=500, blank=True, verbose_name="Текстовое описание показателя")
    plan = models.CharField(max_length=500, verbose_name="План", blank=True)
    fact = models.CharField(max_length=500, verbose_name="Факт", blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод сбора данных 1", default="custom")
    custom_method = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 1", blank=True)
    method2 = models.CharField(max_length=500, verbose_name="Метод сбора данных 2", default="custom")
    custom_method2 = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 2", blank=True)
    method3 = models.CharField(max_length=500, verbose_name="Метод сбора данных 3", default="custom")
    custom_method3 = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 3", blank=True)
    frequency = models.IntegerField(verbose_name = "Частота сбора", blank=True, default=None, null=True)
    owner = models.CharField(max_length=1000, blank=True, default="", verbose_name="Кто ответственен за сбор")
    reports_publicity = models.CharField(max_length=100, verbose_name="В каких отчетах используется", blank=True, default="")
    reports = models.CharField(max_length=1000, blank=True, default="", verbose_name="Отчеты")
    values = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения показателя")
    values_plan = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения плана показателя")
    recieve_date = models.DateField(blank=True, null=True, default=None, verbose_name="Дата первого измерения")
    method_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить файл с методикой")
    source_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить форму источника данных")
    data_source = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Инстумент сбора данных")
    data_source_desc = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Источник данных")
    data_source_custom = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Свой вариант")
    methodic = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Методика сбора данных")
    year = models.IntegerField(verbose_name="Год", blank=True, default=2017)
    #references
    output_ref = models.ForeignKey('Output', on_delete=models.CASCADE, null=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def methods(self):
        result = ""
        if self.method == "custom":
            if self.custom_method.strip() != "":
                result += self.custom_method
        else:
            if self.method.strip() != "":
                result += self.method
        
        if self.method2 == "custom":
            if self.custom_method2.strip() != "":
                result += ("" if result == "" else ", ") + self.custom_method2
        else:
            if self.method2.strip() != "":
                result += ("" if result == "" else ", ") + self.method2
        
        if self.method3 == "custom":
            if self.custom_method3.strip() != "":
                result += ("" if result == "" else ", ") + self.custom_method3
        else:
            if self.method3.strip() != "":
                result += ("" if result == "" else ", ") + self.method3
        return result

    class Meta:
        verbose_name = "Показатель непосредственного результата"
        verbose_name_plural = "Показатели непосредственного результата"

class OutputIndicatorPF(models.Model):
    plan = models.CharField(max_length=500, verbose_name="План", blank=True)
    fact = models.CharField(max_length=500, verbose_name="Факт", blank=True)
    year = models.IntegerField(verbose_name="Год", blank=True, default=2017)
    current = models.BooleanField(verbose_name="Текущий год", default=True)
    output_indicator_ref = models.ForeignKey('OutputIndicator', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.year) + self.plan + "/" + self.fact
    class Meta:
        verbose_name = "План и факт показателя непосредственного результата"
        verbose_name_plural = "Планы и факты показателя непосредственного результата"
        
class OutputIndicatorMethod(models.Model):
    value = models.CharField(max_length=500, verbose_name="Значение метода сбора данных", blank=True)
    output_indicator_ref = models.ForeignKey('OutputIndicator', on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Метод показателя непосредственного результата"
        verbose_name_plural = "Методы показателя непосредственного результата"

#Социальный результат
class Outcome(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    order = models.IntegerField(verbose_name = "Порядковый номер", blank=True, default=0)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    # output_ref = models.ForeignKey('Output', on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="Непосредственный результат")
    output_refs = models.ManyToManyField(Output, blank=True, verbose_name="Непосредственные результаты")
    target_ref = models.ForeignKey('Target', on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Целевая группа")
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def outputs(self):
        result = ""
        for elem in self.output_refs.all():
            result += ("" if result == "" else ", ") + str(elem)
        return result
    class Meta:
        verbose_name = "Социальный результат"
        verbose_name_plural = "Социальные результаты"
        ordering = ['order']

class OutcomeIndicator(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка", blank=True)
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    description = models.CharField(max_length=500, blank=True, verbose_name="Текстовое описание показателя")
    plan = models.CharField(max_length=500, verbose_name="План", blank=True)
    fact = models.CharField(max_length=500, verbose_name="Факт", blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод сбора данных 1", default="custom")
    custom_method = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 1", blank=True)
    method2 = models.CharField(max_length=500, verbose_name="Метод сбора данных 2", default="custom")
    custom_method2 = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 2", blank=True)
    method3 = models.CharField(max_length=500, verbose_name="Метод сбора данных 3", default="custom")
    custom_method3 = models.CharField(max_length=500, verbose_name="Свой метод сбора данных 3", blank=True)
    frequency = models.IntegerField(verbose_name = "Частота сбора", blank=True, default=None, null=True)
    owner = models.CharField(max_length=1000, blank=True, default="", verbose_name="Кто ответственен за сбор")
    reports_publicity = models.CharField(max_length=100, verbose_name="В каких отчетах используется", blank=True, default="")
    reports = models.CharField(max_length=1000, blank=True, default="", verbose_name="Отчеты")
    values = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения показателя")
    values_plan = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения плана показателя")
    recieve_date = models.DateField(blank=True, null=True, default=None, verbose_name="Дата первого измерения")
    method_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить файл с методикой")
    source_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить форму источника данных")
    data_source = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Инстумент сбора данных")
    data_source_desc = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Источник данных")
    data_source_custom = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Свой вариант")
    methodic = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Методика сбора данных")
    year = models.IntegerField(verbose_name="Год", blank=True, default=2017)
    #references
    outcome_ref = models.ForeignKey('Outcome', on_delete=models.CASCADE, null=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def methods(self):
        result = ""
        if self.method == "custom":
            if self.custom_method.strip() != "":
                result += self.custom_method
        else:
            if self.method.strip() != "":
                result += self.method
        
        if self.method2 == "custom":
            if self.custom_method2.strip() != "":
                result += ("" if result == "" else ", ") + self.custom_method2
        else:
            if self.method2.strip() != "":
                result += ("" if result == "" else ", ") + self.method2
        
        if self.method3 == "custom":
            if self.custom_method3.strip() != "":
                result += ("" if result == "" else ", ") + self.custom_method3
        else:
            if self.method3.strip() != "":
                result += ("" if result == "" else ", ") + self.method3
        return result

    class Meta:
        verbose_name = "Показатель социального результата"
        verbose_name_plural = "Показатели социального результата"
        
class OutcomeIndicatorPF(models.Model):
    plan = models.CharField(max_length=500, verbose_name="План", blank=True)
    fact = models.CharField(max_length=500, verbose_name="Факт", blank=True)
    year = models.IntegerField(verbose_name="Год", blank=True, default=2017)
    current = models.BooleanField(verbose_name="Текущий год", default=True)
    outcome_indicator_ref = models.ForeignKey('OutcomeIndicator', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.year) + self.plan + "/" + self.fact
    class Meta:
        verbose_name = "План и факт показателя социального результата"
        verbose_name_plural = "Планы и факты показателя социального результата"
        
class OutcomeIndicatorMethod(models.Model):
    value = models.CharField(max_length=500, verbose_name="Значение метода сбора данных", blank=True)
    outcome_indicator_ref = models.ForeignKey('OutcomeIndicator', on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Метод показателя социального результата"
        verbose_name_plural = "Методы показателя социального результата"

#Социальный эффект
class Impact(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    comm = models.CharField(max_length=5000, verbose_name="Комментарий", blank=True)
    order = models.IntegerField(verbose_name = "Порядковый номер", blank=True, default=0)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    target_ref = models.ForeignKey('Target', on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Целевая группа")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, verbose_name="Социальные результаты")
    # outcome_ref = models.ForeignKey('Outcome', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Социальный результат")
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def outcomes(self):
        result = ""
        for elem in self.outcome_refs.all():
            result += ("" if result == "" else ", ") + str(elem)
        return result
    class Meta:
        verbose_name = "Социальный эффект"
        verbose_name_plural = "Социальные эффекты"
        ordering = ['order']

class ImpactIndicator(models.Model):
    value = models.CharField(max_length=500, verbose_name="Выберите из списка")
    custom_value = models.CharField(max_length=500, blank=True, verbose_name="Либо введите свой вариант")
    description = models.CharField(max_length=500, blank=True, verbose_name="Текстовое описание показателя")
    plan = models.CharField(max_length=500, verbose_name="План", blank=True)
    fact = models.CharField(max_length=500, verbose_name="Факт", blank=True)
    frequency = models.IntegerField(verbose_name = "Частота сбора", blank=True, default=None, null=True)
    owner = models.CharField(max_length=1000, blank=True, default="", verbose_name="Кто ответственен за сбор")
    reports_publicity = models.CharField(max_length=100, verbose_name="В каких отчетах используется", blank=True, default="")
    reports = models.CharField(max_length=1000, blank=True, default="", verbose_name="Отчеты")
    values = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения показателя")
    values_plan = models.CharField(max_length=1000, blank=True, default="", verbose_name="Значения плана показателя")
    recieve_date = models.DateField(blank=True, null=True, default=None, verbose_name="Дата первого измерения")
    source_file = models.FileField(blank=True, null=True, default=None, verbose_name="Загрузить форму источника данных")
    data_source = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Инстумент сбора данных")
    data_source_desc = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Источник данных")
    data_source_custom = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Свой вариант")
    methodic = models.CharField(max_length=1000, blank=True, null=True, default=None, verbose_name="Методика сбора данных")
    #references
    impact_ref = models.ForeignKey('Impact', on_delete=models.CASCADE, null=True)
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.value if self.value != "custom" else self.custom_value
    def get_values_list(self):
        values_string = self.values
        if values_string is not None and len(values_string.strip()) > 0:
            return values_string.split(',')
        else:
            toret = []
            if self.frequency is None:
                return toret
            counter = 1
            while counter < self.frequency:
                toret.append('')
                counter += 1
            return toret
    def get_values_plan_list(self):
        values_plan_string = self.values_plan
        if values_plan_string is not None and len(values_plan_string.strip()) > 0:
            return values_plan_string.split(',')
        else:
            toret = []
            if self.frequency is None:
                return toret
            counter = 1
            while counter < self.frequency:
                toret.append('')
                counter += 1
            return toret
    class Meta:
        verbose_name = "Показатель социального эффекта"
        verbose_name_plural = "Показатели социального эффекта"


class PageComment(models.Model):
    comment = models.CharField(max_length=1000, verbose_name="Комментарий к странице")
    page_url = models.CharField(max_length=100, verbose_name="Страница", blank=True, null=True)
    def __str__(self):
        return self.comment
    class Meta:
        verbose_name = "Комментарий эксперта"
        verbose_name_plural = "Комментарии экспертов"

class ResultsChainUserConnector(models.Model):
    rc_ref = models.ForeignKey('ResultsChain', on_delete=models.CASCADE, null=True)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    class Meta:
        verbose_name = "Связь цепочки и пользователя"
        verbose_name_plural = "Связи цепочки и пользователя"

#Списки : Не реализовано

class TargetsListGroup(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Группа списка "Целевые группы"'
        verbose_name_plural = 'Группы списка "Целевые группы"'

class TargetsListItem(models.Model):
    value = models.CharField(max_length=300, verbose_name="Значение")
    item_of = models.ForeignKey('TargetsListGroup', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.value
    class Meta:
        verbose_name = 'Значение списка "Целевые группы"'
        verbose_name_plural = 'Значения списка "Целевые группы"'

class CompanyData(models.Model):
    company_name  = models.CharField(max_length=300, verbose_name="Название организации")
    company_site  = models.CharField(max_length=300, verbose_name="Веб-сайт организации", blank=True, default="")
    company_logo  = models.ImageField(verbose_name="Логотип организации", blank=True, null=True, default=None,
                                                upload_to=parse_filename)
    company_owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Создатель", null=True)
    # contact 
    contact_fio = models.CharField(max_length=300, blank=True, default="", verbose_name="ФИО контактного лица")
    contact_job = models.CharField(max_length=300, blank=True, default="", verbose_name="Должность контактного лица")
    contact_email = models.CharField(max_length=300, blank=True, default="", verbose_name="E-mail контактного лица")
    # regions
    reg_region = models.CharField(max_length=300, blank=True, default="", verbose_name="Регион регистрации")
    realization_region = models.CharField(max_length=300, blank=True, default="", verbose_name="Регионы реализации программы")

    display_in_list = models.BooleanField(verbose_name="Отображать в списке", default=True)
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
    def __str__(self):
        return self.company_name
    def get_absolute_url(self):
        return "/portal/company-view/" + str(self.pk)
    
class CompanyDataUserConnector(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Участник")
    company_data_ref = models.ForeignKey('CompanyData', on_delete=models.CASCADE, verbose_name="Организация")

class LibraryPage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название страницы")
    content = RichTextUploadingField(default=None, null=True, blank=True, verbose_name="Содержание")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return '/portal/library/' + str(self.pk)
    class Meta:
        verbose_name = "Страница библиотеки"
        verbose_name_plural = "Страницы библиотеки"
        
class HelpParagraph(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название подсказки")
    short_content = RichTextUploadingField(blank=True, verbose_name="Краткая подсказка")
    full_content = RichTextUploadingField(blank=True, verbose_name="Полная подсказка")
    additional_content = RichTextUploadingField(blank=True, verbose_name="Дополнение")
    order = models.IntegerField(blank=True, default=1, verbose_name="Порядковый номер")
    display_full = models.BooleanField(default=True, verbose_name="Отображать в полном руководстве")
    display_short = models.BooleanField(default=True, verbose_name="Отображать во всплывающей подсказке")
    special_name = models.CharField(max_length=200, verbose_name="Системное название")
    def __str__(self):
        return self.name + " (порядковый номер: " + str(self.order) + ")"
    class Meta:
        verbose_name = "Подсказка онлайн-руководства"
        verbose_name_plural = "Подсказки онлайн-руководства"

class BenchmarkingParametersQuery(models.Model):
    query = models.CharField(max_length=5000, verbose_name="Запрос с параметрами")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    def __str__(self):
        return self.query