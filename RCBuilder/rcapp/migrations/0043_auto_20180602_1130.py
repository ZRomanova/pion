# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-02 11:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0042_auto_20180602_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequest',
            name='region',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, message='Недопустимое значение региона')], verbose_name='Регион'),
        ),
    ]