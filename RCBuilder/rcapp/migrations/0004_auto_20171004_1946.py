# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0003_auto_20171001_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='impactindicator',
            name='recieve_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Время сбора'),
        ),
        migrations.AddField(
            model_name='outcomeindicator',
            name='recieve_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Время сбора'),
        ),
        migrations.AddField(
            model_name='outputindicator',
            name='recieve_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Время сбора'),
        ),
    ]