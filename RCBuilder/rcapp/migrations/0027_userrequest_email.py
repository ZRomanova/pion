# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-22 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0026_auto_20180116_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='email',
            field=models.CharField(default='', max_length=100, verbose_name='Адрес электронной почты'),
            preserve_default=False,
        ),
    ]
