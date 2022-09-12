from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Целевая группа
class Target(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название целевой группы")
    parent_ref = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Родительский раздел", null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Целевая группа"
        verbose_name_plural = "Целевые группы"

# Практика
class Practice(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название практики")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Практика"
        verbose_name_plural = "Практики"

#Тематическая группа
class ThematicGroup(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название тематической группы")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Тематическая группа"
        verbose_name_plural = "Тематические группы"

class OutcomeMethod(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название метода и инструмента сбора данных")
    url = models.CharField(max_length=500, verbose_name="Ссылка на метод и инструмент сбора данных")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Метод и инструмент сбора данных"
        verbose_name_plural = "Методы и инструменты сбора данных"

# Социальный результат
class Outcome(models.Model):
    name = models.CharField(max_length=500, verbose_name="Общая формулировка социального результата")
    thematic_group_refs = models.ManyToManyField(ThematicGroup, blank=True, default=None, verbose_name="Тематические группы")
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевые группы")
    practice_refs = models.ManyToManyField(Practice, blank=True, verbose_name="Практики")
    method_refs = models.ManyToManyField(OutcomeMethod, blank=True, verbose_name="Методы и инструменты сбора данных")

    createdby = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    add_public_will = models.BooleanField(verbose_name="В общую библиотеку", default=False)
    add_public_confirm = models.BooleanField(verbose_name="Подтверждение администратором", default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Социальный результат"
        verbose_name_plural = "Социальные результаты"

class OutcomeExactName(models.Model):
    name = models.CharField(max_length=500, verbose_name="Частная формулировка социального результата")
    outcome_ref = models.ForeignKey('Outcome', on_delete=models.CASCADE, verbose_name="Социальный результат")
    def __str__(self):
        return self.outcome_ref.name + " --> " + self.name
    class Meta:
        verbose_name = "Частная формулировка социального результата"
        verbose_name_plural = "Частные формулировки социального результата"

class UserRequest(models.Model):
    email = models.CharField(max_length=500, verbose_name="Адрес эл. почты")
    lastname = models.CharField(max_length=500, verbose_name="Фамилия")
    firstname = models.CharField(max_length=500, verbose_name="Имя")
    middlename = models.CharField(max_length=500, verbose_name="Отчество")
    region = models.CharField(max_length=500, verbose_name="Регион", default=None, null=True, blank=True)
    organization = models.CharField(max_length=500, verbose_name="Организация")
    website = models.CharField(max_length=500, verbose_name="Веб-сайт или адрес организации в социальных сетях")
    position = models.CharField(max_length=500, verbose_name="Должность")
    password = models.CharField(max_length=500, verbose_name="Пароль")
    createdon = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    verifiedon = models.DateTimeField(verbose_name="Дата подтверждения", default=None, null=True, blank=True)
    lastseenon = models.DateTimeField(verbose_name="Дата последнего визита", default=None, null=True, blank=True)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=None, null=True, blank=True)
    class Meta:
        verbose_name = "Запрос на регистрацию"
        verbose_name_plural = "Запросы на регистрацию"
    def __str__(self):
        return self.email
    def accept(self):
        user_ref = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user_ref = user_ref
        self.verifiedon = datetime.datetime.now()
        self.save()
        send_mail('Заявка на сервисе pion.org.ru/newpion', 'Ваша заявка принята! Вы можете войти с использованием ваших логина и пароля по адресу https://pion.org.ru/newpion', 'mail@pion.org.ru', [self.email], fail_silently=True)
    def decline(self):
        self.verifiedon = datetime.datetime.now()
        self.save()

@receiver(post_save, sender=UserRequest)
def new_user_registration(sender, instance, **kwargs):
    if instance.verifiedon is not None:
        return
    send_mail('NEWPION Заявка на регистрацию', 'Заявка на создание нового пользователя поступила\nАдминистрация запроса: https://pion.org.ru/newpion/admin/user-requests', 'mail@pion.org.ru', ['info@ep.org.ru', 'kolega212@yandex.ru'], fail_silently=True)
    send_mail('Заявка на сервисе pion.org.ru/newpion', 'Ваша заявка на регистрацию принята. Мы свяжемся с вами!', 'mail@pion.org.ru', [instance.email], fail_silently=True)

class OutcomeLibraryLink(models.Model):
    outcome_ref = models.ForeignKey(Outcome, on_delete=models.CASCADE, verbose_name="Социальный результат")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    def __str__(self):
        return self.outcome_ref.name + " <-> " + self.user_ref.username
    class Meta:
        verbose_name = "Связь социального результата с личной библиотекой"
        verbose_name_plural = "Связи социального результата с личной библиотекой"
        
class OutcomeIndicator(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название показателя социального результата")
    outcome_ref = models.ForeignKey(Outcome, on_delete=models.CASCADE, verbose_name="Социальный результат")
    def __str__(self):
        return self.outcome_ref.name + " --> " + self.name
    class Meta:
        verbose_name = "Показатель социального результата"
        verbose_name_plural = "Показатели социального результата"



#Создание библиотек=====================================================================================================


#Метод
class Method(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название метода")
    info = models.CharField(max_length=1000, blank=True, default='', verbose_name="Подсказка")
    parent_ref = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Родительский раздел", null=True, blank=True)
    add_public = models.BooleanField(default=False, verbose_name="Публичный доступ")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Метод"
        verbose_name_plural = "Методы"


#Уровень результата
class OutcomeLevel(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название уровня результата")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Уровень результата"
        verbose_name_plural = "Уровени результата"

#Элементы системы мониторинга и оценки, представленные в кейсе
class MonitoringElement(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название элемента системы мониторинга и оценки")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Элемент системы мониторинга и оценки"
        verbose_name_plural = "Элементы системы мониторинга и оценки"

#Виды деятельности (активностей) организации, представленные в кейсе
class OrganizationActivity(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название вида деятельности организации")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Вид деятельности организации"
        verbose_name_plural = "Виды деятельности организации"

#=======================================================================================================================


class RepresentationMethod(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название представления данных в отчете")
    add_public = models.BooleanField(default=False, verbose_name="Публичный доступ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Представление данных в отчете"
        verbose_name_plural = "Представления данных в отчете"


class EvaluationType(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название вида оценки")
    add_public = models.BooleanField(default=False, verbose_name="Публичный доступ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид оценки"
        verbose_name_plural = "Виды оценки"


class AnalysisMethod(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название метод анализа")
    add_public = models.BooleanField(default=False, verbose_name="Публичный доступ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод анализа"
        verbose_name_plural = "Методы анализа"

class ToolTag(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег краткой информации инструмента"
        verbose_name_plural = "Теги краткой информации инструмента"



#Библиотека инструментов================================================================================================

#Элемент



class Tool(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название инструмента")
    info = models.CharField(max_length=500, verbose_name="Аннотация")
    tool_tag_refs = models.ManyToManyField(ToolTag, blank=True, verbose_name="Теги краткой информации")

    thematic_group_ref = models.ForeignKey(ThematicGroup, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Тематическая группа")
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевые группы")
    practice_ref = models.ForeignKey(Practice, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Практика")
    method_ref = models.ForeignKey(Method, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Метод")
    outcome_level_ref = models.ForeignKey(OutcomeLevel, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Уровень социального результата")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, verbose_name="Социальные результаты")
    tool_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл инструмента")
    url = models.CharField(max_length=500, blank=True, default=None, verbose_name="Ссылка на инструмент")

    createdby = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    add_public_will = models.BooleanField(verbose_name="В общую библиотеку", default=False)
    add_public_confirm = models.BooleanField(verbose_name="Подтверждение администратором ", default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Инструмент"
        verbose_name_plural = "Инструменты"

class ToolChangeRequest(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, default=None, verbose_name="Название инструмента")
    info = models.CharField(max_length=500, blank=True, null=True, default=None,verbose_name="Аннотация")
    tool_tag_refs = models.ManyToManyField(ToolTag, blank=True, default=None, verbose_name="Теги краткой информации")

    thematic_group_ref = models.ForeignKey(ThematicGroup, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Тематическая группа")
    target_refs = models.ManyToManyField(Target, blank=True, default=None, verbose_name="Целевые группы")
    practice_ref = models.ForeignKey(Practice, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Практика")
    method_ref = models.ForeignKey(Method, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Метод")
    outcome_level_ref = models.ForeignKey(OutcomeLevel, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Уровень социального результата")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, default=None, verbose_name="Социальные результаты")
    tool_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл инструмента")
    url = models.CharField(max_length=500, blank=True, default=None, null=True, verbose_name="Ссылка на инструмент")
    tool_ref = models.OneToOneField(Tool, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата запроса')

    add_public_confirm = models.BooleanField(verbose_name="Принять изменения", default=False)

    def __str__(self):
        tool = Tool.objects.filter(pk=self.pk).first()
        return "Запрос на изменение " + tool.name
    class Meta:
        verbose_name = "Запрос на изменение инструмента"
        verbose_name_plural = "Запрос на изменение инструмента"

#Элемент связь
class ToolLibraryLink(models.Model):
    tool_ref = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name="Инструмент")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    def __str__(self):
        return self.tool_ref.name + " <-> " + self.user_ref.username
    class Meta:
        verbose_name = "Связь инструмента с личной библиотекой"
        verbose_name_plural = "Связи инструментов с личной библиотекой"
#=======================================================================================================================



#Библиотека кейсов======================================================================================================

#Элемент
class Case(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название кейса")
    organization = models.CharField(max_length=500, verbose_name="Организация")
    case_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл кейса")
    url = models.CharField(max_length=500, blank=True, default=None, verbose_name="Ссылка на кейс")
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевая группа")
    practice_ref = models.ForeignKey(Practice, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Практика")
    organization_activity_refs = models.ManyToManyField(OrganizationActivity, blank=True, verbose_name="Виды деятельности")
    monitoring_element_refs = models.ManyToManyField(MonitoringElement, blank=True, verbose_name="Элементы системы мониторинга и оценки")

    thematic_group_ref = models.ForeignKey(ThematicGroup, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Тематическая группа")
    verification_info = models.CharField(max_length=2000, verbose_name="Сведения о верификации практики, в рамках которой реализовывалась программа", default="", blank=True)
    verification_level_regularity = models.CharField(max_length=2000, verbose_name="Регламентированность практики", default="", blank=True)
    verification_level_validity = models.CharField(max_length=2000, verbose_name="Обоснованность практики", default="", blank=True)
    verification_level_outcome_accessibility = models.CharField(max_length=2000, verbose_name="Достижение социальных результатов", default="", blank=True)
    verification_level_outcome_validity = models.CharField(max_length=2000, verbose_name="Обоснованность данных о социальных результатах", default="", blank=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    add_public_will = models.BooleanField(verbose_name="В общую библиотеку", default=False)
    add_public_confirm = models.BooleanField(verbose_name="Подтверждение администратором ", default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Кейсы"
        verbose_name_plural = "Кейсы"

class CaseChangeRequest(models.Model):
    name = models.CharField(max_length=500,null=True, default=None, verbose_name="Название кейса")
    organization = models.CharField(max_length=500, null=True, default=None, verbose_name="Организация")
    case_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл кейса")
    url = models.CharField(max_length=500, blank=True, null=True, default=None, verbose_name="Ссылка на кейс")
    target_refs = models.ManyToManyField(Target, blank=True, default=None, verbose_name="Целевая группа")
    practice_ref = models.ForeignKey(Practice, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Практика")
    organization_activity_refs = models.ManyToManyField(OrganizationActivity, blank=True, default=None, verbose_name="Виды деятельности")
    monitoring_element_refs = models.ManyToManyField(MonitoringElement, blank=True, default=None, verbose_name="Элементы системы мониторинга и оценки")
    thematic_group_ref = models.ForeignKey(ThematicGroup, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Тематическая группа")
    
    verification_info = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Сведения о верификации практики, в рамках которой реализовывалась программа")
    verification_level_regularity = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Регламентированность практики")
    verification_level_validity = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Обоснованность практики")
    verification_level_outcome_accessibility = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Достижение социальных результатов")
    verification_level_outcome_validity = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Обоснованность данных о социальных результатах")
    
    case_ref = models.OneToOneField(Case, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата запроса')
    add_public_confirm = models.BooleanField(verbose_name="Принять изменения", default=False)

    def __str__(self):
        case = Case.objects.filter(pk=self.pk).first()
        return "Запрос на изменение " + case.name
    class Meta:
        verbose_name = "Запрос на изменение кейса"
        verbose_name_plural = "Запрос на изменение кейса"

class CaseLibraryLink(models.Model):
    case_ref = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="Кейс")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    def __str__(self):
        return self.case_ref.name + " <-> " + self.user_ref.username
    class Meta:
        verbose_name = "Связь кейса с личной библиотекой"
        verbose_name_plural = "Связи кейсов с личной библиотекой"

#Oтчёт об оценке EvaluationReport отчёт об оценке
class EvaluationReport(models.Model):
    type = models.CharField(max_length=500, verbose_name="Тип отчета")
    evaluation_type_ref = models.ForeignKey(EvaluationType, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Вид оценки")
    representation_method_refs = models.ManyToManyField(RepresentationMethod, blank=True, verbose_name="Методы представления данных в отчете")
    analysis_method_refs = models.ManyToManyField(AnalysisMethod, blank=True, verbose_name="Методы анализа данных")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, verbose_name="Социальные результаты")
    method_refs = models.ManyToManyField(Method, blank=True, verbose_name="Методы")
    key_questions = models.CharField(max_length=2000, verbose_name="Ключевые вопросы", default="")
    other_results = models.CharField(max_length=2000, verbose_name="Другие результаты", default="")
    evaluation_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл отчёта")
    case_ref = models.ForeignKey(Case, verbose_name="Кейс", on_delete=models.CASCADE, blank=True, null=True, default=None)

    add_public_will = models.BooleanField(verbose_name="Запрос сделать общедоступным", default=False)
    add_public_confirm = models.BooleanField(verbose_name="Подтверждение администратором", default=True)

    def __str__(self):
        return self.case_ref.name + '--->' + str(self.pk)
    class Meta:
        verbose_name = "Отчёт об оценке"
        verbose_name_plural = "Отчёты об оценке"

class EvaluationReportChangeRequest(models.Model):
    type = models.CharField(max_length=500, verbose_name="Тип отчета", blank=True, default=None, null=True)
    evaluation_type_ref = models.ForeignKey(EvaluationType, on_delete=models.CASCADE, blank=True, default=None, null=True, verbose_name="Вид оценки")
    representation_method_refs = models.ManyToManyField(RepresentationMethod, blank=True, verbose_name="Методы представления данных в отчете")
    analysis_method_refs = models.ManyToManyField(AnalysisMethod, blank=True, verbose_name="Методы анализа данных")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, verbose_name="Социальные результаты")
    method_refs = models.ManyToManyField(Method, blank=True, verbose_name="Методы")
    key_questions = models.CharField(max_length=2000, verbose_name="Ключевые вопросы", blank=True, default=None, null=True)
    other_results = models.CharField(max_length=2000, verbose_name="Другие результаты", blank=True, default=None, null=True)
    evaluation_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл отчёта")

    evalution_report_ref = models.OneToOneField(EvaluationReport, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата запроса')
    add_public_confirm = models.BooleanField(verbose_name="Принять изменения", default=False)

    def __str__(self):
        er = EvaluationReport.objects.filter(pk=self.pk).first()
        return er.case_ref.name
    class Meta:
        verbose_name = "Запрос на редактирование отчёта об оценке"
        verbose_name_plural = "Запрос на редактирование отчёта об оценке"


#=======================================================================================================================

class LogicalModel(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название логической модели")
    organization = models.CharField(max_length=500, verbose_name="Организация")
    thematic_group_ref = models.ForeignKey(ThematicGroup, null=True, on_delete=models.CASCADE, blank=True, verbose_name="Тематическая группа")
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевые группы")
    practice_refs = models.ManyToManyField(Practice, blank=True, verbose_name="Практики")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, verbose_name="Социальные результаты")
    period = models.CharField(max_length=2000, verbose_name="Сроки реализации")
    verification_info = models.CharField(max_length=2000, verbose_name="Сведения о верификации практики, в рамках которой реализовывалась программа", default="", blank=True)
    verification_level_regularity = models.CharField(max_length=2000, verbose_name="Регламентированность практики", default="", blank=True)
    verification_level_validity = models.CharField(max_length=2000, verbose_name="Обоснованность практики", default="", blank=True)
    verification_level_outcome_accessibility = models.CharField(max_length=2000, verbose_name="Достижение социальных результатов", default="", blank=True)
    verification_level_outcome_validity = models.CharField(max_length=2000, verbose_name="Обоснованность данных о социальных результатах", default="", blank=True)
    model_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл логической модели")
    result_tree_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл дерева результатов")

    add_public_confirm = models.BooleanField(verbose_name="Подтверждение администратором", default=False)
    add_public_will = models.BooleanField(verbose_name="В общую библиотеку", default=False)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")

    def __str__(self):
        return self.name + ' ' + self.period
    class Meta:
        verbose_name = "Логическая модель"
        verbose_name_plural = "Логические модели"

class LogicalModelChangeRequest(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, default=None,  verbose_name="Название логической модели")
    organization = models.CharField(max_length=500, blank=True, null=True, default=None,  verbose_name="Организация")
    thematic_group_ref = models.ForeignKey(ThematicGroup, null=True, default=None, on_delete=models.CASCADE, blank=True, verbose_name="Тематическая группа")
    target_refs = models.ManyToManyField(Target, blank=True, default=None, verbose_name="Целевые группы")
    practice_refs = models.ManyToManyField(Practice, blank=True, default=None, verbose_name="Практики")
    outcome_refs = models.ManyToManyField(Outcome, blank=True, default=None, verbose_name="Социальные результаты")
    period = models.CharField(max_length=2000, blank=True, null=True, default=None,  verbose_name="Сроки реализации")
    verification_info = models.CharField(max_length=2000, blank=True, null=True, default=None,  verbose_name="Сведения о верификации практики, в рамках которой реализовывалась программа")
    verification_level_regularity = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Регламентированность практики")
    verification_level_validity = models.CharField(max_length=2000, blank=True, null=True, default=None,  verbose_name="Обоснованность практики")
    verification_level_outcome_accessibility = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Достижение социальных результатов")
    verification_level_outcome_validity = models.CharField(max_length=2000, blank=True, null=True, default=None, verbose_name="Обоснованность данных о социальных результатах")
    model_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл логической модели")
    result_tree_file = models.FileField(blank=True, null=True, default=None, verbose_name="Файл дерева результатов")

    logical_model_ref = models.OneToOneField(LogicalModel, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата запроса')
    add_public_confirm = models.BooleanField(verbose_name="Принять изменения", default=False)

    def __str__(self):
        logical_model = LogicalModel.objects.filter(pk=self.pk).first()
        return "Запрос на изменение " + logical_model.name
    class Meta:
        verbose_name = "Запрос на изменение логической модели"
        verbose_name_plural = "Запрос на изменение логической модели"

class LogicalModelLibraryLink(models.Model):
    logical_model_ref = models.ForeignKey(LogicalModel, on_delete=models.CASCADE, verbose_name="Логическая модель")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    def __str__(self):
        return self.logical_model_ref.name + " <-> " + self.user_ref.username
    class Meta:
        verbose_name = "Связь логической модели с личной библиотекой"
        verbose_name_plural = "Связи логических моделей с личной библиотекой"

class Program(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название программы")
    description = models.CharField(max_length=2000, verbose_name="Описание программы")
    period = models.CharField(max_length=2000, verbose_name="Сроки программы")
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=None, null=True, blank=True)
    target_refs = models.ManyToManyField(Target, blank=True, verbose_name="Целевые группы")
    practice_refs = models.ManyToManyField(Practice, blank=True, verbose_name="Практики")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

class Assumption(models.Model):
    text = models.TextField(verbose_name="Текст предположения")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.text:
            name_former += self.text
        return name_former
    class Meta:
        verbose_name = "Предположение"
        verbose_name_plural = "Предположения"

class Context(models.Model):
    text = models.TextField(verbose_name="Текст контекста")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.text:
            name_former += self.text
        return name_former
    class Meta:
        verbose_name = "Контекст"
        verbose_name_plural = "Контексты"

class TargetDescription(models.Model):
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    target_ref = models.ForeignKey('Target', on_delete=models.CASCADE, verbose_name="Целевая группа")
    def __str__(self):
        name_former = ""
        if self.target_ref.name:
            name_former += self.target_ref.name
        if self.info:
            name_former += self.info
        return name_former
    class Meta:
        verbose_name = "Описание целевой группы"
        verbose_name_plural = "Описания целевых групп"

class Activity(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название активности")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    target_ref = models.ForeignKey('Target', on_delete=models.SET_NULL, verbose_name="Целевая группа", default=None, null=True, blank=True)
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Активности"

class ProgramOutput(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название непосредственного результата")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    activity_ref = models.ForeignKey('Activity', on_delete=models.SET_NULL, verbose_name="Активность", default=None, null=True, blank=True)
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет", blank=True, default=0)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Непосредственный результат"
        verbose_name_plural = "Непосредственные результаты"

class ProgramShortOutcome(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название краткосрочного социального результата")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    program_output_ref = models.ForeignKey('ProgramOutput', on_delete=models.SET_NULL, verbose_name="Непосредственный результат", default=None, null=True, blank=True)
    program_output_many_refs = models.ManyToManyField(ProgramOutput, blank=True, verbose_name="Непосредственные результаты", related_name = "program_output_many_refs")
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    outcome_ref = models.ForeignKey('Outcome', on_delete=models.SET_NULL, verbose_name="Социальный результат из библиотеки", default=None, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет", blank=True, default=0)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Краткосрочный социальный результат"
        verbose_name_plural = "Краткосрочные социальные результаты"

class ProgramMidOutcome(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название среднесрочного социального результата")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    program_short_outcome_ref = models.ForeignKey('ProgramShortOutcome', on_delete=models.SET_NULL, verbose_name="Краткосрочный социальный результат", default=None, null=True, blank=True)
    program_short_outcome_many_refs = models.ManyToManyField(ProgramShortOutcome, blank=True, verbose_name="Краткосрочные социальные результаты", related_name = "program_short_outcome_many_refs")
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    outcome_ref = models.ForeignKey('Outcome', on_delete=models.SET_NULL, verbose_name="Социальный результат из библиотеки", default=None, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет", blank=True, default=0)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Среднесрочный социальный результат"
        verbose_name_plural = "Среднесрочные социальные результаты"

class ProgramImpact(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название социального эффекта")
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    program_mid_outcome_ref = models.ForeignKey('ProgramMidOutcome', on_delete=models.SET_NULL, verbose_name="Среднесрочный социальный результат", default=None, null=True, blank=True)
    program_mid_outcome_many_refs = models.ManyToManyField(ProgramMidOutcome, blank=True, verbose_name="Среднесрочные социальные результаты", related_name = "program_mid_outcome_many_refs")
    info = models.TextField(verbose_name="Информация", default=None, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет", blank=True, default=0)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Социальный эффект"
        verbose_name_plural = "Социальные эффекты"

class MonitoringPlanLineOutput(models.Model):
    TOOL_TYPE_CHOICES = [
        ("Tools", 'Библиотека инструментов ПИОН'),
        ("OutcomeMethods", 'Сторонний инструмент'),
    ]
    result_ref = models.ForeignKey('ProgramOutput', on_delete=models.CASCADE, verbose_name="Результат")
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    name = models.CharField(max_length=500, verbose_name="Вопрос", default=None, null=True, blank=True)
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод", default=None, null=True, blank=True)
    tool_type = models.CharField(max_length=100, verbose_name="Откуда инструмент", default="OutcomeMethods", choices=TOOL_TYPE_CHOICES)
    tool = models.CharField(max_length=500, verbose_name="Инструмент", default=None, null=True, blank=True)
    frequency = models.CharField(max_length=500, verbose_name="Частота сбора", default=None, null=True, blank=True)
    reporting = models.CharField(max_length=500, verbose_name="Отчетность и использование", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.result_ref.name:
            name_former += self.result_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Строка плана мониторинга для непосредственного результата"
        verbose_name_plural = "Строки плана мониторинга для непосредственного результата"

class MonitoringPlanLineShortOutcome(models.Model):
    TOOL_TYPE_CHOICES = [
        ("Tools", 'Библиотека инструментов ПИОН'),
        ("OutcomeMethods", 'Сторонний инструмент'),
    ]
    result_ref = models.ForeignKey('ProgramShortOutcome', on_delete=models.CASCADE, verbose_name="Результат")
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    name = models.CharField(max_length=500, verbose_name="Вопрос", default=None, null=True, blank=True)
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод", default=None, null=True, blank=True)
    tool_type = models.CharField(max_length=100, verbose_name="Откуда инструмент", default="OutcomeMethods", choices=TOOL_TYPE_CHOICES)
    tool = models.CharField(max_length=500, verbose_name="Инструмент", default=None, null=True, blank=True)
    frequency = models.CharField(max_length=500, verbose_name="Частота сбора", default=None, null=True, blank=True)
    reporting = models.CharField(max_length=500, verbose_name="Отчетность и использование", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.result_ref.name:
            name_former += self.result_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Строка плана мониторинга для краткосрочного социального результата"
        verbose_name_plural = "Строки плана мониторинга для краткосрочного социального результата"

class MonitoringPlanLineMidOutcome(models.Model):
    TOOL_TYPE_CHOICES = [
        ("Tools", 'Библиотека инструментов ПИОН'),
        ("OutcomeMethods", 'Сторонний инструмент'),
    ]
    result_ref = models.ForeignKey('ProgramMidOutcome', on_delete=models.CASCADE, verbose_name="Результат")
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    name = models.CharField(max_length=500, verbose_name="Вопрос", default=None, null=True, blank=True)
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод", default=None, null=True, blank=True)
    tool_type = models.CharField(max_length=100, verbose_name="Откуда инструмент", default="OutcomeMethods", choices=TOOL_TYPE_CHOICES)
    tool = models.CharField(max_length=500, verbose_name="Инструмент", default=None, null=True, blank=True)
    frequency = models.CharField(max_length=500, verbose_name="Частота сбора", default=None, null=True, blank=True)
    reporting = models.CharField(max_length=500, verbose_name="Отчетность и использование", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.result_ref.name:
            name_former += self.result_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Строка плана мониторинга для среднесрочного социального результата"
        verbose_name_plural = "Строки плана мониторинга для среднесрочного социального результата"

class MonitoringPlanLineImpact(models.Model):
    TOOL_TYPE_CHOICES = [
        ("Tools", 'Библиотека инструментов ПИОН'),
        ("OutcomeMethods", 'Сторонний инструмент'),
    ]
    result_ref = models.ForeignKey('ProgramImpact', on_delete=models.CASCADE, verbose_name="Результат")
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    name = models.CharField(max_length=500, verbose_name="Вопрос", default=None, null=True, blank=True)
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    method = models.CharField(max_length=500, verbose_name="Метод", default=None, null=True, blank=True)
    tool_type = models.CharField(max_length=100, verbose_name="Откуда инструмент", default="OutcomeMethods", choices=TOOL_TYPE_CHOICES)
    tool = models.CharField(max_length=500, verbose_name="Инструмент", default=None, null=True, blank=True)
    frequency = models.CharField(max_length=500, verbose_name="Частота сбора", default=None, null=True, blank=True)
    reporting = models.CharField(max_length=500, verbose_name="Отчетность и использование", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    def __str__(self):
        name_former = ""
        if self.result_ref.name:
            name_former += self.result_ref.name
        if self.name:
            name_former += self.name
        return name_former
    class Meta:
        verbose_name = "Строка плана мониторинга для социального эффекта"
        verbose_name_plural = "Строки плана мониторинга для социального эффекта"

class MonitoringFormLineOutput(models.Model):
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    plan = models.FloatField(verbose_name="Плановое значение", default=None, null=True, blank=True)
    period1 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact1 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period2 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact2 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period3 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact3 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period4 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact4 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    mpl_ref = models.ForeignKey('MonitoringPlanLineOutput', on_delete=models.CASCADE, verbose_name="Строка плана мониторинга", default=None, null=True, blank=True)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.indicator:
            name_former += self.indicator
        return name_former
    class Meta:
        verbose_name = "Строка рабочей формы мониторинга непосредственного результата"
        verbose_name_plural = "Строки рабочей формы мониторинга непосредственного результата"

class MonitoringFormLineShortOutcome(models.Model):
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    plan = models.FloatField(verbose_name="Плановое значение", default=None, null=True, blank=True)
    period1 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact1 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period2 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact2 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period3 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact3 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period4 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact4 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    mpl_ref = models.ForeignKey('MonitoringPlanLineShortOutcome', on_delete=models.CASCADE, verbose_name="Строка плана мониторинга", default=None, null=True, blank=True)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.indicator:
            name_former += self.indicator
        return name_former
    class Meta:
        verbose_name = "Строка рабочей формы мониторинга краткосрочного социального результата"
        verbose_name_plural = "Строки рабочей формы мониторинга краткосрочного социального результата"

class MonitoringFormLineMidOutcome(models.Model):
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    plan = models.FloatField(verbose_name="Плановое значение", default=None, null=True, blank=True)
    period1 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact1 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period2 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact2 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period3 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact3 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period4 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact4 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    mpl_ref = models.ForeignKey('MonitoringPlanLineMidOutcome', on_delete=models.CASCADE, verbose_name="Строка плана мониторинга", default=None, null=True, blank=True)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.indicator:
            name_former += self.indicator
        return name_former
    class Meta:
        verbose_name = "Строка рабочей формы мониторинга среднесрочного социального результата"
        verbose_name_plural = "Строки рабочей формы мониторинга среднесрочного социального результата"

class MonitoringFormLineImpact(models.Model):
    indicator = models.CharField(max_length=500, verbose_name="Показатель", default=None, null=True, blank=True)
    sort_index = models.IntegerField(verbose_name="Индекс сортировки", default=0)
    plan = models.FloatField(verbose_name="Плановое значение", default=None, null=True, blank=True)
    period1 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact1 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period2 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact2 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period3 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact3 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    period4 = models.CharField(max_length=500, verbose_name="Период сбора", default=None, null=True, blank=True)
    fact4 = models.FloatField(verbose_name="Фактическое значение", default=None, null=True, blank=True)
    program_ref = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name="Программа")
    mpl_ref = models.ForeignKey('MonitoringPlanLineImpact', on_delete=models.CASCADE, verbose_name="Строка плана мониторинга", default=None, null=True, blank=True)
    def __str__(self):
        name_former = ""
        if self.program_ref.name:
            name_former += self.program_ref.name
        if self.indicator:
            name_former += self.indicator
        return name_former
    class Meta:
        verbose_name = "Строка рабочей формы мониторинга социального эффекта"
        verbose_name_plural = "Строки рабочей формы мониторинга социального эффекта"
