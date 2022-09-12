# Generated by Django 3.0.8 on 2020-07-18 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outcomeexactname',
            options={'verbose_name': 'Частная формулировка социального результата', 'verbose_name_plural': 'Частные формулировки социального результата'},
        ),
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=500, verbose_name='Адрес эл. почты')),
                ('lastname', models.CharField(max_length=500, verbose_name='Фамилия')),
                ('firstname', models.CharField(max_length=500, verbose_name='Имя')),
                ('middlename', models.CharField(max_length=500, verbose_name='Отчество')),
                ('region', models.CharField(max_length=500, verbose_name='Регион')),
                ('organization', models.CharField(max_length=500, verbose_name='Организация')),
                ('website', models.CharField(max_length=500, verbose_name='Веб-сайт или адрес организации в социальных сетях')),
                ('position', models.CharField(max_length=500, verbose_name='Должность')),
                ('password', models.CharField(max_length=500, verbose_name='Пароль')),
                ('createdon', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата создания')),
                ('acceptedon', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата подтверждения')),
                ('lastseenon', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата последнего визита')),
                ('user_ref', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запрос на регистрацию',
                'verbose_name_plural': 'Запросы на регистрацию',
            },
        ),
        migrations.CreateModel(
            name='OutcomeLibraryLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Outcome', verbose_name='Социальный результат')),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Связь социального результата с личной библиотекой',
                'verbose_name_plural': 'Связи социального результата с личной библиотекой',
            },
        ),
    ]