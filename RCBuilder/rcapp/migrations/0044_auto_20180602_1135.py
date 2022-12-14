# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-02 11:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0043_auto_20180602_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='site',
            field=models.CharField(default='--', max_length=100, validators=[django.core.validators.MinLengthValidator(2, message='Недопустимое значение')], verbose_name='Веб сайт или адрес в социальных сетях'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='organization',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, message='Недопустимое значение организации')], verbose_name='Организация'),
        ),
    ]
