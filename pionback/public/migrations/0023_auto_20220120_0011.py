# Generated by Django 2.0.2 on 2022-01-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0022_accordance_activitiestypes_addressee_elementsmonitoring_method_practicetype_resultlevel_sociallibrar'),
    ]

    operations = [
        migrations.AddField(
            model_name='accordance',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.Accordance', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='activitiestypes',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.ActivitiesTypes', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='addressee',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.Addressee', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='elementsmonitoring',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.ElementsMonitoring', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='method',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.Method', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='practicetype',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.PracticeType', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='resultlevel',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.ResultLevel', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='sociallibrarypeon',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.SocialLibraryPEON', verbose_name='Подразделы'),
        ),
        migrations.AddField(
            model_name='thematicgroup',
            name='subgroup',
            field=models.ManyToManyField(blank=True, to='public.ThematicGroup', verbose_name='Подразделы'),
        ),
    ]
