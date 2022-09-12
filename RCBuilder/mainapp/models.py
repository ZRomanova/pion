from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse

User = get_user_model()

class newsManager:
    @staticmethod
    def category_list(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')
            products.extend(model_products)

        return products

class newsitemlist:
    objects = newsManager()


class MainForm(models.Model):
    class Meta():
        db_table = 'user_mail'
        verbose_name = "Форма обратной связи"
        verbose_name_plural = "Форма обратной связи"

    fname = models.CharField(max_length=255, verbose_name='Имя')
    lname = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    mail = models.EmailField(verbose_name='Mail')
    msg = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.mail

class Subscription(models.Model):
    class Meta():
        db_table = 'mail_list'
        verbose_name = "Подписки"
        verbose_name_plural = "Подписки"

    mail = models.EmailField(verbose_name='Mail')

    def __str__(self):
        return self.mail

class NewsCat(models.Model):
    class Meta():
        db_table = 'naws_cat'
        verbose_name = "Разделы новостей"
        verbose_name_plural = "Разделы новостей"
        ordering = ["create"]


    STATUS_NORMAL = 'normal'
    STATUS_BIG = 'big'
    STATUS_OVER_BIG = 'over_big'

    STATUS_CHOICES = (
        (STATUS_NORMAL, 'Нормальный'),
        (STATUS_BIG, 'Большой'),
        (STATUS_OVER_BIG, 'Очень большой'),
    )

    size = models.CharField(max_length=255, default=STATUS_NORMAL, choices=STATUS_CHOICES, verbose_name='Шрифт')

    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)
    create = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.name

class News(models.Model):
    class Meta():
        db_table = 'naws'
        verbose_name = "Новости"
        verbose_name_plural = "Новости"
        ordering = ["-create"]

    category = models.ForeignKey(NewsCat, verbose_name='Категория', on_delete=models.CASCADE)
    create = models.DateTimeField("Дата создания", auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name='Название новости')
    title = models.CharField(max_length=255, verbose_name='title в браузере')
    desc = models.CharField(max_length=255, verbose_name='desc в браузере')
    slug = models.SlugField(unique=True)

    image = models.ImageField(verbose_name='Изображение')

    minitext = models.TextField(verbose_name='Краткое описание', null=True)
    maintext = models.TextField(verbose_name='Описание', null=True)

    active = models.BooleanField("Активно", default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return get_news_url(self, 'news_detail')