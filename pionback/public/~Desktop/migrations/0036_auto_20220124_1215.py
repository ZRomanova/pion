# Generated by Django 2.0.2 on 2022-01-24 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0035_auto_20220124_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysismethod',
            options={'verbose_name': 'Метод анализа', 'verbose_name_plural': 'Метод анализа'},
        ),
        migrations.AlterModelOptions(
            name='evaluationtype',
            options={'verbose_name': 'Вид оценки', 'verbose_name_plural': 'Вид оценки'},
        ),
        migrations.AlterModelOptions(
            name='representationmethod',
            options={'verbose_name': 'Представления данных в отчете', 'verbose_name_plural': 'Представления данных в отчете'},
        ),
        migrations.AddField(
            model_name='logicalmodel',
            name='add_public_confirm',
            field=models.BooleanField(default=False, verbose_name='Подтверждение администратором'),
        ),
        migrations.AddField(
            model_name='logicalmodel',
            name='add_public_will',
            field=models.BooleanField(default=False, verbose_name='В общую библиотеку'),
        ),
        migrations.AddField(
            model_name='logicalmodel',
            name='createdby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='add_public_confirm',
            field=models.BooleanField(default=False, verbose_name='Подтверждение администратором '),
        ),
        migrations.AddField(
            model_name='outcome',
            name='add_public_will',
            field=models.BooleanField(default=False, verbose_name='В общую библиотеку'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='createdby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='analysismethod',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название метод анализа'),
        ),
        migrations.AlterField(
            model_name='evaluationtype',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название вида оценки'),
        ),
        migrations.AlterField(
            model_name='representationmethod',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название представления данных в отчете'),
        ),
    ]
