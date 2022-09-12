from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Main page models

class Description(models.Model):
    title = models.CharField(max_length=40)
    logo_name = models.CharField(max_length=20)
    order = models.IntegerField()
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'

class Contact(models.Model):
    order = models.IntegerField()
    logo_name = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    link_to = models.CharField(max_length=300, blank=True)
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

class SocialNetworkLink(models.Model):
    order = models.IntegerField()
    logo_name = models.CharField(max_length=20)
    link_to = models.CharField(max_length=300)
    def __str__(self):
        return self.logo_name
    class Meta:
        verbose_name = 'Ссылка на соц.сеть'
        verbose_name_plural = 'Ссылки на социальные сети'

# HERE!!

class Document(models.Model):
    name = models.CharField(max_length=200)
    content = models.FileField(upload_to='%Y/%m/%d/')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Документ страницы материалы'
        verbose_name_plural = 'Документы страницы материалы'
        
class Page(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название страницы")
    content = RichTextUploadingField(default=None, null=True, blank=True, verbose_name="Содержание")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

class TargetsHyperlink(models.Model):
    name = models.CharField(max_length=500, verbose_name="Текст ссылки")
    url = models.CharField(max_length=200, verbose_name="URL ссылки")
    def __str__(self):
        return self.name + '. URL:' + self.url
    class Meta:
        verbose_name = "Ссылка страницы целевых групп"
        verbose_name = "Ссылки страницы целевых групп"