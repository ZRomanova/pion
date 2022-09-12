from django.apps import AppConfig


class PublicConfig(AppConfig):
    name = 'public'
    verbose_name = 'public (этот раздел работает, раздел выше не работает)'
