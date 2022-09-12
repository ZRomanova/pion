# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0009_auto_20171005_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydata',
            name='realization_region',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Регионы реализации программы'),
        ),
        migrations.AddField(
            model_name='companydata',
            name='reg_region',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Регион регистрации'),
        ),
    ]