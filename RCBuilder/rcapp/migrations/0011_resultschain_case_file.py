# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-17 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0010_auto_20171006_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultschain',
            name='case_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Загрузить файл с кейсом по данной программе'),
        ),
    ]
