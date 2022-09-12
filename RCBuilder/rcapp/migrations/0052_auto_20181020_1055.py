# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-20 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0051_auto_20181020_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='impactindicator',
            name='data_source_desc',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AddField(
            model_name='outcomeindicator',
            name='data_source_desc',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AddField(
            model_name='outputindicator',
            name='data_source_desc',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Источник данных'),
        ),
        migrations.AlterField(
            model_name='impactindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Инстумент сбора данных'),
        ),
        migrations.AlterField(
            model_name='outcomeindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Инстумент сбора данных'),
        ),
        migrations.AlterField(
            model_name='outputindicator',
            name='data_source',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Инстумент сбора данных'),
        ),
    ]