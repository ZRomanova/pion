# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-20 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0052_auto_20181020_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcomeindicator',
            name='values_plan',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Значения плана показателя'),
        ),
        migrations.AddField(
            model_name='outputindicator',
            name='values_plan',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Значения плана показателя'),
        ),
        migrations.AlterField(
            model_name='impactindicator',
            name='values',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Значения плана показателя'),
        ),
    ]
