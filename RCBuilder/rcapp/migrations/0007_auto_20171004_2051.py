# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0006_remove_impactindicator_method_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='impactindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AddField(
            model_name='impactindicator',
            name='data_source_custom',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Свой вариант'),
        ),
        migrations.AddField(
            model_name='outcomeindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AddField(
            model_name='outcomeindicator',
            name='data_source_custom',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Свой вариант'),
        ),
        migrations.AddField(
            model_name='outputindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AddField(
            model_name='outputindicator',
            name='data_source_custom',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Свой вариант'),
        ),
    ]
