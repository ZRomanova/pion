# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-10 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0037_auto_20180310_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='target_refs',
            field=models.ManyToManyField(blank=True, to='rcapp.Target', verbose_name='Целевые группы'),
        ),
    ]
